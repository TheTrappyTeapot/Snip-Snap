from app.db.connection import get_db_connection


def get_barbershops_for_map():
    """Return all barbershops with their barbers for the map page API."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    bs.barbershop_id,
                    bs.name,
                    bs.postcode,
                    bs.location_lat,
                    bs.location_lng,
                    bs.phone,
                    bs.website,
                    b.barber_id,
                    b.average_rating,
                    b.profile_image_url,
                    u.username
                FROM Barbershop bs
                LEFT JOIN Barber b ON b.barbershop_id = bs.barbershop_id
                LEFT JOIN App_User u ON u.user_id = b.user_id
                ORDER BY bs.barbershop_id, b.barber_id
                """
            )
            rows = cur.fetchall()

    shops = {}
    for row in rows:
        bid = row[0]
        if bid not in shops:
            shops[bid] = {
                "barbershop_id": bid,
                "name": row[1],
                "postcode": row[2].strip(),
                "lat": row[3],
                "lng": row[4],
                "phone": row[5],
                "website": row[6],
                "barbers": [],
            }
        if row[7] is not None:
            shops[bid]["barbers"].append(
                {
                    "barber_id": row[7],
                    "average_rating": float(row[8] or 0),
                    "profile_image_url": row[9],
                    "username": row[10],
                }
            )

    return list(shops.values())


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
