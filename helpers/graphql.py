from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode
from helpers.config import LIVIA_GRAPHQL_ENDPOINT
from typing import Any

transport = RequestsHTTPTransport(
    url = LIVIA_GRAPHQL_ENDPOINT,
    timeout=30,
    retries=2
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=False
)

class LiviaGraphQLError(RuntimeError):
    """Raised when a request to livia fails."""

# variables can be format {str: Any} or it can be None, and if not passed, by default variables is None
def execute_query(query: DocumentNode, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    try: return client.execute(query, variable_values = variables)
    except Exception as error: raise LiviaGraphQLError("The GraphQL request to livia has failed.") from error