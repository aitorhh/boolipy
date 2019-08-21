import os
import logging
import sys

logger = logging.getLogger(__name__)

try:
    CALLER_ID=os.environ["CALLER_ID"]
    PRIVATE_KEY=os.environ["PRIVATE_KEY"]
except KeyError as e:
    CALLER_ID=None
    PRIVATE_KEY=None


DEFAULT_LIMIT = 100
