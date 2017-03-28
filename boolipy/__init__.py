import logging

from . import settings
from . import common
from . import api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def usage():
    print("BooliPy >> Access to Booli API with CALLER_ID={id}".format(id=settings.CALLER_ID))


def main():
    #FIXME: use command line options
    usage()


if __name__ == '__main__':
    main()
