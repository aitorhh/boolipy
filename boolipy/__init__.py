import logging
import argparse
import os

from . import settings
from . import common
from . import api


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description="Access to Booli API")

    ## ACTIONS GROUPS
    actiong = parser.add_mutually_exclusive_group(required=True)
    actiong.add_argument("--test",
                        dest="test",
                        action="store_true",
                        help="test the credentials with CALLER_ID: {id}".format(id=settings.CALLER_ID),
                        default=False)

    actiong.add_argument("--endpoint",
                         dest="endpoint",
                         help="name of the API endpoint. Options: {listings, areas, sold}. For more detail: https://www.booli.se/p/api/referens/")

    ## CONFIGURATION GROUP
    confg = parser.add_argument_group('configuration')
    confg.add_argument("--caller-id",
                        dest="caller_id",
                        default=settings.CALLER_ID,
                        help="CALLER ID obtained contacting booly.se. Set by env variable: {}".format("True" if "CALLER_ID" in os.environ else "False"))

    confg.add_argument("--private-key",
                        dest="private_key",
                        default=settings.PRIVATE_KEY,
                        help="PRIVATE KEY obtained contating booly.se. Set by env variable: {}".format("True" if "PRIVATE_KEY" in os.environ else "False"))


    ## PARAMETERS GROUP
    paramg = parser.add_argument_group('api parameters')
    paramg.add_argument("--center",
                        dest="center",
                        help="If you want to search around a center coordinates. Example: 59.334438, 18.029522")

    paramg.add_argument("--dim",
                        dest="dim",
                        help="If you want to search around a center coordinates this is the dimension of the rectangle around, in meters. Example: 400,500")


    args = parser.parse_args()

    # set the settings from the arguments
    if args.caller_id:
        settings.CALLER_ID = args.caller_id
    if args.private_key:
        settings.PRIVATE_KEY = args.private_key

    if settings.PRIVATE_KEY is None or settings.CALLER_ID is None:
        print(common.PREFIX + common.bcolors.FAIL + " Either PRIVATE KEY or CALLER ID is missing. Please set the environemtnal variable or provide the arguments" + common.bcolors.ENDC)
        return -1

    ### TEST
    ########
    if args.test:
        ret = test()
        if ret < 0:
            print(common.PREFIX + common.bcolors.FAIL + "API test not working" + common.bcolors.ENDC)
        return ret

    ### ENDPOINT
    ############
    if args.endpoint and args.endpoint in api.Api.VALID_ENDPOINTS:
        apiobj = api.Api()
        apiobj.get(endpoint=args.endpoint, parameters={})
    elif args.endpoint:
        print(common.PREFIX + common.bcolors.FAIL + "{} not a valid endpoint".format(repr(args.endpoint)) + common.bcolors.ENDC)
    else:
        ## never should get here since argsparse takes care of it
        print(common.PREFIX + common.bcolors.FAIL + "No action requested".format(repr(args.endpoint)) + common.bcolors.ENDC)
        parser.print_help()



def test(apiobj=None):
    if apiobj is None:
        apiobj = api.Api()
    print(common.PREFIX + "Get endpoints")
    res = apiobj.get_areas(query="kungsholmen")
    if res is None:
        return -1
    res = apiobj.get_listings(query="kungsholmen")
    if res is None:
        return -1


if __name__ == '__main__':
    run()
