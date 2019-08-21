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
    VALID_ENDPOINTS = ["listings", "areas", "sold"]

    def __init__(self):
        self.callerid = settings.CALLER_ID
        self.privatekey = settings.PRIVATE_KEY

    def set_auth(self):
        """ Set the authentification parameters """
        timestamp = str(int(time.time()))
        unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
        hashstr = sha1(self.callerid + timestamp +
                       self.privatekey + unique).hexdigest()
        logger.debug("Time from api {}".format(timestamp))

        return {"callerId": self.callerid,
                "time": timestamp,
                "unique": unique,
                "hash": hashstr
               }

    def get(self, endpoint, parameters=None, responses_acc=None, auth=None):
        logger.debug("Get endpoint {} with {}".format(repr(endpoint), parameters))
        if responses_acc is None:
            responses_acc = []

        if parameters is None:
            parameters = {"limit": settings.DEFAULT_LIMIT}

        response = self.get_endpoint(endpoint = endpoint,
                                     parameters = parameters,
                                     auth = auth)

        if response.ok:
            dinit = response.json()
            # start acumulating
            responses_acc.append(dinit)

            # deal with pagination
            total_count = dinit["total_count"]
            count = dinit["count"]
            offset = dinit["offset"]

            # stop accumulating when offset > total_count
            if offset >= total_count:
                return responses_acc
            else:
                # keep requesting
                nparams = parameters.copy()
                nparams.update({"offset": count})
                return self.get(endpoint = endpoint,
                                parameters = parameters,
                                responses_acc = responses_acc)

        return responses_acc


    def get_endpoint(self, endpoint, parameters, auth):
        if not auth:
            auth = self.set_auth()
        params = {}
        params.update(parameters)
        params.update(auth)

        url = self.API_ENDPOINT + "/" + endpoint

        logger.debug("Get url: {} with params {}".format(url, params))
        response = requests.get(url, params=params)

        if response.ok:
            return response

        logger.error("API error: {}".format(response.content))
        return response

    def get_listings(self, query=None, parameters=None):
        if parameters is None:
            parameters = {}
        if query is not None:
            parameters.update({"q": query})
        return self.get(endpoint='listings',
                        parameters=parameters)

    def get_areas(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        parameters.update({"q": query})
        return self.get(endpoint='areas',
                        parameters=parameters)

    def get_sold(self, parameters=None):
        if parameters is None:
            parameters = {}
        return self.get(endpoint='sold',
                        parameters=parameters)
