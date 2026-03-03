# scripts/nuke_db.py
"""
DANGER: Deletes ALL objects in the target database schema.

Drops and recreates the public schema in the database pointed to by DATABASE_URL.

Usage:
  (.venv) python scripts/nuke_db.py

This is irreversible.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

import psycopg


REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    if load_dotenv is not None:
        load_dotenv(REPO_ROOT / ".env")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL is not set.")
        return 2

    # WARNING message with database details for confirmation
    parsed = urlparse(db_url)
    db_name = parsed.path.lstrip("/") or "(unknown)"
    host = parsed.hostname or "(unknown)"
    port = parsed.port or "(default)"

    print("⚠️  YOU ARE ABOUT TO DELETE ALL DATA IN:")
    print(f"    database: {db_name}")
    print(f"    host: {host}:{port}")
    print()

    confirm = input("Type 'NUKE' to continue: ").strip()
    if confirm != "NUKE":
        print("Aborted.")
        return 1

    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP SCHEMA IF EXISTS public CASCADE;")
                cur.execute("CREATE SCHEMA public;")
                cur.execute("GRANT ALL ON SCHEMA public TO PUBLIC;")
                cur.execute("GRANT ALL ON SCHEMA public TO CURRENT_USER;")
            conn.commit()
    except Exception as ex:
        print(f"ERROR: {ex}")
        return 1

    print("💥 Database schema nuked successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())