import os
import logging

logger = logging.getLogger(__name__)

CALLER_ID = "not set"
PRIVATE_KEY = "not set"
try:
    CALLER_ID = os.environ["CALLER_ID"]
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]
except KeyError as e:
    logger.error("boolipy requires CALLER_ID and PRIVATE_KEY from the environment")
