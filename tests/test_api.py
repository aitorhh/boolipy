import logging
import unittest
import mock

from boolipy import api

logger = logging.getLogger(__name__)


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.settingsmock = mock.Mock(name='settings')
        self.settingsmock.CALLER_ID = 'my-caller-id'
        self.settingsmock.PRIVATE_KEY = 'my-private-key'

        # enable patcher
        self.settingspatcher = mock.patch('boolipy.settings', 
                                          self.settingsmock)
        self.settingspatcher.start()


    def tearDown(self):
        self.settingspatcher.stop()

    def test_set_auth(self):
        pass

    def test_get(self):
        pass

    def test_get_real(self):
        api_obj = api.Api()
        response = api_obj.get(endpoint='listings',
                               parameters={'q': 'nacka'})
        assert response.status_code == 200
