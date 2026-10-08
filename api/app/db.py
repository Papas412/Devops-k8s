import os

import psycopg
from psycopg.rows import dict_row


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


def connect():
    """Open a Postgres connection that returns each row as a dict."""
    return psycopg.connect(database_url(), row_factory=dict_row)
