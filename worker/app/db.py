import os


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


def connect():
    """Open a Postgres connection.

    TODO: return psycopg.connect(database_url()).
    """
    raise NotImplementedError
