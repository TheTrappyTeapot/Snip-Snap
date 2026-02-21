from app.db.connection import get_db_connection


def filter_existing_tag_ids(tag_ids):
    if not tag_ids:
        return []

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT tag_id FROM Tag WHERE tag_id = ANY(%s)",
                (tag_ids,),
            )
            return sorted(row[0] for row in cur.fetchall())


def create_haircut_post(barber_id, image_url, width_px, height_px, tag_ids):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO HaircutPhoto (barber_id, image_url, width_px, height_px, status)
                VALUES (%s, %s, %s, %s, 'show')
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

        conn.commit()
        return photo_id
