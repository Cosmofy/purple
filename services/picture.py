import re # regex
from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo
from gql import gql
from helpers.graphql import execute_query

def normalize_date(requested_date: str | None) -> str:
    if requested_date is None or not requested_date.strip(): return datetime.now(ZoneInfo("America/Denver")).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", requested_date): raise ValueError("Date must use yyyy-mm-dd format.")
    if date.fromisoformat(requested_date) < date(1995, 6, 16): raise ValueError("APOD began on 1995-06-16.")
    if date.fromisoformat(requested_date) > datetime.now(ZoneInfo("America/Denver")).date(): raise ValueError("Picture date cannot be in the future")
    return requested_date

def get_picture(requested_date: str | None = None) -> dict[str, Any]:
    requested_date = normalize_date(requested_date)
    result = execute_query(
        gql(
            """
            query Picture($date: String!) {
                picture(date: $date) {
                    title
                    date
                    media
                    media_type
                    copyright
                    credit
                    explanation {
                        summarized
                    }
                }
            }
            """
        ),
        {"date": requested_date}
    )

    if not isinstance(result.get("picture"), dict): raise LookupError(f"No picture was found for {requested_date}")
    return result.get("picture")
    