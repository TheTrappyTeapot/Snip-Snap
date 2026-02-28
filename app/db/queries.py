import os
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

import psycopg2
import psycopg2.extras


def _get_conn():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return psycopg2.connect(db_url)


def filter_existing_tag_ids(tag_ids: List[int]) -> List[int]:
    if not tag_ids:
        return []
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT tag_id FROM Tag WHERE tag_id = ANY(%s)",
                (tag_ids,),
            )
            rows = cur.fetchall()
    return [r[0] for r in rows]


def create_haircut_post(barber_id: int, image_url: str, width_px: int, height_px: int, tag_ids: List[int]):
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO HaircutPhoto (barber_id, image_url, width_px, height_px, is_post)
                VALUES (%s, %s, %s, %s, TRUE)
                RETURNING photo_id
                """,
                (barber_id, image_url, width_px, height_px),
            )
            photo_id = cur.fetchone()[0]

            for tag_id in tag_ids:
                cur.execute(
                    """
                    INSERT INTO HaircutPhoto_Tag (photo_id, tag_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (photo_id, tag_id),
                )
    return photo_id


def fetch_discover_posts(
    tag_ids: List[int],
    barber_ids: List[int],
    barbershop_ids: List[int],
    cursor: Optional[Tuple[datetime, int]],
    limit: int,
    effective_sort: str,
) -> List[Dict[str, Any]]:
    where = ["hp.is_post = TRUE", "hp.status = 'show'"]
    params: List[Any] = []

    join = []
    having = []

    if barbershop_ids:
        join.append("JOIN Barber b ON b.barber_id = hp.barber_id")
        where.append("b.barbershop_id = ANY(%s)")
        params.append(barbershop_ids)

    if barber_ids:
        where.append("hp.barber_id = ANY(%s)")
        params.append(barber_ids)

    if tag_ids:
        join.append("JOIN HaircutPhoto_Tag hpt ON hpt.photo_id = hp.photo_id")
        where.append("hpt.tag_id = ANY(%s)")
        params.append(tag_ids)
        having.append("COUNT(DISTINCT hpt.tag_id) = %s")
        params.append(len(tag_ids))

    if cursor is not None:
        cursor_created_at, cursor_photo_id = cursor
        where.append("(hp.created_at < %s OR (hp.created_at = %s AND hp.photo_id < %s))")
        params.extend([cursor_created_at, cursor_created_at, cursor_photo_id])

    order_by = "hp.created_at DESC, hp.photo_id DESC"

    if effective_sort == "closest":
        order_by = "hp.created_at DESC, hp.photo_id DESC"

    if effective_sort == "highest_rated":
        order_by = "hp.created_at DESC, hp.photo_id DESC"

    having_sql = f"HAVING {' AND '.join(having)}" if having else ""

    sql = f"""
        SELECT hp.photo_id, hp.image_url, hp.width_px, hp.height_px, hp.created_at
        FROM HaircutPhoto hp
        {' '.join(join)}
        WHERE {' AND '.join(where)}
        GROUP BY hp.photo_id
        {having_sql}
        ORDER BY {order_by}
        LIMIT %s
    """
    params.append(limit)

    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    return rows


def _pick_label(row: Dict[str, Any], preferred_keys: List[str]) -> str:
    for k in preferred_keys:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    for k, v in row.items():
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


import psycopg2.extras


def fetch_discover_search_items():
    items = [
        {"id": 0, "type": "filter", "label": "Closest"},
        {"id": 1, "type": "filter", "label": "Highest rated"},
        {"id": 2, "type": "filter", "label": "Most recent"},
    ]

    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT tag_id, name FROM Tag ORDER BY name ASC")
            for r in cur.fetchall():
                items.append({"id": int(r["tag_id"]), "type": "tag", "label": r["name"]})

            cur.execute(
                """
                SELECT b.barber_id, u.username
                FROM Barber b
                JOIN App_User u ON u.user_id = b.user_id
                ORDER BY u.username ASC
                """
            )
            for r in cur.fetchall():
                items.append(
                    {"id": int(r["barber_id"]), "type": "barber", "label": r["username"]}
                )

            cur.execute("SELECT barbershop_id, name FROM Barbershop ORDER BY name ASC")
            for r in cur.fetchall():
                items.append(
                    {"id": int(r["barbershop_id"]), "type": "barbershop", "label": r["name"]}
                )

    return items