import logging
import responses
import unittest
import pytest
import mock
import random


logger = logging.getLogger(__name__)


class TestApi:

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.set_references()
        self.patch_time()
        self.patch_settings()

        # repeability
        random.seed(__name__)

        yield
        self.settingspatcher.stop()
        self.timepatcher.stop()

    def patch_settings(self):
        self.settingsmock = mock.Mock(name='settings')
        self.settingsmock.CALLER_ID = self.callerid
        self.settingsmock.PRIVATE_KEY = self.privatekey

        # enable patcher
        self.settingspatcher = mock.patch('boolipy.settings',
                                          self.settingsmock)
        self.settingspatcher.start()

    def patch_time(self):
        self.timemock = mock.Mock(name='time')
        self.timepatcher = mock.patch('boolipy.api.time',
                                          self.timemock)
        self.timepatcher.start()
        self.timemock.time.return_value = self.timeref

    def mock_api(self):
        import boolipy
        apimock = mock.Mock(name='api', spec=boolipy.api.Api)
        apimock.callerid = self.callerid
        apimock.privatekey = self.privatekey
        apimock.API_ENDPOINT = self.apiendpoint

        return apimock

    def set_references(self):
        self.apiendpoint = 'https://api.booli.se'
        self.timeref = 1491633575.83
        self.timerefstr = "1491633575"
        self.callerid = 'my-caller-id'
        self.privatekey = 'my-private-key'
        self.unique = "L5OXU9YZBRR4Y90D"
        self.hashref = "8f485a367b7ae7940709d3cd5cebcba4dde59791"

        self.authdictref = {"callerId": self.callerid,
                            "time": self.timerefstr,
                            "unique": self.unique,
                            "hash": self.hashref}
        self.urlparam = "https://api.booli.se/{endpoint}?q={query}&unique={unique}&hash={hash}&callerId={callerid}&time={time}"
        self.url = "https://api.booli.se/listings?q=nacka&unique={unique}&hash={hash}&callerId={callerid}&time={time}".format(unique=self.unique, hash=self.hashref, callerid=self.callerid, time=self.timerefstr)

    def test_set_auth(self):
        from boolipy.api import Api
        apimock = self.mock_api()
        authdict = Api.set_auth(apimock)
        assert authdict == self.authdictref

    @responses.activate
    def test_get(self):
        from boolipy.api import Api
        apimock = self.mock_api()
        responses.add(responses.GET, self.apiendpoint + "/listings",
                      status=200,
                      body='{}',
                      content_type='application/json')
        response = Api.get(apimock,
                           endpoint='listings',
                           parameters={'q': 'nacka'},
                           auth=self.authdictref)
        assert responses.calls[0].request.url == self.url
        assert response.status_code == 200

    @pytest.mark.parametrize("endpoint,query", [
            ("listings", "nacka"),
            ("areas", "nacka")
    ])
    def test_get_endpoints(self, endpoint, query):
        from boolipy.api import Api
        url = self.urlparam.format(endpoint=endpoint,
                                   query=query,
                                   unique=self.unique,
                                   hash=self.hashref,
                                   callerid=self.callerid,
                                   time=self.timerefstr)
        apimock = self.mock_api()
        get_endpoint = getattr(Api, "get_{}".format(endpoint))
        response = get_endpoint(apimock, query=query)
        apimock.get.assert_called_once_with(endpoint=endpoint,
                                            parameters={"q": query})

    @pytest.mark.skip()
    def test_get_real(self):
        from boolipy import api
        api_obj = api.Api()
        response = api_obj.get(endpoint='listings',
                               parameters={'q': 'nacka'})
        assert response.status_code == 200
