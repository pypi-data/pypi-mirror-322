from tests.services.FileTransferService.BaseFileTransferServiceAPITest import BaseFileTransferServiceAPITest
from opentera.db.models.TeraAsset import TeraAsset
from opentera.db.models.TeraUser import TeraUser
from opentera.db.models.TeraParticipant import TeraParticipant
from opentera.db.models.TeraDevice import TeraDevice
from opentera.db.models.TeraService import TeraService
from opentera.services.ServiceAccessManager import ServiceAccessManager


class FileTransferAssetFileTest(BaseFileTransferServiceAPITest):
    test_endpoint = '/api/file/assets'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_endpoint_with_invalid_token(self):
        with self.app_context():
            response = self._get_with_token_auth(self.test_client, token="invalid")
            self.assertEqual(response.status_code, 403)

    def test_post_endpoint_with_invalid_token(self):
        with self.app_context():
            response = self._post_with_token_auth(self.test_client, token="invalid")
            self.assertEqual(response.status_code, 403)

    def test_delete_endpoint_with_invalid_token(self):
        with self.app_context():
            response = self._delete_with_token_auth(self.test_client, token="invalid")
            self.assertEqual(response.status_code, 403)

    def test_get_endpoint_with_user_admin_token_no_params(self):
        with self.app_context():
            user: TeraUser = TeraUser.get_user_by_username('admin')
            self.assertIsNotNone(user)
            admin_token = user.get_token(ServiceAccessManager.api_user_token_key)
            self.assertGreater(len(admin_token), 0)
            response = self._get_with_token_auth(self.test_client, token=admin_token)
            self.assertEqual(response.status_code, 400)

    def test_get_endpoint_with_participant_static_token_no_params(self):
        with self.app_context():
            for participant in TeraParticipant.query.all():
                self.assertIsNotNone(participant)
                if participant.participant_enabled and participant.participant_token:
                    self.assertIsNotNone(participant.participant_token)
                    self.assertGreater(len(participant.participant_token), 0)
                    response = self._get_with_token_auth(self.test_client, token=participant.participant_token)
                    self.assertEqual(response.status_code, 403)

    def test_get_endpoint_with_participant_dynamic_token_no_params(self):
        with self.app_context():
            for participant in TeraParticipant.query.all():
                self.assertIsNotNone(participant)
                if participant.participant_enabled and participant.participant_login_enabled:
                    participant_token = participant.dynamic_token(ServiceAccessManager.api_participant_token_key)
                    self.assertIsNotNone(participant_token)
                    self.assertGreater(len(participant_token), 0)
                    response = self._get_with_token_auth(self.test_client, token=participant_token)
                    self.assertEqual(response.status_code, 400)

    def test_get_endpoint_with_device_static_token_no_params(self):
        with self.app_context():
            for device in TeraDevice.query.all():
                self.assertIsNotNone(device)
                if device.device_enabled:
                    device_token = device.device_token
                    self.assertIsNotNone(device_token)
                    self.assertGreater(len(device_token), 0)
                    response = self._get_with_token_auth(self.test_client, token=device_token)
                    self.assertEqual(response.status_code, 400)

    def test_get_endpoint_with_device_dynamic_token_no_params(self):
        with self.app_context():
            for device in TeraDevice.query.all():
                self.assertIsNotNone(device)
                if device.device_enabled and device.device_onlineable:
                    # Device dynamic tokens not yet available
                    # Result should give status_code of 400
                    pass

    def test_get_endpoint_with_service_token_no_params(self):
        with self.app_context():
            service: TeraService = TeraService.get_service_by_key('FileTransferService')
            self.assertIsNotNone(service)
            service_token = service.get_token(ServiceAccessManager.api_service_token_key)
            self.assertGreater(len(service_token), 0)
            response = self._get_with_token_auth(self.test_client, token=service_token)
            self.assertEqual(response.status_code, 400)

    def test_get_endpoint_with_user_token_as_admin_with_asset_uuid_and_good_access_token(self):
        with self.app_context():
            user: TeraUser = TeraUser.get_user_by_username('admin')
            service = TeraService.get_service_by_key('FileTransferService')
            self.assertIsNotNone(user)
            self.assertIsNotNone(service)
            admin_token = user.get_token(ServiceAccessManager.api_user_token_key)
            self.assertIsNotNone(admin_token)
            self.assertGreater(len(admin_token), 0)

            for asset in TeraAsset.query.all():
                params = {
                    'access_token': TeraAsset.get_access_token([asset.asset_uuid],
                                                               ServiceAccessManager.api_service_token_key,
                                                               user.user_uuid),
                    'asset_uuid': asset.asset_uuid
                }
                response = self._get_with_token_auth(self.test_client, token=admin_token, params=params)

                # Not from FileTransferService ?
                if asset.asset_service_uuid != service.service_uuid:
                    self.assertEqual(response.status_code, 404)
                    continue

                self.assertEqual(response.status_code, 200)

    def test_get_endpoint_with_disabled_token(self):
        with self.app_context():
            login_response = self._get_with_user_http_auth(self.test_client, username='admin',
                                                           password='admin', endpoint=self.user_login_endpoint)
            self.assertEqual(200, login_response.status_code)
            token = login_response.json['user_token']

            logout_response = self._get_with_user_token_auth(self.test_client, token=token,
                                                             endpoint=self.user_logout_endpoint)
            self.assertEqual(200, logout_response.status_code)

            # Try to call endpoint with disabled token
            response = self._get_with_token_auth(self.test_client, token=token)
            self.assertEqual(403, response.status_code)
