import os
from .auth import *
from .model import *
from .env import JWKS_ENDPOINT

os.environ["NO_PROXY"] = JWKS_ENDPOINT
