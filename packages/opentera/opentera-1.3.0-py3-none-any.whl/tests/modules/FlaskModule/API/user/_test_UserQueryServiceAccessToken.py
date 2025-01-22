from tests.modules.FlaskModule.API.user.BaseUserAPITest import BaseUserAPITest
from opentera.db.models.TeraService import TeraService
from opentera.db.models.TeraServiceRole import TeraServiceRole
from opentera.db.models.TeraServiceProject import TeraServiceProject
from opentera.db.models.TeraServiceSite import TeraServiceSite
from opentera.db.models.TeraUserGroup import TeraUserGroup
from opentera.db.models.TeraServiceAccess import TeraServiceAccess
from opentera.db.models.TeraUser import TeraUser
import jwt


class UserQueryServiceAccessTokenTest(BaseUserAPITest):
    test_endpoint = '/api/user/services/access/token'

    def setUp(self):
        super().setUp()
        with self._flask_app.app_context():
            service = TeraService.get_service_by_key('BureauActif')
            self.id_test_service = service.id_service
            self.test_service_key = service.service_key
            # Create global roles for that service
            self.role1 = TeraServiceRole()
            self.role1.id_service = service.id_service
            self.role1.service_role_name = 'role1'
            TeraServiceRole.insert(self.role1)

            self.role2 = TeraServiceRole()
            self.role2.id_service = service.id_service
            self.role2.service_role_name = 'role2'
            TeraServiceRole.insert(self.role2)

            self.role3 = TeraServiceRole()
            self.role3.id_service = service.id_service
            self.role3.service_role_name = 'role3'
            TeraServiceRole.insert(self.role3)

            # Associate service to project / site
            service_site = TeraServiceSite()
            service_site.id_service = service.id_service
            service_site.id_site = 1
            TeraServiceSite.insert(service_site)

            service_project = TeraServiceProject()
            service_project.id_service = service.id_service
            service_project.id_project = 1
            TeraServiceProject.insert(service_project)

            # Associate roles to user(group) for user3
            self.id_test_user_group = TeraUserGroup.get_user_group_by_group_name("Admins - Project 1").id_user_group
            access = TeraServiceAccess()
            access.id_user_group = self.id_test_user_group
            access.id_service_role = self.role1.id_service_role
            TeraServiceAccess.insert(access)

            access = TeraServiceAccess()
            access.id_user_group = self.id_test_user_group
            access.id_service_role = self.role2.id_service_role
            TeraServiceAccess.insert(access)

    def tearDown(self):
        super().tearDown()

    def test_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.get(self.test_endpoint)
            self.assertEqual(401, response.status_code)

    def test_post_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.post(self.test_endpoint)
            self.assertEqual(405, response.status_code)

    def test_delete_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.delete(self.test_endpoint)
            self.assertEqual(405, response.status_code)

    def test_get_endpoint_invalid_http_auth(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='invalid', password='invalid')
            self.assertEqual(401, response.status_code)

    def test_get_endpoint_invalid_token_auth(self):
        with self._flask_app.app_context():
            response = self._get_with_user_token_auth(self.test_client, token='invalid')
            self.assertEqual(401, response.status_code)

    def test_get_access_levels(self):
        response = self._get_with_user_http_auth(self.test_client, username='user4', password='user4')
        self.assertEqual(400, response.status_code, msg='Missing id_service')
        response = self._get_with_user_http_auth(self.test_client, username='user4', password='user4',
                                                 params={'id_service': self.id_test_service})
        self.assertEqual(403, response.status_code, msg='No access to service')
        response = self._get_with_user_http_auth(self.test_client, username='user3', password='user3',
                                                 params={'id_service': self.id_test_service})
        self.assertEqual(200, response.status_code, msg='Service accessible')
        response = self._get_with_user_http_auth(self.test_client, username='admin', password='admin',
                                                 params={'id_service': self.id_test_service})
        self.assertEqual(200, response.status_code, msg='Service accessible')

    def test_get_global_access(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='user3', password='user3',
                                                     params={'id_service': self.id_test_service})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='user3')

    def test_get_sites_access(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='user3', password='user3',
                                                     params={'id_service': self.id_test_service, 'with_sites': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='user3')
            self._validate_sites_structure(token_dict=token_dict, username='user3')

    def test_get_sites_access_site_admin(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='siteadmin', password='siteadmin',
                                                     params={'id_service': self.id_test_service, 'with_sites': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='siteadmin')
            self._validate_sites_structure(token_dict=token_dict, username='siteadmin')

    def test_get_sites_access_super_admin(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='admin', password='admin',
                                                     params={'id_service': self.id_test_service, 'with_sites': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='admin')
            self._validate_sites_structure(token_dict=token_dict, username='admin')

    def test_get_projects_access(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='user3', password='user3',
                                                     params={'id_service': self.id_test_service, 'with_projects': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='user3')
            self._validate_projects_structure(token_dict=token_dict, username='user3')

    def test_get_projects_access_super_admin(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='admin', password='admin',
                                                     params={'id_service': self.id_test_service, 'with_projects': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='admin')
            self._validate_projects_structure(token_dict=token_dict, username='admin')

    def test_get_sites_projects_access(self):
        with self._flask_app.app_context():
            response = self._get_with_user_http_auth(self.test_client, username='user3', password='user3',
                                                     params={'id_service': self.id_test_service, 'with_projects': 1,
                                                             'with_sites': 1})
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.json)
            token = response.json
            token_dict = jwt.decode(token, self.user_token_key, algorithms='HS256')
            self._validate_global_structure(token_dict=token_dict, username='user3')
            self._validate_sites_structure(token_dict=token_dict, username='user3')
            self._validate_projects_structure(token_dict=token_dict, username='user3')

    def _validate_global_structure(self, token_dict: dict,  username: str):
        self.assertTrue('user_access' in token_dict)
        self.assertTrue('services' in token_dict['user_access'])
        self.assertTrue(self.test_service_key in token_dict['user_access']['services'])
        self.assertTrue('global' in token_dict['user_access']['services'][self.test_service_key])

        user = TeraUser.get_user_by_username(username)
        access = user.get_service_roles(self.id_test_service)

        self.assertEqual(len(access), len(token_dict['user_access']['services'][self.test_service_key]['global']))
        for acc in access:
            self.assertTrue(acc in token_dict['user_access']['services'][self.test_service_key]['global'])

    def _validate_sites_structure(self, token_dict: dict, username: str):
        self.assertTrue(self.test_service_key in token_dict['user_access']['services'])
        self.assertTrue('OpenTeraServer' in token_dict['user_access']['services'])
        self.assertTrue('sites' in token_dict['user_access']['services'][self.test_service_key])
        self.assertTrue('sites' in token_dict['user_access']['services']['OpenTeraServer'])

        user = TeraUser.get_user_by_username(username)
        site_roles = user.get_sites_roles(self.id_test_service)
        self.assertEqual(len(site_roles), len(token_dict['user_access']['services'][self.test_service_key]['sites']))
        for site, role in site_roles.items():
            self.assertTrue([site.id_site, role['site_role']] in
                            token_dict['user_access']['services'][self.test_service_key]['sites'])

        site_roles = user.get_sites_roles()
        self.assertEqual(len(site_roles), len(token_dict['user_access']['services']['OpenTeraServer']['sites']))
        for site, role in site_roles.items():
            self.assertTrue([site.id_site, role['site_role']] in
                            token_dict['user_access']['services']['OpenTeraServer']['sites'])

    def _validate_projects_structure(self, token_dict: dict, username: str):
        self.assertTrue(self.test_service_key in token_dict['user_access']['services'])
        self.assertTrue('OpenTeraServer' in token_dict['user_access']['services'])
        self.assertTrue('projects' in token_dict['user_access']['services'][self.test_service_key])
        self.assertTrue('projects' in token_dict['user_access']['services']['OpenTeraServer'])

        user = TeraUser.get_user_by_username(username)
        proj_roles = user.get_projects_roles(self.id_test_service)
        self.assertEqual(len(proj_roles), len(token_dict['user_access']['services'][self.test_service_key]['projects']))
        for proj, role in proj_roles.items():
            self.assertTrue([proj.id_project, role['project_role']] in
                            token_dict['user_access']['services'][self.test_service_key]['sites'])

        proj_roles = user.get_projects_roles()
        self.assertEqual(len(proj_roles), len(token_dict['user_access']['services']['OpenTeraServer']['projects']))
        for proj, role in proj_roles.items():
            self.assertTrue([proj.id_project, role['project_role']] in
                            token_dict['user_access']['services']['OpenTeraServer']['projects'])
