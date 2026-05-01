"""Database access helpers for Snip-Snap."""

import os
import psycopg2
import psycopg2.extras
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from .supabase_storage import sign_storage_path

load_dotenv()


def _get_conn():
    """Create and return a PostgreSQL connection from DATABASE_URL."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    # Supabase Postgres requires SSL. Enforce if not present in the URL.
    if "sslmode=" not in db_url:
        sep = "&" if "?" in db_url else "?"
        db_url = f"{db_url}{sep}sslmode=require"

    return psycopg2.connect(db_url)


def create_app_user(email: str, username: str, role: str = "customer") -> int:
    """
    Create a new App_User record and return the user_id.
    
    Args:
        email: User's email address
        username: User's username
        role: User's role - 'customer' or 'barber' (default: 'customer')
    """
    email = email.strip().lower()
    role = role.strip().lower()
    
    # Validate role
    if role not in ["customer", "barber"]:
        raise ValueError(f"Invalid role: {role}. Must be 'customer' or 'barber'")
    
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO App_User (email, username, role)
                VALUES (%s, %s, %s)
                RETURNING user_id
                """,
                (email, username, role),
            )
            user_id = cur.fetchone()[0]
        conn.commit()
    return user_id


def link_auth_user_id(email: str, auth_user_id: str) -> bool:
    """
    Link Supabase auth user UUID to App_User row (only if not already linked).
    Returns True if a row was actually updated, False otherwise.
    """
    email = email.strip().lower()
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE App_User
                SET auth_user_id = %s
                WHERE LOWER(email) = %s
                  AND auth_user_id IS NULL
                """,
                (auth_user_id, email),
            )
            rows_updated = cur.rowcount
        conn.commit()
    return rows_updated > 0

def get_app_user_by_auth_user_id(auth_user_id: str):
    """Handles get app user by auth user id."""
    with _get_conn() as conn:
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
    """Handles get app user by email."""
    email = email.strip().lower()
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id, auth_user_id, email, username, role
                FROM App_User
                WHERE LOWER(email) = %s
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

def get_user_promo(user_id: int):
    """Get user profile data for the userPromo component."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    u.username AS name,
                    u.role,
                    pp.image_url AS profile_image_url,
                    bs.name AS barbershop_name
                FROM App_User u
                LEFT JOIN Barber b ON b.user_id = u.user_id
                LEFT JOIN Barbershop bs ON bs.barbershop_id = b.barbershop_id
                LEFT JOIN ProfilePhoto pp ON pp.user_id = u.user_id
                WHERE u.user_id = %s
                LIMIT 1
                """,
                (user_id,),
            )
            row = cur.fetchone()

    if not row:
        return None

    raw_url = row[2]
    image_url = None
    if raw_url:
        image_url = sign_storage_path(raw_url)

    return {
        "name": row[0] or "Unknown",
        "role": row[1] or "",
        "profile_image_url": image_url,
        "barbershop_name": row[3] or "",
    }


def get_barber_public_by_user_id(user_id: int):
    """
    Public barber profile (safe fields only).
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.user_id, u.username, u.location_lat, u.location_lng,
                       u.postcode, u.role,
                       bs.location_lat AS shop_lat, bs.location_lng AS shop_lng, bs.website, bs.postcode AS shop_postcode,
                       b.bio, bs.website AS shop_website, bs.barbershop_id,
                       b.social_links
                FROM App_User u
                LEFT JOIN Barber b ON b.user_id = u.user_id
                LEFT JOIN Barbershop bs ON bs.barbershop_id = b.barbershop_id
                WHERE u.user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()

    if not row:
        return None

    role = (row[5] or "").strip().lower()
    if role != "barber":
        return None

    return {
        "user_id": row[0],
        "username": row[1],
        "location_lat": row[2],
        "location_lng": row[3],
        "postcode": row[4],
        "role": role,
        "shop_lat": row[6],
        "shop_lng": row[7],
        "website": row[8],
        "shop_postcode": row[9],
        "bio": row[10],
        "shop_website": row[11],
        "barbershop_id": row[12],
        "social_links": row[13] or {},
    }


def get_barber_id_from_user_id(user_id: int) -> int | None:
    """
    Get the barber_id for a given user_id.
    
    Args:
        user_id: User ID
        
    Returns:
        Barber ID or None if user is not a barber
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT barber_id FROM Barber WHERE user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()
            return row[0] if row else None


def get_barbershop_by_id(barbershop_id: int):
    """
    Get barbershop details including all barbers working there.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            # Get barbershop info
            cur.execute(
                """
                SELECT barbershop_id, name, postcode, location_lat, location_lng, phone, website
                FROM Barbershop
                WHERE barbershop_id = %s
                """,
                (barbershop_id,),
            )
            shop_row = cur.fetchone()

    if not shop_row:
        return None

    shop = {
        "barbershop_id": shop_row[0],
        "name": shop_row[1],
        "postcode": shop_row[2],
        "location_lat": shop_row[3],
        "location_lng": shop_row[4],
        "phone": shop_row[5],
        "website": shop_row[6],
        "barbers": []
    }

    # Get all barbers at this shop
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.user_id, u.username, u.location_lat, u.location_lng,
                       pp.image_url AS profile_image_url
                FROM Barber b
                LEFT JOIN App_User u ON u.user_id = b.user_id
                LEFT JOIN ProfilePhoto pp ON pp.user_id = u.user_id
                WHERE b.barbershop_id = %s
                ORDER BY u.username
                """,
                (barbershop_id,),
            )
            barber_rows = cur.fetchall()

    barbers = []
    for row in barber_rows:
        promo_data = None
        if row[0]:  # if user_id exists
            user_promo = get_user_promo(row[0])
            if user_promo:
                promo_data = user_promo

        barbers.append({
            "user_id": row[0],
            "username": row[1],
            "location_lat": row[2],
            "location_lng": row[3],
            "promo": promo_data or {
                "name": row[1] or "Unknown",
                "role": "barber",
                "profile_image_url": sign_storage_path(row[4]) if row[4] else None,
                "barbershop_name": shop["name"]
            }
        })

    shop["barbers"] = barbers
    return shop


def get_shifts_for_barber(user_id: int):
    """
    Get all shifts for a barber, ordered by day of week.
    Returns a dict mapping day_of_week to list of shifts.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.shift_id, s.day_of_week, s.start_time, s.end_time
                FROM Shift s
                LEFT JOIN Barber b ON b.barber_id = s.barber_id
                WHERE b.user_id = %s
                ORDER BY s.day_of_week, s.start_time
                """,
                (user_id,),
            )
            rows = cur.fetchall()

    if not rows:
        return {}

    shifts_by_day = {}
    for row in rows:
        day = row[1]
        if day not in shifts_by_day:
            shifts_by_day[day] = []
        
        # Format times
        start_time = row[2]
        end_time = row[3]
        start_str = start_time.strftime("%H:%M") if start_time else ""
        end_str = end_time.strftime("%H:%M") if end_time else ""
        
        shifts_by_day[day].append({
            "shift_id": row[0],
            "start_time": start_str,
            "end_time": end_str
        })

    return shifts_by_day


def add_shift(barber_id: int, day_of_week: int, start_time: str, end_time: str) -> int:
    """Add a shift for a barber. Returns the new shift_id."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Shift (barber_id, day_of_week, start_time, end_time)
                VALUES (%s, %s, %s, %s)
                RETURNING shift_id
                """,
                (barber_id, day_of_week, start_time, end_time),
            )
            shift_id = cur.fetchone()[0]
        conn.commit()
    return shift_id


def delete_shift(shift_id: int, barber_id: int) -> bool:
    """Delete a shift, only if it belongs to the given barber."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Shift WHERE shift_id = %s AND barber_id = %s",
                (shift_id, barber_id),
            )
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def get_shop_opening_hours(barbershop_id: int):
    """
    Get aggregate opening hours for a shop by analyzing all barbers' shifts.
    Returns a dict mapping day_of_week to {open_time, close_time}.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    s.day_of_week,
                    MIN(s.start_time) AS earliest_start,
                    MAX(s.end_time) AS latest_end
                FROM Shift s
                LEFT JOIN Barber b ON b.barber_id = s.barber_id
                WHERE b.barbershop_id = %s
                GROUP BY s.day_of_week
                ORDER BY s.day_of_week
                """,
                (barbershop_id,),
            )
            rows = cur.fetchall()

    if not rows:
        return {}

    hours_by_day = {}
    for row in rows:
        day = row[0]
        open_time = row[1]
        close_time = row[2]
        
        open_str = open_time.strftime("%H:%M") if open_time else ""
        close_str = close_time.strftime("%H:%M") if close_time else ""
        
        hours_by_day[day] = {
            "open": open_str,
            "close": close_str
        }

    return hours_by_day


def update_barber_profile(user_id: int, username: str | None, postcode: str | None, lat, lng) -> None:
    """
    Barber edits their own public profile.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE App_User
                SET
                  username = COALESCE(%s, username),
                  postcode = COALESCE(%s, postcode),
                  location_lat = %s,
                  location_lng = %s
                WHERE user_id = %s
                """,
                (username, postcode, lat, lng, user_id),
            )
        conn.commit()


def update_barber_bio(user_id: int, bio: str | None) -> None:
    """Update the bio for a barber."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE Barber SET bio = %s WHERE user_id = %s",
                (bio, user_id),
            )
        conn.commit()


def update_barbershop_website(user_id: int, website: str | None) -> None:
    """Update the website for the barbershop the barber works at."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Barbershop SET website = %s
                WHERE barbershop_id = (
                    SELECT barbershop_id FROM Barber WHERE user_id = %s
                )
                """,
                (website, user_id),
            )
        conn.commit()


def update_barber_social_links(user_id: int, social_links: dict) -> None:
    """Update the social_links JSON for a barber."""
    import json as _json
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE Barber SET social_links = %s WHERE user_id = %s",
                (_json.dumps(social_links), user_id),
            )
        conn.commit()


def filter_existing_tag_ids(tag_ids: List[int]) -> List[int]:
    """Handles filter existing tag ids."""
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


def create_haircut_post(barber_id: int, image_url: str, width_px: int, height_px: int, tag_ids: List[int], is_post: bool = True):
    """Handles create haircut post."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO HaircutPhoto (barber_id, image_url, width_px, height_px, is_post)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING photo_id
                """,
                (barber_id, image_url, width_px, height_px, is_post),
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

# fetch_discover_posts is a complex query builder for the discover page, supporting multiple optional filters and sorts, and calculating distance and blended scores for ranking.
# It returns a list of haircut posts with associated promo info, ratings, and distance if viewer location is provided.
# It is a very important function for the discover page performance and relevance, and is carefully optimized with conditional joins and where clauses based on the provided filters.
def fetch_discover_posts(
    tag_ids: List[int],
    barber_ids: List[int],
    barbershop_ids: List[int],
    cursor: Optional[Tuple[datetime, int]],
    limit: int,
    effective_sort: str,
    viewer_lat: float | None = None,
    viewer_lng: float | None = None,
    followed: bool = False,
    user_id: Optional[int] = None,
    filter_ids: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """Handles fetch discover posts."""
    where: List[str] = ["hp.is_post = TRUE", "hp.status = 'show'"]
    where_params: List[Any] = []
    select_params: List[Any] = []
    join: List[str] = []
    having: List[str] = []

    # Check if "closest" filter (id=0) is selected
    has_closest_filter = filter_ids and 0 in filter_ids

    # --- Core joins for promo + barbershop coords
    join.append("JOIN barber b_promo ON b_promo.barber_id = hp.barber_id")
    join.append("JOIN app_user u_promo ON u_promo.user_id = b_promo.user_id")
    join.append("LEFT JOIN barbershop bs_promo ON bs_promo.barbershop_id = b_promo.barbershop_id")
    join.append("LEFT JOIN profilephoto pp_promo ON pp_promo.user_id = u_promo.user_id")

    # --- Rating aggregate
    join.append("""
        LEFT JOIN (
            SELECT
                r.target_barber_id AS barber_id,
                AVG(r.rating)::float AS avg_rating,
                COUNT(*)::int AS rating_count
            FROM review r
            WHERE r.status = 'show'
              AND r.rating IS NOT NULL
              AND r.target_barber_id IS NOT NULL
            GROUP BY r.target_barber_id
        ) rating_agg ON rating_agg.barber_id = hp.barber_id
    """)

    # --- Filters
    if followed and user_id is not None:
        print(f"[DB] Filtering for followed barbers - user_id={user_id}")
        join.append("JOIN follow f ON f.barber_id = hp.barber_id")
        where.append("f.user_id = %s")
        where_params.append(user_id)

    if barbershop_ids:
        where.append("b_promo.barbershop_id = ANY(%s)")
        where_params.append(barbershop_ids)

    if barber_ids:
        where.append("hp.barber_id = ANY(%s)")
        where_params.append(barber_ids)

    if tag_ids:
        join.append("JOIN haircutphoto_tag hpt ON hpt.photo_id = hp.photo_id")
        where.append("hpt.tag_id = ANY(%s)")
        where_params.append(tag_ids)
        having.append("COUNT(DISTINCT hpt.tag_id) = %s")
        where_params.append(len(tag_ids))

    if cursor is not None:
        cursor_created_at, cursor_photo_id = cursor
        where.append("(hp.created_at < %s OR (hp.created_at = %s AND hp.photo_id < %s))")
        where_params.extend([cursor_created_at, cursor_created_at, cursor_photo_id])

    # --- Distance
    include_distance = (viewer_lat is not None and viewer_lng is not None)

    distance_expr = "NULL::float"
    distance_score_expr = "0.0::float"

    if include_distance:
        distance_expr = """
        (ST_DistanceSphere(
            ST_MakePoint(bs_promo.location_lng, bs_promo.location_lat),
            ST_MakePoint(%s, %s)
        ) / 1000.0)::float
        """
        # SELECT placeholders come before WHERE placeholders
        select_params.extend([viewer_lng, viewer_lat])
        
        # Only filter out barbers more than 50km away if "closest" filter is explicitly selected
        if has_closest_filter:
            where.append("""
        (ST_DistanceSphere(
            ST_MakePoint(bs_promo.location_lng, bs_promo.location_lat),
            ST_MakePoint(%s, %s)
        ) / 1000.0) <= 50
        """)
            where_params.extend([viewer_lng, viewer_lat])

        distance_score_expr = """
        (1.0 / (1.0 + (
            ST_DistanceSphere(
                ST_MakePoint(bs_promo.location_lng, bs_promo.location_lat),
                ST_MakePoint(%s, %s)
            ) / 1000.0
        )))
        """
        # blended_score uses distance again, so add them again
        select_params.extend([viewer_lng, viewer_lat])

    # --- Scoring
    # For rating: use average rating if available, otherwise use 3.0 (neutral/average)
    rating_score_expr = "COALESCE(rating_agg.avg_rating, 3.0)::float / 5.0"
    recency_score_expr = """
    (1.0 / (1.0 + (EXTRACT(EPOCH FROM (NOW() - hp.created_at)) / 86400.0)))
    """

    # Blended score prioritizes distance heavily (75% for local service),
    # then rating (20%), then recency (5% - minimal impact to favor established barbers)
    blended_score_expr = f"""
    (
        0.75 * ({distance_score_expr}) +
        0.20 * ({rating_score_expr}) +
        0.05 * ({recency_score_expr})
    )::float
    """

    # --- Ordering
    if effective_sort == "closest" and include_distance:
        order_by = "distance_km ASC, hp.created_at DESC, hp.photo_id DESC"
    elif effective_sort == "highest_rated":
        order_by = "rating_agg.avg_rating DESC NULLS LAST, rating_agg.rating_count DESC, hp.created_at DESC, hp.photo_id DESC"
    elif effective_sort == "blended" or (include_distance and effective_sort == "most_recent"):
        # Use blended score when explicitly requested OR when we have location and using default most_recent
        order_by = "blended_score DESC, hp.created_at DESC, hp.photo_id DESC"
    else:
        order_by = "hp.created_at DESC, hp.photo_id DESC"

    having_sql = f"HAVING {' AND '.join(having)}" if having else ""

    sql = f"""
        SELECT
            hp.photo_id,
            hp.image_url,
            hp.width_px,
            hp.height_px,
            hp.created_at,
            hp.barber_id,

            u_promo.user_id AS promo_user_id,
            u_promo.username AS promo_name,
            u_promo.role AS promo_role,
            bs_promo.name AS promo_barbershop_name,
            pp_promo.image_url AS promo_profile_image_url,

            bs_promo.location_lat AS shop_lat,
            bs_promo.location_lng AS shop_lng,

            rating_agg.avg_rating AS avg_rating,
            rating_agg.rating_count AS rating_count,

            {distance_expr} AS distance_km,
            {blended_score_expr} AS blended_score

        FROM haircutphoto hp
        {' '.join(join)}
        WHERE {' AND '.join(where)}
        GROUP BY
            hp.photo_id, hp.image_url, hp.width_px, hp.height_px, hp.created_at, hp.barber_id,
            u_promo.user_id, u_promo.username, u_promo.role, bs_promo.name, pp_promo.image_url,
            bs_promo.location_lat, bs_promo.location_lng,
            rating_agg.avg_rating, rating_agg.rating_count
        {having_sql}
        ORDER BY {order_by}
        LIMIT %s
    """

    params = select_params + where_params + [limit * 150]  # Fetch 150x buffer for 150km filter + diversity filtering

    print(f"[DB] fetch_discover_posts: effective_sort={effective_sort}, include_distance={include_distance}, has_closest_filter={has_closest_filter}, viewer_lat={viewer_lat}, viewer_lng={viewer_lng}, cursor={cursor}, limit={limit}")
    print(f"[DB] where clauses: {where}")
    print(f"[DB] SQL params count: {len(params)}")

    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    print(f"[DB] Fetched {len(rows)} rows from database (requested limit={limit * 10})")

    # --- Diversity filter: limit consecutive posts from same barber
    # This prevents one barber from dominating the entire feed
    # We fetch 50x limit to account for 50km distance filter + diversity filtering reducing result set
    diverse_rows = []
    max_consecutive = 2     # Allow max 2 consecutive posts from same barber to scatter posts better
    last_barber_id = None
    consecutive_count = 0

    for row in rows:
        barber_id = row["barber_id"]
        
        # Check if this is the same barber as the last post
        if barber_id == last_barber_id:
            consecutive_count += 1
        else:
            consecutive_count = 1
            last_barber_id = barber_id
        
        # Allow up to max_consecutive posts from same barber before forcing a different barber
        if consecutive_count <= max_consecutive:
            diverse_rows.append(row)
            
            # Stop once we have enough diverse results (with buffer for pagination)
            if len(diverse_rows) >= limit:
                break

    return diverse_rows[:limit]

def update_user_location(user_id: int, lat: float, lng: float) -> None:
    """Handles update user location."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE App_User SET location_lat = %s, location_lng = %s WHERE user_id = %s",
                (lat, lng, user_id),
            )
        conn.commit()


def get_user_location(user_id: int):
    """Handles get user location."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT location_lat, location_lng, postcode FROM App_User WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
    if not row:
        return None
    lat, lng, postcode = row
    
    # If we have lat/lng, use those
    if lat is not None and lng is not None:
        return {"lat": float(lat), "lng": float(lng)}
    
    # Otherwise, try to convert postcode to coordinates
    if postcode:
        coords = postcode_to_coordinates(postcode.strip())
        if coords:
            return {"lat": float(coords[0]), "lng": float(coords[1])}
    
    return None


def update_user_postcode(user_id: int, postcode: str) -> None:
    """Handles update user postcode."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE App_User SET postcode = %s WHERE user_id = %s",
                (postcode.strip(), user_id),
            )
        conn.commit()

def get_user_postcode(user_id: int):
    """Handles get user postcode."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT postcode FROM App_User WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
    if not row:
        return None
    postcode = row[0]
    if isinstance(postcode, str):
        return postcode.strip()
    return None



def _pick_label(row: Dict[str, Any], preferred_keys: List[str]) -> str:
    """Handles pick label."""
    for k in preferred_keys:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    for k, v in row.items():
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""



def get_barbershops_for_map():
    """Return all barbershops with their barbers for the map page API."""
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
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
                    b.bio,
                    u.user_id,
                    u.username,
                    pp.image_url AS profile_image_url
                FROM Barbershop bs
                LEFT JOIN Barber b ON b.barbershop_id = bs.barbershop_id
                LEFT JOIN App_User u ON u.user_id = b.user_id
                LEFT JOIN ProfilePhoto pp ON pp.user_id = b.user_id
                ORDER BY bs.barbershop_id, b.barber_id
                """
            )
            rows = cur.fetchall()

    shops = {}
    for row in rows:
        bid = row["barbershop_id"]
        if bid not in shops:
            shops[bid] = {
                "barbershop_id": bid,
                "name": row["name"],
                "postcode": row["postcode"].strip(),
                "lat": row["location_lat"],
                "lng": row["location_lng"],
                "phone": row["phone"],
                "website": row["website"],
                "barbers": [],
            }
        if row["barber_id"] is not None:
            shops[bid]["barbers"].append(
                {
                    "barber_id": row["barber_id"],
                    "user_id": row["user_id"],
                    "username": row["username"],
                    "profile_image_url": row["profile_image_url"],
                }
            )

    return list(shops.values())


def fetch_discover_search_items():
    """Handles fetch discover search items."""
    items = [
        {"id": 0, "type": "filter", "label": "Closest"},
        {"id": 1, "type": "filter", "label": "Highest rated"},
        {"id": 2, "type": "filter", "label": "Most recent"},
        {"id": 3, "type": "filter", "label": "Following"}
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


def get_all_barbershops():
    """Get all barbershops for autocomplete in profile."""
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT barbershop_id, name, postcode, location_lat, location_lng
                FROM Barbershop
                ORDER BY name ASC
                """
            )
            rows = cur.fetchall()
    
    return [
        {
            "barbershop_id": row["barbershop_id"],
            "name": row["name"],
            "postcode": row["postcode"].strip() if row["postcode"] else "",
            "location_lat": row["location_lat"],
            "location_lng": row["location_lng"],
        }
        for row in rows
    ]


def get_barber_barbershop(user_id: int):
    """Get the barbershop that a barber works at."""
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT bs.barbershop_id, bs.name, bs.postcode, bs.location_lat, bs.location_lng
                FROM Barber b
                LEFT JOIN Barbershop bs ON bs.barbershop_id = b.barbershop_id
                WHERE b.user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()

    if not row or row["barbershop_id"] is None:
        return None

    return {
        "barbershop_id": row["barbershop_id"],
        "name": row["name"],
        "postcode": row["postcode"].strip() if row["postcode"] else "",
        "location_lat": row["location_lat"],
        "location_lng": row["location_lng"],
    }


def update_user_profile(user_id: int, username: str | None, postcode: str | None, role: str | None, lat: float | None = None, lng: float | None = None) -> None:
    """
    Update user profile (username, postcode, role, and optionally latitude/longitude).
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE App_User
                SET
                  username = COALESCE(%s, username),
                  postcode = COALESCE(%s, postcode),
                  role = COALESCE(%s, role),
                  location_lat = COALESCE(%s, location_lat),
                  location_lng = COALESCE(%s, location_lng)
                WHERE user_id = %s
                """,
                (username, postcode, role, lat, lng, user_id),
            )
        conn.commit()


def create_or_update_barber(user_id: int, barbershop_id: int) -> None:
    """
    Create a barber record if it doesn't exist, or update the barbershop if it does.
    This is used when a barber first picks their shop or changes shops.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            # First, check if barber record exists
            cur.execute("SELECT barber_id FROM Barber WHERE user_id = %s", (user_id,))
            barber_record = cur.fetchone()

            if barber_record:
                # Update existing barber record
                cur.execute(
                    "UPDATE Barber SET barbershop_id = %s WHERE user_id = %s",
                    (barbershop_id, user_id),
                )
            else:
                # Create new barber record
                cur.execute(
                    "INSERT INTO Barber (user_id, barbershop_id) VALUES (%s, %s)",
                    (user_id, barbershop_id),
                )
        conn.commit()


def update_barber_barbershop(user_id: int, barbershop_id: int) -> None:
    """
    Update the barbershop that a barber works at.
    Will create a barber record if it doesn't exist.
    """
    create_or_update_barber(user_id, barbershop_id)



def get_reviews_for_barber(barber_profile_id: int):
    """Fetch all reviews for a specific barber from the database."""
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT r.review_id, r.rating, r.comment, r.created_at, u.username
                FROM Reviews r
                JOIN Users u ON r.customer_user_id = u.user_id
                WHERE r.barber_profile_id = %s
                ORDER BY r.created_at DESC
                """,
                (barber_profile_id,),
            )
            return cur.fetchall()

def submit_barber_review(barber_id: int, customer_id: int, rating: int, comment: str):
    """Insert a new review into the Reviews table."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Reviews (barber_profile_id, customer_user_id, rating, comment)
                VALUES (%s, %s, %s, %s)
                RETURNING review_id
                """,
                (barber_id, customer_id, rating, comment),
            )
            review_id = cur.fetchone()[0]
        conn.commit()
    return review_id


def create_review(user_id: int, target_barber_id: int | None, target_barbershop_id: int | None, text: str, rating: int) -> int:
    """
    Create a new review in the database.
    Returns the review_id.
    """
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")
    
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO review (user_id, target_barber_id, target_barbershop_id, text, rating, status)
                VALUES (%s, %s, %s, %s, %s, 'show')
                RETURNING review_id
                """,
                (user_id, target_barber_id, target_barbershop_id, text, rating),
            )
            review_id = cur.fetchone()[0]
        conn.commit()
    return review_id


def create_review_reply(user_id: int, parent_review_id: int, text: str) -> int:
    """
    Create a reply to a review in the database.
    Returns the review_id of the reply.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            # Get the parent review to determine the target
            cur.execute(
                "SELECT target_barber_id, target_barbershop_id FROM review WHERE review_id = %s",
                (parent_review_id,),
            )
            parent = cur.fetchone()
            if not parent:
                raise ValueError("Parent review not found")
            
            # Create the reply (linked via parent_review_id)
            cur.execute(
                """
                INSERT INTO review (user_id, parent_review_id, target_barber_id, target_barbershop_id, text, status)
                VALUES (%s, %s, %s, %s, %s, 'show')
                RETURNING review_id
                """,
                (user_id, parent_review_id, parent[0], parent[1], text),
            )
            reply_id = cur.fetchone()[0]
        conn.commit()
    return reply_id


def get_helpful_vote_count(review_id: int) -> int:
    """
    Get the number of helpful votes for a review.
    
    Args:
        review_id: Review ID
        
    Returns:
        Number of votes
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM review_helpful_vote WHERE review_id = %s",
                (review_id,),
            )
            count = cur.fetchone()[0]
    return count


def has_user_voted(review_id: int, user_id: int) -> bool:
    """
    Check if a user has already voted on a review.
    
    Args:
        review_id: Review ID
        user_id: User ID
        
    Returns:
        True if user has voted, False otherwise
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM review_helpful_vote WHERE review_id = %s AND user_id = %s",
                (review_id, user_id),
            )
            return cur.fetchone() is not None


def add_helpful_vote(review_id: int, user_id: int) -> bool:
    """
    Add a helpful vote for a review by a user.
    Prevents duplicate votes (one user, one vote per review).
    
    Args:
        review_id: Review ID
        user_id: User ID
        
    Returns:
        True if vote was added, False if already voted
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO review_helpful_vote (review_id, user_id)
                    VALUES (%s, %s)
                    """,
                    (review_id, user_id),
                )
                conn.commit()
                print(f"[ADD_HELPFUL_VOTE] Vote added for review_id={review_id}, user_id={user_id}")
                return True
            except Exception as e:
                conn.rollback()
                print(f"[ADD_HELPFUL_VOTE] Error adding vote: {e}")
                # Check if it's a duplicate vote
                if "duplicate key" in str(e):
                    return False
                raise


def remove_helpful_vote(review_id: int, user_id: int) -> bool:
    """
    Remove a helpful vote for a review by a user.
    
    Args:
        review_id: Review ID
        user_id: User ID
        
    Returns:
        True if vote was removed, False if no vote existed
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM review_helpful_vote WHERE review_id = %s AND user_id = %s",
                (review_id, user_id),
            )
            deleted = cur.rowcount > 0
            conn.commit()
            print(f"[REMOVE_HELPFUL_VOTE] Vote removed for review_id={review_id}, user_id={user_id}: {deleted}")
            return deleted


def get_reviews_with_replies(target_barber_id: int | None = None, target_barbershop_id: int | None = None, current_user_id: int | None = None) -> List[Dict[str, Any]]:
    """
    Fetch all reviews (and their replies) for a barber or barbershop.
    
    Args:
        target_barber_id: Barber ID (if provided, fetches reviews for this barber)
        target_barbershop_id: Barbershop ID (if provided, fetches reviews for this barbershop)
        current_user_id: Current user ID (optional, to check if user has voted)
        
    Returns:
        List of review dicts with structure:
        {
            review_id, user_id, username, rating, text, created_at, status, 
            target_barber_id, target_barbershop_id, target_barber_user_id,
            helpful_vote_count, user_has_voted,
            replies: [{ review_id, user_id, username, text, created_at, helpful_vote_count, user_has_voted }, ...]
        }
    """
    print(f"[GET_REVIEWS_WITH_REPLIES] Called with barber_id={target_barber_id}, barbershop_id={target_barbershop_id}, current_user_id={current_user_id}")
    
    if not target_barber_id and not target_barbershop_id:
        raise ValueError("Either target_barber_id or target_barbershop_id must be provided")
    
    # Ensure current_user_id is an int or None
    if current_user_id and not isinstance(current_user_id, int):
        print(f"[GET_REVIEWS_WITH_REPLIES] Warning: current_user_id is {type(current_user_id)}, expected int")
        current_user_id = None
    
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Build WHERE clause
            where_clause = []
            where_params = []
            
            if target_barber_id:
                where_clause.append("r.target_barber_id = %s")
                where_params.append(target_barber_id)
            if target_barbershop_id:
                where_clause.append("r.target_barbershop_id = %s")
                where_params.append(target_barbershop_id)
            
            where_str = " AND ".join(where_clause)
            
            # Prepare all parameters in correct order: [user_id_for_subquery, ...where_params]
            all_params = [current_user_id if current_user_id else -1] + where_params
            
            query = f"""
                SELECT 
                    r.review_id, 
                    r.user_id, 
                    u.username, 
                    r.rating, 
                    r.text, 
                    r.created_at,
                    r.status,
                    r.target_barber_id,
                    r.target_barbershop_id,
                    b.user_id AS target_barber_user_id,
                    COALESCE(vote_counts.vote_count, 0) AS helpful_vote_count,
                    COALESCE(user_votes.has_voted, FALSE) AS user_has_voted
                FROM review r
                JOIN app_user u ON u.user_id = r.user_id
                LEFT JOIN Barber b ON b.barber_id = r.target_barber_id
                LEFT JOIN (
                    SELECT review_id, COUNT(*) as vote_count
                    FROM review_helpful_vote
                    GROUP BY review_id
                ) vote_counts ON vote_counts.review_id = r.review_id
                LEFT JOIN (
                    SELECT review_id, TRUE as has_voted
                    FROM review_helpful_vote
                    WHERE user_id = %s
                ) user_votes ON user_votes.review_id = r.review_id
                WHERE r.parent_review_id IS NULL AND {where_str} AND r.status = 'show'
                ORDER BY r.created_at DESC
                """
            
            print(f"[GET_REVIEWS_WITH_REPLIES] Executing query with params: {all_params}")
            
            cur.execute(query, all_params)
            parent_reviews = cur.fetchall()
            
            print(f"[GET_REVIEWS_WITH_REPLIES] Found {len(parent_reviews)} parent reviews")
            
            # Fetch replies for each parent review
            for parent in parent_reviews:
                print(f"[GET_REVIEWS_WITH_REPLIES] Fetching replies for review_id={parent['review_id']}")
                reply_params = [current_user_id if current_user_id else -1, parent["review_id"]]
                cur.execute(
                    """
                    SELECT 
                        r.review_id, 
                        r.user_id, 
                        u.username, 
                        r.text, 
                        r.created_at,
                        COALESCE(vote_counts.vote_count, 0) AS helpful_vote_count,
                        COALESCE(user_votes.has_voted, FALSE) AS user_has_voted
                    FROM review r
                    JOIN app_user u ON u.user_id = r.user_id
                    LEFT JOIN (
                        SELECT review_id, COUNT(*) as vote_count
                        FROM review_helpful_vote
                        GROUP BY review_id
                    ) vote_counts ON vote_counts.review_id = r.review_id
                    LEFT JOIN (
                        SELECT review_id, TRUE as has_voted
                        FROM review_helpful_vote
                        WHERE user_id = %s
                    ) user_votes ON user_votes.review_id = r.review_id
                    WHERE r.parent_review_id = %s AND r.status = 'show'
                    ORDER BY r.created_at ASC
                    """,
                    reply_params,
                )
                replies = cur.fetchall()
                parent["replies"] = replies
                print(f"[GET_REVIEWS_WITH_REPLIES] Review {parent['review_id']} has {len(replies)} replies")
    
    print(f"[GET_REVIEWS_WITH_REPLIES] Returning {len(parent_reviews)} reviews")
    return parent_reviews


def postcode_to_coordinates(postcode: str) -> tuple | None:
    """
    Convert UK postcode to latitude/longitude using postcodes.io API.
    
    Args:
        postcode: UK postcode (e.g., "SW1A 1AA")
        
    Returns:
        Tuple (lat, lng) or None if not found
    """
    import requests
    
    try:
        response = requests.get(
            "https://api.postcodes.io/postcodes",
            params={"q": postcode.strip()},
            timeout=10
        )
        
        if not response.ok:
            print(f"[POSTCODE_TO_COORDS] API error (HTTP {response.status_code}) for '{postcode}'")
            return None
        
        data = response.json()
        
        # Check if we got results
        if data.get("status") != 200 or not data.get("result"):
            print(f"[POSTCODE_TO_COORDS] No results found for '{postcode}'")
            return None
        
        # Extract coordinates from first result
        result = data["result"][0]
        lat = result.get("latitude")
        lng = result.get("longitude")
        
        if lat is not None and lng is not None:
            print(f"[POSTCODE_TO_COORDS] {postcode} → ({lat}, {lng})")
            return (lat, lng)
        else:
            print(f"[POSTCODE_TO_COORDS] No coordinates in result for '{postcode}'")
            return None
            
    except requests.RequestException as e:
        print(f"[POSTCODE_TO_COORDS] API error for '{postcode}': {e}")
        return None
    except Exception as e:
        print(f"[POSTCODE_TO_COORDS] Unexpected error for '{postcode}': {e}")
        return None


def create_barbershop(name: str, postcode: str, location_lat: float, location_lng: float) -> int:
    """
    Create a new barbershop in the database.
    
    Args:
        name: Barbershop name
        postcode: UK postcode
        location_lat: Latitude coordinate
        location_lng: Longitude coordinate
        
    Returns:
        barbershop_id of the newly created barbershop
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Barbershop (name, postcode, location_lat, location_lng)
                VALUES (%s, %s, %s, %s)
                RETURNING barbershop_id
                """,
                (name.strip(), postcode.strip(), location_lat, location_lng),
            )
            barbershop_id = cur.fetchone()[0]
        conn.commit()
    return barbershop_id


def follow_barber(user_id: int, barber_id: int) -> bool:
    """
    Add a follow relationship between a user and a barber.
    
    Args:
        user_id: User ID
        barber_id: Barber ID
        
    Returns:
        True if follow was added, False if already following
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO follow (user_id, barber_id)
                    VALUES (%s, %s)
                    """,
                    (user_id, barber_id),
                )
                conn.commit()
                print(f"[FOLLOW] User {user_id} followed barber {barber_id}")
                return True
            except Exception as e:
                conn.rollback()
                print(f"[FOLLOW] Error adding follow: {e}")
                # Check if it's a duplicate follow
                if "duplicate key" in str(e):
                    return False
                raise


def unfollow_barber(user_id: int, barber_id: int) -> bool:
    """
    Remove a follow relationship between a user and a barber.
    
    Args:
        user_id: User ID
        barber_id: Barber ID
        
    Returns:
        True if follow was removed, False if not following
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM follow WHERE user_id = %s AND barber_id = %s",
                (user_id, barber_id),
            )
            deleted = cur.rowcount > 0
            conn.commit()
            print(f"[UNFOLLOW] User {user_id} unfollowed barber {barber_id}: {deleted}")
            return deleted


def is_user_following_barber(user_id: int, barber_id: int) -> bool:
    """
    Check if a user is following a barber.
    
    Args:
        user_id: User ID
        barber_id: Barber ID
        
    Returns:
        True if user is following barber, False otherwise
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM follow WHERE user_id = %s AND barber_id = %s",
                (user_id, barber_id),
            )
            return cur.fetchone() is not None

    print(f"[CREATE_BARBERSHOP] Created barbershop (ID: {barbershop_id}): {name} @ {postcode} ({location_lat}, {location_lng})")
    return barbershop_id


def update_or_create_profile_photo(user_id: int, image_url: str, width_px: int, height_px: int) -> int:
    """
    Create or update a ProfilePhoto record for a user.
    
    Uses PostgreSQL INSERT...ON CONFLICT to handle the UNIQUE constraint on user_id.
    If a record already exists, it updates the image_url, width_px, and height_px.
    
    Args:
        user_id: User ID (must exist in Users table)
        image_url: URL of the profile photo
        width_px: Image width in pixels
        height_px: Image height in pixels
        
    Returns:
        The ProfilePhoto ID
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ProfilePhoto (user_id, image_url, width_px, height_px)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET image_url = EXCLUDED.image_url, width_px = EXCLUDED.width_px, height_px = EXCLUDED.height_px
                RETURNING profile_photo_id
                """,
                (user_id, image_url, width_px, height_px),
            )
            photo_id = cur.fetchone()[0]
        conn.commit()
    
    return photo_id


def get_profile_photo(user_id: int) -> dict | None:
    """
    Fetch the ProfilePhoto record for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Dict with {photo_id, user_id, image_url, width_px, height_px} or None if no photo
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT photo_id, user_id, image_url, width_px, height_px
                FROM ProfilePhoto
                WHERE user_id = %s
                """,
                (user_id,),
            )
            result = cur.fetchone()
            
            if not result:
                return None
            
            return {
                "photo_id": result[0],
                "user_id": result[1],
                "image_url": result[2],
                "width_px": result[3],
                "height_px": result[4],
            }


def get_barber_gallery_photos(barber_id: int, limit: int = 16) -> List[Dict[str, Any]]:
    """
    Fetch haircut photos for a barber that are NOT posts (is_post = false).
    Includes main tag name and barber promo info.
    
    Args:
        barber_id: Barber ID
        limit: Maximum number of photos to return (default 16 for 2-column by 8-row grid)
        
    Returns:
        List of dicts with {photo_id, barber_id, image_url, width_px, height_px, main_tag_name, promo_name, promo_role, promo_barbershop_name, promo_profile_image_url}
    """
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT 
                    hp.photo_id, 
                    hp.barber_id, 
                    hp.image_url, 
                    hp.width_px, 
                    hp.height_px,
                    t.name AS main_tag_name,
                    u.username AS promo_name,
                    u.role AS promo_role,
                    bs.name AS promo_barbershop_name,
                    pp.image_url AS promo_profile_image_url
                FROM HaircutPhoto hp
                LEFT JOIN Tag t ON t.tag_id = hp.main_tag
                JOIN Barber b ON b.barber_id = hp.barber_id
                JOIN App_User u ON u.user_id = b.user_id
                LEFT JOIN Barbershop bs ON bs.barbershop_id = b.barbershop_id
                LEFT JOIN ProfilePhoto pp ON pp.user_id = u.user_id
                WHERE hp.barber_id = %s AND hp.is_post = FALSE AND hp.status = 'show'
                ORDER BY hp.created_at DESC
                LIMIT %s
                """,
                (barber_id, limit),
            )
            return cur.fetchall()


def get_barbershop_gallery_photos(barbershop_id: int, limit: int = 16) -> List[Dict[str, Any]]:
    """
    Fetch haircut photos for all barbers at a barbershop that are NOT posts (is_post = false).
    Includes main tag name and barber promo info.
    
    Args:
        barbershop_id: Barbershop ID
        limit: Maximum number of photos to return (default 16 for 2-column by 8-row grid)
        
    Returns:
        List of dicts with {photo_id, barber_id, image_url, width_px, height_px, main_tag_name, promo_name, promo_role, promo_barbershop_name, promo_profile_image_url}
    """
    with _get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT 
                    hp.photo_id, 
                    hp.barber_id, 
                    hp.image_url, 
                    hp.width_px, 
                    hp.height_px,
                    t.name AS main_tag_name,
                    u.username AS promo_name,
                    u.role AS promo_role,
                    bs.name AS promo_barbershop_name,
                    pp.image_url AS promo_profile_image_url
                FROM HaircutPhoto hp
                LEFT JOIN Tag t ON t.tag_id = hp.main_tag
                JOIN Barber b ON b.barber_id = hp.barber_id
                JOIN App_User u ON u.user_id = b.user_id
                LEFT JOIN Barbershop bs ON bs.barbershop_id = b.barbershop_id
                LEFT JOIN ProfilePhoto pp ON pp.user_id = u.user_id
                WHERE b.barbershop_id = %s AND hp.is_post = FALSE AND hp.status = 'show'
                ORDER BY hp.created_at DESC
                LIMIT %s
                """,
                (barbershop_id, limit),
            )
            return cur.fetchall()
