import logging
import itertools
import os

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
    HEADERS = {"content-type": "application/vnd.booli-v2+json",
               "User-Agent": "boolipy",
               "Referrer": "github.com/aitorhh/boolipy"}

    def __init__(self):
        self.callerid = settings.CALLER_ID
        self.privatekey = settings.PRIVATE_KEY

    def set_auth(self):
        """ Set the authentification parameters """
        timestamp = str(int(time.time()))
        unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
        hashstr = sha1((self.callerid + timestamp +
                       self.privatekey + unique).encode('utf8')).hexdigest()
        logger.debug("Time from api {}".format(timestamp))

        return {"callerId": self.callerid,
                "time": timestamp,
                "unique": unique,
                "hash": hashstr
               }

    def get(self, endpoint, parameters=None,
            responses_acc=None, auth=None,
            follow=False, cache=True):

        hashstr = self._hash_request(endpoint, parameters, follow)

        filename = os.path.join('data/', hashstr + '.json')
        if cache and os.path.isfile(filename):
            logger.info("Loading request from cache. Filename: {}".format(filename))
            with open(filename, 'r') as f:
                return json.load(f)

        logger.debug("Get endpoint {} with {} and follow pagination: {}".format(repr(endpoint), parameters, follow))
        if responses_acc is None:
            responses_acc = []

        if parameters is None:
            parameters = {"limit": settings.DEFAULT_LIMIT}

        response = self.get_endpoint(endpoint = endpoint,
                                     parameters = parameters,
                                     auth = auth)

        if response.ok:
            dinit = response.json()
            logger.debug(dinit)
            # start acumulating
            responses_acc.append(dinit)

            # deal with pagination
            total_count = dinit.get("totalCount", None)
            limit = dinit.get("limit", None)
            offset = dinit.get("offset", None)

            # stop accumulating when offset > total_count
            if follow and (total_count is not None) and (limit is not None) and (offset+limit) < total_count :
                # keep requesting
                nparams = parameters.copy()
                nparams.update({"offset": limit + offset})
                return self.get(endpoint = endpoint,
                                parameters = nparams,
                                responses_acc = responses_acc,
                                follow = follow)

        fl = self._flattern_responses(endpoint, responses_acc)
        if not cache:
            return fl
        return self._store_cache(endpoint, parameters, follow, fl)

    def _flattern_responses(self, endpoint, responses_acc):
        return list(itertools.chain.from_iterable([d[endpoint] for d in responses_acc]))

    def get_endpoint(self, endpoint, parameters, auth):
        if not auth:
            auth = self.set_auth()
        params = {}
        params.update(parameters)
        params.update(auth)

        url = self.API_ENDPOINT + "/" + endpoint

        logger.debug("Get url: {} with params {}".format(url, params))
        response = requests.get(url, params=params, headers=self.HEADERS)

        if response.ok:
            return response

        logger.error("API error: {}".format(response.content))
        return response

    def _hash_request(self, endpoint, parameters, follow):
        return sha1((endpoint + json.dumps(parameters) + str(follow)).encode('utf8')).hexdigest()

    def _store_cache(self, endpoint, parameters, follow, responses_acc):
        hashstr = self._hash_request(endpoint, parameters, follow)

        if os.path.isdir('data'):
            filename = os.path.join('data/', hashstr + '.json')
            with open(filename, 'w') as f:
                json.dump(responses_acc, f)

        return responses_acc



