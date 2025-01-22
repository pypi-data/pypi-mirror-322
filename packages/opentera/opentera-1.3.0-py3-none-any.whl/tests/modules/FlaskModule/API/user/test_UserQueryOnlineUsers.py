from tests.modules.FlaskModule.API.user.BaseUserAPITest import BaseUserAPITest


class UserQueryOnlineUsersTest(BaseUserAPITest):
    test_endpoint = '/api/user/users/online'

    def test_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.get(self.test_endpoint)
            self.assertEqual(401, response.status_code)

    def test_post_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.post(self.test_endpoint)
            self.assertEqual(405, response.status_code, msg='Method not allowed')

    def test_delete_no_auth(self):
        with self._flask_app.app_context():
            response = self.test_client.delete(self.test_endpoint)
            self.assertEqual(response.status_code, 405, msg='Method not allowed')

    def test_with_admin_auth(self):
        response = self._get_with_user_http_auth(self.test_client, username='admin', password='admin')
        self.assertEqual(response.status_code, 200)

        # Check for important status fields
        for info in response.json:
            self.assertTrue('user_online' in info)
            self.assertTrue('user_busy' in info)
