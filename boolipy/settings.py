import os

try:
    CALLER_ID = os.environ["CALLER_ID"]
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]
except KeyError as e:
    error("boolipy requires CALLER_ID and PRIVATE_KEY from the environment")
