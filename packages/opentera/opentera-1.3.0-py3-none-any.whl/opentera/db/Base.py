import inspect
import datetime
import time
import typing as t
import sqlalchemy.sql.sqltypes
from flask_sqlalchemy import SQLAlchemy, query, model
from sqlalchemy import Column, BigInteger
from sqlalchemy.inspection import inspect as sqlinspector
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class _QueryProperty:
    def __get__(self, obj: model.Model | None, cls: t.Type[model.Model]) -> query.Query:
        return cls.db().session.query(cls)


class BaseMixin(object):
    version_id = Column(BigInteger, nullable=False, default=int(time.time()*1000))

    # Using timestamp as version tracker - multiplying by 1000 to keep ms part without using floats (which seems to
    # cause problems with the mapper)
    __mapper_args__ = {
        'version_id_col': version_id,
        'version_id_generator': lambda version: int(time.time()*1000)
    }

    # This needs to be initialized by app
    __db__: SQLAlchemy = None

    @classmethod
    def set_db(cls, db: SQLAlchemy):
        cls.__db__ = db

    @classmethod
    def create_all(cls):
        if cls.__db__ and cls.__db__.engine:
            cls.__db__.create_all()
            cls.metadata.create_all(cls.__db__.engine)

    query = _QueryProperty()

    @classmethod
    def db(cls) -> SQLAlchemy:
        return cls.__db__

    def to_json(self, ignore_fields=None):
        if ignore_fields is None:
            ignore_fields = []
        pr = {}
        # Add relationships in ignore_fields by default
        for relation in sqlinspector(self.__class__).relationships.items():
            if relation[0] not in ignore_fields:
                # print('-- Ignoring ' + relation[0] + ' in to_json()')
                ignore_fields.append(relation[0])

        for name in dir(self):
            if (self.is_valid_property_name(name) and name not in ignore_fields) or name == 'deleted_at':
                value = getattr(self, name)
                if name == 'deleted_at' and value is None:
                    continue  # If deleted field, but not deleted, don't add to the json
                if self.is_valid_property_value(value):
                    if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                        value = value.isoformat()
                    if isinstance(value, datetime.timedelta):
                        # Strip too many zeros at the end
                        value_times = str(value).split(".")
                        if len(value_times) > 1:
                            value_times[1] = value_times[1][0:3]
                            value = value_times[0] + '.' + value_times[1]
                        else:
                            value = value_times[0]
                    pr[name] = value
        return pr

    def from_json(self, json, ignore_fields=None):
        if ignore_fields is None:
            ignore_fields = []
        ignore_fields.append('deleted_at')
        for name in json:
            if name not in ignore_fields:
                if hasattr(self, name):
                    # Test for datetime as string
                    # This is a fix for SQLITE that does not convert str to datetime automatically
                    if isinstance(self.__table__.columns[name].type, sqlalchemy.sql.sqltypes.TIMESTAMP) \
                            and isinstance(json[name], str) and len(json[name]) > 0:
                        setattr(self, name, datetime.datetime.fromisoformat(json[name]))
                    else:
                        setattr(self, name, json[name])
                else:
                    print('Attribute ' + name + ' not found.')

    def to_json_create_event(self):
        # Default is None, will not be sent
        return None

    def to_json_update_event(self):
        # Default is None, will not be sent
        return None

    def to_json_delete_event(self):
        # Default is None, will not be sent
        return None

    @staticmethod
    def is_valid_property_name(name: str) -> bool:
        return not name.startswith('__') and not name.startswith('_') and not name.startswith('query') and \
               not name.startswith('metadata') and name != 'version_id' and name != 'registry' and name != 'deleted_at'

    @staticmethod
    def is_valid_property_value(value: str) -> bool:
        return not inspect.ismethod(value) and not inspect.isfunction(value)

    @classmethod
    def clean_values(cls, values: dict):
        # This method is used to remove item from the values dict that are not properties of the object
        obj_properties = list()

        # Build available properties
        for name in dir(cls):
            value = getattr(cls, name)
            if cls.is_valid_property_name(name) and cls.is_valid_property_value(value):
                obj_properties.append(name)

        # Remove any property not in the available list
        clean_values = values.copy()
        for value in values:
            if value not in obj_properties:
                del clean_values[value]

        return clean_values

    @classmethod
    def get_count(cls, filters: dict = None, with_deleted: bool = False) -> int:
        count_query = cls.db().session.query(cls).execution_options(include_deleted=with_deleted)
        if filters:
            count_query = count_query.filter_by(**filters)
        return count_query.count()

    @classmethod
    def get_primary_key_name(cls) -> str:
        from sqlalchemy import inspect
        return inspect(cls).primary_key[0].name

    @classmethod
    def get_model_name(cls) -> str:
        key = cls.get_primary_key_name()
        key_split = key.split('_', 1)
        return key_split[-1]

    @classmethod
    def update(cls, update_id: int, values: dict):
        update_values = cls.clean_values(values)
        if len(update_values) != len(values):
            raise SQLAlchemyError('Invalid values passed to update')

        if cls.get_primary_key_name() in update_values and update_id != update_values[cls.get_primary_key_name()]:
            raise SQLAlchemyError(f'Primary key cannot be updated ({cls.get_primary_key_name()})')

        # with Session(cls.db().engine) as session:
        update_obj = cls.db().session.query(cls).filter(getattr(cls, cls.get_primary_key_name()) == update_id).first()

        if update_obj:
            update_obj.from_json(update_values)
            cls.db().session.commit()
        else:
            raise SQLAlchemyError(cls.__name__ + ' with id ' + str(update_id) + ' cannot update.')

    @classmethod
    def commit(cls):
        cls.db().session.commit()

    @classmethod
    def insert(cls, db_object):
        if getattr(db_object, 'soft_insert', None):
            return db_object.soft_insert(db_object)
        else:
            # Clear primary key value
            setattr(db_object, cls.get_primary_key_name(), None)

            # Add to database session and commit
            cls.db().session.add(db_object)
            cls.commit()
            return db_object

    def delete_check_integrity(self, with_deleted: bool = False) -> IntegrityError | None:
        return None  # Can delete by default

    @classmethod
    def delete(cls, id_todel, autocommit: bool = True, hard_delete: bool = False):
        if hard_delete:
            cls.handle_include_deleted_flag(True)
            autocommit = False
        delete_obj = cls.db().session.query(cls).filter(getattr(cls, cls.get_primary_key_name()) == id_todel).first()

        if delete_obj:
            has_soft_delete = getattr(delete_obj, 'soft_delete', None) is not None
            has_hard_delete = getattr(delete_obj, 'hard_delete', None) is not None

            if (has_soft_delete and not delete_obj.deleted_at) or not has_soft_delete:
                # Don't check integrity for already soft-deleted objects
                cannot_be_deleted_exception = delete_obj.delete_check_integrity()
                if cannot_be_deleted_exception:
                    raise cannot_be_deleted_exception

            if has_soft_delete and not hard_delete:
                delete_obj.soft_delete()
            else:
                # if has_soft_delete:
                #     # Check that object was soft deleted before doing a hard delete
                #     if not delete_obj.deleted_at:
                #         # Object must be soft deleted first before being hard deleted!
                #         raise SQLAlchemyError(cls.__name__ + ' with id ' + str(id_todel) +
                #                               ' cannot be hard deleted: not soft deleted beforehand!')
                if has_hard_delete and hard_delete:
                    delete_obj.hard_delete()
                else:
                    cls.db().session.delete(delete_obj)
            if autocommit:
                cls.commit()
        else:
            raise SQLAlchemyError(cls.__name__ + ' with id ' + str(id_todel) + ' cannot delete.')
        if hard_delete:
            cls.handle_include_deleted_flag(False)

    @classmethod
    def undelete(cls, id_to_undelete):
        undelete_obj = cls.db().session.query(cls).execution_options(include_deleted=True).filter(
            getattr(cls, cls.get_primary_key_name()) == id_to_undelete).first()
        if undelete_obj:
            if getattr(undelete_obj, 'soft_undelete', None):
                undelete_obj.soft_undelete()
            cls.commit()
        else:
            print(cls.__name__ + ' with id ' + str(id_to_undelete) + ' cannot undelete.')
            raise SQLAlchemyError(cls.__name__ + ' with id ' + str(id_to_undelete) + ' cannot undelete.')

    @classmethod
    def handle_include_deleted_flag(cls, include_deleted=False):
        if 'include_deleted' not in cls.db().session.info:
            cls.db().session.info['include_deleted'] = list()

        if include_deleted:
            cls.db().session.info['include_deleted'].append(cls.get_model_name())
        else:
            cls.db().session.info['include_deleted'].pop(-1)

    @classmethod
    def query_with_filters(cls, filters=None, with_deleted: bool = False):
        if filters is None:
            filters = dict()

        return cls.db().session.query(cls).execution_options(include_deleted=with_deleted).filter_by(**filters).all()

    @classmethod
    def get_json_schema(cls) -> dict:
        # Get model prefix (name)
        model_name = cls.get_model_name()

        # Browse each
        pr_dict = dict()
        required_fields: list[str] = []

        for name in dir(cls):
            value = getattr(cls, name)
            if cls.is_valid_property_name(name) and cls.is_valid_property_value(value) and \
                    (name.startswith(model_name) or name.startswith('id')):
                # Ok so far, do we have a column and not a relationship or something else?
                if 'ColumnProperty' in str(type(value.prop)):
                    # Get correct data type
                    data_type = 'object'
                    data_format = None
                    column_type = str(value.prop.columns[0].type).lower()
                    # Add primary key to required fields
                    if value.prop.columns[0].primary_key:
                        required_fields.append(name)
                    default_value = value.prop.columns[0].default
                    if 'string' in column_type or 'timestamp' in column_type or 'varchar' in column_type:
                        data_type = 'string'
                        if 'uuid' in name:
                            data_format = 'uuid'
                        if 'timestamp' in column_type:
                            data_format = 'date-time'
                    if 'integer' in column_type:
                        data_type = 'integer'
                    if 'boolean' in column_type:
                        data_type = 'boolean'

                    pr_dict[name] = {'type': data_type}
                    if data_format:
                        pr_dict[name]['format'] = data_format
                    if default_value:
                        if hasattr(default_value, 'arg'):
                            if not callable(default_value.arg):
                                pr_dict[name]['default'] = default_value.arg

        schema = {model_name: {'properties': pr_dict,
                               'type': 'object',
                               'required': required_fields,
                               'additionalProperties': False}}

        return schema

    @classmethod
    def validate_required_fields(cls, json_data: dict, ignore_fields: list = None):
        if not ignore_fields:
            ignore_fields = []

        # Get model prefix (name)
        model_name = cls.get_model_name()
        missing_fields = []

        # Browse each
        for name in dir(cls):
            value = getattr(cls, name)
            if cls.is_valid_property_name(name) and cls.is_valid_property_value(value) and \
                    (name.startswith(model_name) or name.startswith('id')) and not name.endswith('uuid'):
                # Ok so far, check if column is required or not
                if 'ColumnProperty' in str(type(value.prop)):
                    if not value.prop.columns[0].nullable and name not in json_data and name not in ignore_fields and \
                            not value.prop.columns[0].default:
                        missing_fields.append(name)

        return missing_fields


# Declarative base, inherit from Base for all models
BaseModel = sqlalchemy.orm.declarative_base(cls=BaseMixin)
