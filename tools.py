from langchain.tools import tool
from services.picture import get_picture

@tool
def tool_get_picture(requested_date: str | None = None) -> dict:
    """ Get an astronomy picture of the day with format yyyy-mm-dd date. Leave requested_date empty for today's picture. Time zone = Mountain Time. """
    return get_picture(requested_date)
    