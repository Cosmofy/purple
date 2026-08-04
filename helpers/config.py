import os

from dotenv import load_dotenv

load_dotenv()

LIVIA_GRAPHQL_ENDPOINT = os.getenv("LIVIA_GRAPHQL_ENDPOINT")
if not LIVIA_GRAPHQL_ENDPOINT:
    raise RuntimeError("LIVIA_GRAPHQL_ENDPOINT is not set.")
    