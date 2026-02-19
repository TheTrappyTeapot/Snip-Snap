# scripts/init_db.py
"""
Initialises the PostgreSQL schema for this project by applying db.sql.

Design goals:
- No superuser required (does NOT create roles/databases).
- Safe to re-run (db.sql should use IF NOT EXISTS where possible).
- Reads connection from DATABASE_URL in .env / environment.

Usage (Windows PowerShell):
  (.venv) python scripts/init_db.py

Prereqs:
  - PostgreSQL running
  - DATABASE_URL set (e.g. in .env)
  - psycopg + python-dotenv installed
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # handled later

try:
    import psycopg
except ImportError as e:
    raise SystemExit(
        "psycopg is not installed. Run: pip install psycopg[binary] python-dotenv"
    ) from e


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SQL_PATH = REPO_ROOT / "app" / "db" / "db.sql"



def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")


def _split_sql_statements(sql: str) -> List[str]:
    """
    Split SQL script into executable statements.
    Handles:
      - single quotes: '...'
      - double quotes: "..."
      - dollar-quoted strings: $$...$$ or $tag$...$tag$
      - line comments: --
      - block comments: /* ... */

    Skips:
      - psql meta-commands starting with backslash (e.g. \\c, \\i)
      - empty statements

    Note: This is not a full SQL parser, but it is robust enough for typical
    Postgres schema files (CREATE TABLE/INDEX/VIEW/FUNCTION, etc.).
    """
    # Normalise newlines
    s = sql.replace("\r\n", "\n").replace("\r", "\n")

    out: List[str] = []
    buf: List[str] = []

    in_single = False
    in_double = False
    in_line_comment = False
    in_block_comment = False
    dollar_tag: str | None = None

    i = 0
    n = len(s)

    def flush():
        stmt = "".join(buf).strip()
        buf.clear()
        if not stmt:
            return
        # Skip psql meta-commands (start of statement)
        stripped = stmt.lstrip()
        if stripped.startswith("\\"):
            return
        out.append(stmt)

    while i < n:
        ch = s[i]
        nxt = s[i + 1] if i + 1 < n else ""

        # Handle line comments
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                buf.append(ch)
            i += 1
            continue

        # Handle block comments
        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue

        # Start comments (only if not in string/dollar)
        if not in_single and not in_double and dollar_tag is None:
            if ch == "-" and nxt == "-":
                in_line_comment = True
                i += 2
                continue
            if ch == "/" and nxt == "*":
                in_block_comment = True
                i += 2
                continue

        # Dollar-quoted strings
        if not in_single and not in_double:
            if dollar_tag is None and ch == "$":
                # Try to read a tag: $tag$
                j = i + 1
                while j < n and s[j] != "$" and (s[j].isalnum() or s[j] == "_"):
                    j += 1
                if j < n and s[j] == "$":
                    tag = s[i : j + 1]  # includes both $ ... $
                    dollar_tag = tag
                    buf.append(tag)
                    i = j + 1
                    continue
            elif dollar_tag is not None and ch == "$":
                # Try to match closing dollar tag
                if s.startswith(dollar_tag, i):
                    buf.append(dollar_tag)
                    i += len(dollar_tag)
                    dollar_tag = None
                    continue

        # Quoted strings
        if dollar_tag is None:
            if ch == "'" and not in_double:
                # Handle escaped single quote ''
                if in_single and nxt == "'":
                    buf.append("''")
                    i += 2
                    continue
                in_single = not in_single
                buf.append(ch)
                i += 1
                continue
            if ch == '"' and not in_single:
                in_double = not in_double
                buf.append(ch)
                i += 1
                continue

        # Statement terminator ; (only if not inside quotes/comments/dollar)
        if ch == ";" and not in_single and not in_double and dollar_tag is None:
            buf.append(ch)
            i += 1
            flush()
            continue

        buf.append(ch)
        i += 1

    # Flush remainder
    if buf:
        flush()

    return out


def main() -> int:
    if load_dotenv is not None:
        load_dotenv(REPO_ROOT / ".env")

    db_url = os.getenv("DATABASE_URL")
    print("DEBUG DATABASE_URL:", db_url)
    if not db_url:
        print("ERROR: DATABASE_URL is not set.")
        print("Create a .env file in the repo root containing e.g.:")
        print("  DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/snipsnap_db")
        return 2

    sql_path = Path(os.getenv("DB_SQL_PATH", str(DEFAULT_SQL_PATH)))

    try:
        sql_text = _read_text(sql_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 2

    statements = _split_sql_statements(sql_text)
    if not statements:
        print(f"ERROR: No executable SQL statements found in {sql_path}")
        return 2

    print(f"Connecting to DB via DATABASE_URL...")
    print(f"Applying schema from: {sql_path}")
    print(f"Statements to run: {len(statements)}")

    try:
        with psycopg.connect(db_url) as conn:
            # Optional: keep it explicit for schema init
            conn.execute("SET client_min_messages TO WARNING;")

            with conn.cursor() as cur:
                for idx, stmt in enumerate(statements, start=1):
                    try:
                        cur.execute(stmt)
                    except Exception as ex:
                        print("\nERROR while executing statement", idx)
                        print("---- statement start ----")
                        # Print at most first 1000 chars to avoid terminal spam
                        preview = stmt if len(stmt) <= 1000 else (stmt[:1000] + "\n... (truncated)")
                        print(preview)
                        print("---- statement end ----")
                        print(f"\nException: {ex}")
                        conn.rollback()
                        return 1

            conn.commit()

    except Exception as ex:
        print(f"ERROR: Could not connect/apply schema: {ex}")
        return 1

    print("✅ Database schema applied successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
