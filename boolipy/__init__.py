import logging
import argparse
import os

from . import api
from . import settings
from . import common
from .common import printp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description="Access to Booli API",
                                     epilog="For more information about API parameters and endpoints visit https://www.booli.se/p/api")

    ## ACTIONS GROUPS
    actiong = parser.add_mutually_exclusive_group(required=True)
    actiong.add_argument("--test",
                        dest="test",
                        action="store_true",
                        help="test the credentials with CALLER_ID: {id}".format(id=settings.CALLER_ID),
                        default=False)

    actiong.add_argument("--endpoint",
                         dest="endpoint",
                         help="name of the API endpoint. Options: {listings, areas, sold}")

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

    confg.add_argument("--follow",
                        dest="follow",
                        action="store_true",
                        default=False,
                        help="Follow the requests when using pagination")

    confg.add_argument("--no-cache",
                        dest="cache",
                        action="store_false",
                        default=True,
                        help="Use the cache data if available")

    ## PARAMETERS GROUP
    paramg = parser.add_argument_group('api parameters')
    paramg.add_argument("--center",
                        dest="center",
                        help="If you want to search around a center coordinates. Example: 59.334438, 18.029522")

    paramg.add_argument("--dim",
                        dest="dim",
                        help="If you want to search around a center coordinates this is the dimension of the rectangle around, in meters. Example: 400,500")


    args, unknown = parser.parse_known_args()
    keypairs = dict([unknown[i:i+2] for i in range(0, len(unknown), 1) if unknown[i].startswith("--") and not (unknown[i+1:i+2]+["--"])[0].startswith("--")])
    keypairs = {k.replace("--", ""): v for k, v in keypairs.items()}

    flags = [unknown[i] for i in range(0, len(unknown), 2) if (unknown[i+1:i+2]+["--"])[0].startswith("--")]

    # set the settings from the arguments
    if args.caller_id:
        settings.CALLER_ID = args.caller_id
    if args.private_key:
        settings.PRIVATE_KEY = args.private_key

    if settings.PRIVATE_KEY is None or settings.CALLER_ID is None:
        printp(common.bcolors.FAIL + " Either PRIVATE KEY or CALLER ID is missing. Please set the environemtnal variable or provide the arguments" + common.bcolors.ENDC)
        return -1

    printp("Arguments")
    print("\t\t Endpoint: {:<20}".format(repr(args.endpoint)))
    print("\t\t CallerId: {:<20}".format(repr(args.caller_id)))
    print("\t\t Follow: {:<20}".format(repr(args.follow)))
    print("\t\t Center: {:<20}".format(repr(args.center)))
    print("\t\t Dim: {:<20}".format(repr(args.dim)))


    if keypairs:
        printp("Unrecognized arguments (as parameters to requests)")
        for k, v in keypairs.items():
            print("\t\t {}: {:<20}".format(k, repr(v)))


    ### TEST
    ########
    if args.test:
        ret = test(follow=args.follow)
        if ret < 0:
            printp(common.bcolors.FAIL + "API test not working" + common.bcolors.ENDC)
        return ret

    ### ENDPOINT
    ############
    if args.endpoint and args.endpoint in api.Api.VALID_ENDPOINTS:
        apiobj = api.Api()
        # add center and dim to keypairs
        keypairs.update({"center": args.center})
        keypairs.update({"dim": args.dim})
        data = apiobj.get(endpoint=args.endpoint, parameters=keypairs, follow=args.follow)
        print(data)

    elif args.endpoint:
        printp(common.bcolors.FAIL + "{} not a valid endpoint".format(repr(args.endpoint)) + common.bcolors.ENDC)
    else:
        ## never should get here since argsparse takes care of it
        printp(common.bcolors.FAIL + "No action requested".format(repr(args.endpoint)) + common.bcolors.ENDC)
        parser.print_help()



def test(apiobj=None, follow=False):
    if apiobj is None:
        apiobj = api.Api()

    for e in ["areas", "listings", "sold"]:
        printp("Get {}".format(e))
        res = apiobj.get(endpoint=e,
                         parameters={"query": "kungsholmen"},
                         follow=follow)
        if res is None:
            return -1

if __name__ == '__main__':
    run()
