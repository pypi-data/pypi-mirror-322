import jwt
import json
import time
from opentera.redis.RedisVars import RedisVars
from opentera.redis.RedisClient import RedisClient
from requests import get, post, Response, delete
from opentera.services.ServiceConfigManager import ServiceConfigManager
import opentera.messages.python as messages
from twisted.internet import defer
import datetime
from opentera.logging.LoggingClient import LoggingClient
from opentera.services.ServiceAccessManager import ServiceAccessManager


class ServiceOpenTera(RedisClient):

    def __init__(self, config_man: ServiceConfigManager, service_info):
        # First initialize redis
        RedisClient.__init__(self, config_man.redis_config)

        # Initialize logger
        self.logger = LoggingClient(config_man.redis_config, 'LoggingClient_' + self.__class__.__name__)

        # Store service info
        self.service_info = service_info

        # Store RPC API
        self.rpc_api = dict()

        # Store config
        self.config = config_man.service_config
        self.config_man = config_man

        # Take values from config_man
        # Values are checked when config is loaded...
        self.backend_hostname = config_man.backend_config['hostname']
        self.backend_port = config_man.backend_config['port']
        self.service_uuid = config_man.service_config['ServiceUUID']

        # Create service token for service api requests
        self.service_token = self.service_generate_token()

        # Init service access manager
        ServiceAccessManager.init_access_manager(service=self)

    def redisConnectionMade(self):
        print('*** ServiceOpenTera.redisConnectionMade for', self.config['name'])

        # Build RPC interface
        self.setup_rpc_interface()

        # Build standard interface
        self.build_interface()

        # Register to system events
        self.register_to_events()

    def setup_rpc_interface(self):
        self.rpc_api['session_type_config'] = {'args': ['int:id_session_type'],
                                               'returns': 'dict',
                                               'callback': self.get_session_type_config_form}

    def register_to_events(self):
        # Should be implemented in derived classes
        yield None

    def notify_service_messages(self, pattern, channel, message):
        pass

    @defer.inlineCallbacks
    def build_interface(self):
        # TODO not sure of the interface using UUID or name here...
        # Will do  both!
        yield self.subscribe_pattern_with_callback(
            RedisVars.build_service_message_topic( self.service_info['service_uuid']), self.notify_service_messages)

        yield self.subscribe_pattern_with_callback(
            RedisVars.build_service_message_topic(self.service_info['service_key']), self.notify_service_messages)

        yield self.subscribe_pattern_with_callback(
            RedisVars.build_service_rpc_topic(self.service_info['service_uuid']), self.notify_service_rpc)

        yield self.subscribe_pattern_with_callback(
            RedisVars.build_service_rpc_topic(self.service_info['service_key']), self.notify_service_rpc)

    def notify_service_rpc(self, pattern, channel, message):
        # import threading
        # print('ServiceOpenTera - Received rpc', self, pattern, channel, message, ' thread:', threading.current_thread())

        rpc_message = messages.RPCMessage()

        try:
            # Look for a RPCMessage
            rpc_message.ParseFromString(message)

            if self.rpc_api.__contains__(rpc_message.method):

                # RPC method found, call it with the args
                args = list()
                kwargs = dict()

                # TODO type checking with declared rpc interface ?
                for value in rpc_message.args:
                    # Append the oneof value to args
                    args.append(getattr(value, value.WhichOneof('arg_value')))

                # Call callback function
                ret_value = self.rpc_api[rpc_message.method]['callback'](*args, **kwargs)

                # More than we need?
                my_dict = {'method': rpc_message.method,
                           'id': rpc_message.id,
                           'pattern': pattern,
                           'status': 'OK',
                           'return_value': ret_value}

                json_data = json.dumps(my_dict)

                # Return result (a json string)
                self.publish(rpc_message.reply_to, json_data)

        except Exception as e:
            import sys
            print('Error calling rpc method', message, sys.exc_info(), e)
            my_dict = {'method': rpc_message.method,
                       'id': rpc_message.id,
                       'pattern': pattern,
                       'status': 'Error',
                       'return_value': None}

            json_data = json.dumps(my_dict)

            # Return result (a json string)
            self.publish(rpc_message.reply_to, json_data)

    def service_generate_token(self):
        # Use redis key to generate token
        # Creating token with service info
        # TODO ADD MORE FIELDS?
        payload = {
            'iat': int(time.time()),
            'service_uuid': self.service_uuid
        }

        return jwt.encode(payload, self.redisGet(RedisVars.RedisVar_ServiceTokenAPIKey), algorithm='HS256')

    def post_to_opentera(self, api_url: str, json_data: dict) -> Response:
        return self.post_to_opentera_with_token(self.service_token, api_url, json_data)

    def get_from_opentera(self, api_url: str, params: dict) -> Response:
        return self.get_from_opentera_with_token(self.service_token, api_url, params)

    def delete_from_opentera(self, api_url: str, params: dict) -> Response:
        return self.delete_from_opentera_with_token(self.service_token, api_url, params)

    def get_from_opentera_with_token(self, token: str, api_url: str, params: dict = None,
                                     additional_headers: dict = None) -> Response:
        request_headers = {'Authorization': 'OpenTera ' + token}
        if params is None:
            params = {}

        if additional_headers is not None:
            request_headers.update(additional_headers)

        backend_url = f"https://{self.backend_hostname}:{self.backend_port}"
        # TODO fix verify=False
        return get(url=backend_url + api_url, headers=request_headers, params=params, verify=False, timeout=10)

    def post_to_opentera_with_token(self, token: str,  api_url: str, json_data: dict, params: dict = None,
                                    additional_headers: dict = None) -> Response:
        request_headers = {'Authorization': 'OpenTera ' + token}
        if params is None:
            params = {}

        if additional_headers is not None:
            request_headers.update(additional_headers)

        backend_url = f"https://{self.backend_hostname}:{self.backend_port}"
        # TODO fix verify=False
        return post(url=backend_url + api_url, headers=request_headers, json=json_data, params=params, verify=False, timeout=10)

    def delete_from_opentera_with_token(self, token: str, api_url: str, params: dict = None,
                                        additional_headers: dict = None) -> Response:
        request_headers = {'Authorization': 'OpenTera ' + token}
        if params is None:
            params = {}

        if additional_headers is not None:
            request_headers.update(additional_headers)

        backend_url = f"https://{self.backend_hostname}:{self.backend_port}"
        # TODO fix verify=False
        return delete(url=backend_url + api_url, headers=request_headers, params=params, verify=False, timeout=10)

    def send_event_message(self, event, topic: str):
        message = self.create_event_message(topic)
        any_message = messages.Any()
        any_message.Pack(event)
        message.events.extend([any_message])
        return self.publish(message.header.topic, message.SerializeToString())

    def send_service_event_message(self, event):
        topic = RedisVars.build_service_event_topic(self.service_info['service_key'])
        self.send_event_message(event, topic)

    def create_event_message(self, topic):
        event_message = messages.TeraEvent()
        event_message.header.version = 1
        event_message.header.time = datetime.datetime.now().timestamp()
        event_message.header.topic = topic
        return event_message

    def send_tera_message(self, event, src: str, topic: str):
        message = self.create_tera_message(src, topic)
        any_message = messages.Any()
        any_message.Pack(event)
        message.data.extend([any_message])
        return self.publish(topic, message.SerializeToString())

    def create_tera_message(self, src='', dest='', seq=0):
        tera_message = messages.TeraModuleMessage()
        tera_message.head.version = 1
        tera_message.head.time = datetime.datetime.now().timestamp()
        tera_message.head.seq = seq
        tera_message.head.source = src
        tera_message.head.dest = dest
        return tera_message

    def get_session_type_config_form(self, id_session_type: int) -> dict:
        # Default session type config form for services
        return {}
