import os

JWKS_ENDPOINT = os.getenv("JWKS_ENDPOINT")
JWT_ALGORITHM = "RS256"
HOST_RESOURCE_APP = os.getenv("HOST_RESOURCE_APP")

if JWKS_ENDPOINT is None:
    raise Exception("環境変数 JWKS_ENDPOINT は必須です。")

if HOST_RESOURCE_APP is None:
    raise Exception("環境変数 HOST_RESOURCE_APP は必須です。")

JWT_AUDIENCE = [HOST_RESOURCE_APP]
