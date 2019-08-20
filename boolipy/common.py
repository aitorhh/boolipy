import requests
import json
import time
import random
import string

from hashlib import sha1


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PREFIX = bcolors.BOLD + "Boolipy >> " + bcolors.ENDC

def printp(x): print(PREFIX + x)
