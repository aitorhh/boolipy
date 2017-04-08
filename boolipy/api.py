import logging

from . import settings

# all dependencies are at .common
from .common import requests
from .common import json
from .common import time
from .common import random
from .common import sha1
from .common import string

logger = logging.getLogger(__name__)


class Api():
    API_ENDPOINT = 'https://api.booli.se'

    def __init__(self):
        self.callerid = settings.CALLER_ID
        self.privatekey = settings.PRIVATE_KEY

    def set_auth(self):
        """ Set the authentification parameters """
        timestamp = str(int(time.time()))
        unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
        hashstr = sha1(self.callerid + timestamp +
                       self.privatekey + unique).hexdigest()
        logger.debug("Time from api {}".format(time.time()))

        return {"callerId": self.callerid,
                "time": timestamp,
                "unique": unique,
                "hash": hashstr
               }

    def get(self, endpoint, parameters, auth=None):
        if not auth:
            auth = self.set_auth()
        params = {}
        params.update(parameters)
        params.update(auth)

        url = self.API_ENDPOINT + "/" + endpoint

        logger.debug("Get url: {} with params {}".format(url, params))
        response = requests.get(url, params=params)

        return response

    def get_listings(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        parameters.update({"q": query})
        return self.get(endpoint='listings',
                        parameters=parameters)

    def get_areas(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        parameters.update({"q": query})
        return self.get(endpoint='areas',
                        parameters=parameters)
