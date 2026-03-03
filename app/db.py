import os
import psycopg

def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])

def link_auth_user_id(email: str, auth_user_id: str) -> None:
    """
    Link Supabase auth user UUID to App_User row (only if not already linked).
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE App_User
                SET auth_user_id = %s
                WHERE email = %s
                  AND auth_user_id IS NULL
                """,
                (auth_user_id, email),
            )
        conn.commit()

def get_app_user_by_auth_user_id(auth_user_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id, auth_user_id, email, username, role
                FROM App_User
                WHERE auth_user_id = %s
                """,
                (auth_user_id,),
            )
            row = cur.fetchone()

    if not row:
        return None

    return {
        "user_id": row[0],
        "auth_user_id": row[1],
        "email": row[2],
        "username": row[3],
        "role": row[4],
    }

def get_app_user_by_email(email: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id, auth_user_id, email, username, role
                FROM App_User
                WHERE email = %s
                """,
                (email,),
            )
            row = cur.fetchone()

    if not row:
        return None

    return {
        "user_id": row[0],
        "auth_user_id": row[1],
        "email": row[2],
        "username": row[3],
        "role": row[4],
    }