import os

from psycopg import connect


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return connect(database_url)

    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "snipsnap"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
