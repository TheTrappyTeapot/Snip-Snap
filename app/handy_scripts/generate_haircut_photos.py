"""Module for app/handy_scripts/generate_haircut_photos.py."""

import os
import random
from datetime import datetime, timedelta
from supabase import create_client
from dotenv import load_dotenv
import psycopg2
from ..db import _get_conn
load_dotenv()

POST_PHOTOS_PER_BARBER = 10
NON_POST_PHOTOS_PER_BARBER = 8
TAG_ID_MIN = 1
TAG_ID_MAX = 20
HIDDEN_RATIO = 0.10


# Spread timestamps over the last 180 days.
MAX_AGE_DAYS = 180


def get_storage_image_pool():
    """Handles get storage image pool."""
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

    sb = create_client(url, key)

    res = sb.storage.from_("photos").list("haircuts")

    if not res:
        raise RuntimeError("No files found in photos/haircuts")

    paths = []
    for item in res:
        name = item.get("name")
        if not name:
            continue
        paths.append(f"haircuts/{name}")

    if not paths:
        raise RuntimeError("No usable image paths found in photos/haircuts")

    return paths


def random_timestamp() -> datetime:
    """Handles random timestamp."""
    now = datetime.now()
    delta = timedelta(
        days=random.randint(0, MAX_AGE_DAYS),
        seconds=random.randint(0, 24 * 60 * 60 - 1),
    )
    return now - delta


def choose_status() -> str:
    """Handles choose status."""
    return "hide" if random.random() < HIDDEN_RATIO else "show"


def choose_dimensions() -> tuple[int, int]:
    """Handles choose dimensions."""
    # Mostly portrait/square social-style images
    options = [
        (1080, 1080),
        (1080, 1350),
        (1200, 1200),
        (1080, 1440),
        (1440, 1440),
    ]
    return random.choice(options)


def choose_tags() -> list[int]:
    """Handles choose tags."""
    # 1 to 5 tags per photo, no duplicates
    tag_count = random.randint(1, 5)
    return random.sample(range(TAG_ID_MIN, TAG_ID_MAX + 1), k=tag_count)


def main() -> None:
    """Handles main."""
    conn = _get_conn()
    conn.autocommit = False


    STORAGE_IMAGE_POOL = get_storage_image_pool()
    print(f"Loaded {len(STORAGE_IMAGE_POOL)} storage images from photos/haircuts")

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT barber_id FROM barber ORDER BY barber_id ASC")
            barber_rows = cur.fetchall()

            if not barber_rows:
                raise RuntimeError("No barbers found in barber table")

            barber_ids = [row[0] for row in barber_rows]

            photo_insert_sql = """
                INSERT INTO haircutphoto (
                    barber_id,
                    image_url,
                    width_px,
                    height_px,
                    status,
                    main_tag,
                    is_post,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING photo_id
            """

            tag_insert_sql = """
                INSERT INTO haircutphoto_tag (photo_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """

            total_photos = 0
            total_tag_links = 0

            for barber_id in barber_ids:
                # Generate 10 post photos and 8 non-post photos for this barber
                photo_configs = (
                    [(True, barber_id) for _ in range(POST_PHOTOS_PER_BARBER)] +
                    [(False, barber_id) for _ in range(NON_POST_PHOTOS_PER_BARBER)]
                )
                
                for is_post, current_barber_id in photo_configs:
                    image_path = random.choice(STORAGE_IMAGE_POOL)
                    width_px, height_px = choose_dimensions()
                    status = choose_status()
                    created_at = random_timestamp()
                    tag_ids = choose_tags()
                    main_tag = random.choice(tag_ids)

                    cur.execute(
                        photo_insert_sql,
                        (
                            current_barber_id,
                            image_path,
                            width_px,
                            height_px,
                            status,
                            main_tag,
                            is_post,
                            created_at,
                        ),
                    )
                    photo_id = cur.fetchone()[0]
                    total_photos += 1

                    for tag_id in tag_ids:
                        cur.execute(tag_insert_sql, (photo_id, tag_id))
                        total_tag_links += 1

        conn.commit()
        print(f"Inserted {total_photos} haircutphoto rows")
        print(f"Inserted {total_tag_links} haircutphoto_tag rows")
        print(f"Barbers covered: {len(barber_ids)}")
        print(f"Photos per barber: {POST_PHOTOS_PER_BARBER} post + {NON_POST_PHOTOS_PER_BARBER} non-post = {POST_PHOTOS_PER_BARBER + NON_POST_PHOTOS_PER_BARBER}")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
