"""Module for app/api.py."""

from datetime import datetime
from flask import Blueprint, request, jsonify, session

from .db import (
    fetch_discover_posts, 
    fetch_discover_search_items, 
    get_user_location, 
    get_barbershops_for_map, 
    create_app_user, 
    update_user_location,
    get_all_barbershops,
    get_barber_barbershop,
    update_user_profile,
    update_barber_barbershop,
    create_haircut_post,
    postcode_to_coordinates,
    create_barbershop,
    update_or_create_profile_photo,
    create_review,
    create_review_reply,
    get_reviews_with_replies,
    add_helpful_vote,
    remove_helpful_vote,
    get_helpful_vote_count,
)
from .input_sanitization import sanitize_input
from .supabase_storage import sign_storage_path, upload_photo_to_storage

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.post("/auth/create-user")
def create_user():
    """Create a new App_User record for signup."""
    try:
        import re
        data = request.get_json(silent=True) or {}
        email = data.get("email", "").strip().lower()
        username = data.get("username", "").strip()
        role = data.get("role", "customer").strip().lower()

        print(f"[CREATE_USER] Received request: email={email}, username={username}, role={role}")

        if not email or not username:
            print(f"[CREATE_USER] Validation failed: missing email or username")
            return jsonify({"ok": False, "error": "Email and username required"}), 400

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return jsonify({"ok": False, "error": "Invalid email address"}), 400

        if len(username) > 50:
            return jsonify({"ok": False, "error": "Username must be 50 characters or fewer"}), 400

        if len(username) < 2:
            return jsonify({"ok": False, "error": "Username must be at least 2 characters"}), 400

        err = sanitize_input(username)
        if err:
            return jsonify({"ok": False, "error": err}), 400

        # Validate role
        if role not in ["customer", "barber"]:
            print(f"[CREATE_USER] Invalid role: {role}")
            return jsonify({"ok": False, "error": "Invalid account type. Must be 'customer' or 'barber'"}), 400
        
        print(f"[CREATE_USER] Creating user in database...")
        user_id = create_app_user(email, username, role)
        print(f"[CREATE_USER] User created successfully with user_id={user_id}")
        return jsonify({"ok": True, "user_id": user_id}), 201
    except Exception as e:
        error_msg = str(e)
        print(f"[CREATE_USER] Error creating app user: {error_msg}")
        
        # Check if it's a duplicate email error
        if "duplicate key" in error_msg.lower() and "email" in error_msg.lower():
            print(f"[CREATE_USER] Duplicate email detected")
            return jsonify({"ok": False, "error": "Email already in use"}), 400
        
        return jsonify({"ok": False, "error": error_msg}), 500


@api_bp.get("/barbershops")
def barbershops():
    """Handles barbershops."""
    try:
        shops = get_barbershops_for_map()
        return jsonify(shops)
    except Exception:
        return jsonify({"error": "Could not load barbershops"}), 500


@api_bp.post("/user/location")
def save_user_location():
    """Handles save user location."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    lat = data.get("lat")
    lng = data.get("lng")
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng required"}), 400
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        return jsonify({"error": "lat and lng must be numbers"}), 400
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        return jsonify({"error": "Coordinates out of range"}), 400
    update_user_location(int(u["id"]), lat, lng)
    return jsonify({"ok": True})


@api_bp.get("/discover/search_items")
def discover_search_items():
    """Handles discover search items."""
    items = fetch_discover_search_items()
    return jsonify({"items": items})


def _parse_cursor(cursor_value: str):
    """
    Expects cursor like: "2026-03-04T16:32:36.123456Z|123"
    Returns (datetime, int) or None
    """
    if not cursor_value:
        return None
    try:
        created_at_s, photo_id_s = cursor_value.split("|", 1)
        # Accept Z or no Z
        created_at_s = created_at_s.replace("Z", "")
        dt = datetime.fromisoformat(created_at_s)
        return (dt, int(photo_id_s))
    except Exception:
        return None


def _make_next_cursor(items):
    """
    items from fetch_discover_posts are RealDictCursor dicts containing
    created_at + photo_id.
    """
    if not items:
        return None
    last = items[-1]
    created_at = last.get("created_at")
    photo_id = last.get("photo_id")
    if not created_at or photo_id is None:
        return None
    # created_at is already a datetime from psycopg2
    return f"{created_at.isoformat()}Z|{int(photo_id)}"


@api_bp.post("/gallery/posts")
def gallery_posts():
    """Handles gallery posts."""
    payload = request.get_json(silent=True) or {}

    ALLOWED_SORTS = {"most_recent", "nearest", "highest_rated"}

    raw_tag_ids = payload.get("tag_ids") or []
    raw_barber_ids = payload.get("barber_ids") or []
    raw_barbershop_ids = payload.get("barbershop_ids") or []

    try:
        tag_ids = [int(x) for x in raw_tag_ids if str(x).lstrip("-").isdigit()]
        barber_ids = [int(x) for x in raw_barber_ids if str(x).lstrip("-").isdigit()]
        barbershop_ids = [int(x) for x in raw_barbershop_ids if str(x).lstrip("-").isdigit()]
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid filter values"}), 400

    effective_sort = (payload.get("effective_sort") or "most_recent").strip().lower()
    if effective_sort not in ALLOWED_SORTS:
        effective_sort = "most_recent"

    try:
        limit = max(1, min(int(payload.get("limit") or 18), 100))
    except (TypeError, ValueError):
        limit = 18

    cursor_raw = payload.get("cursor")
    cursor = _parse_cursor(cursor_raw) if isinstance(cursor_raw, str) else None

    # --- viewer location (customer OR barber) ---
    u = session.get("user") or {}
    uid = u.get("id")

    viewer_lat = None
    viewer_lng = None

    if uid is not None:
        loc = get_user_location(int(uid))  # returns {"lat": float, "lng": float} or None
        if loc:
            viewer_lat = loc["lat"]
            viewer_lng = loc["lng"]

    # Determine actual sort being used
    actual_sort = effective_sort
    if effective_sort == "most_recent" and viewer_lat is not None and viewer_lng is not None:
        actual_sort = "blended"

    # Fetch 1 extra so we can calculate has_more
    rows = fetch_discover_posts(
        tag_ids=tag_ids,
        barber_ids=barber_ids,
        barbershop_ids=barbershop_ids,
        cursor=cursor,
        limit=limit + 1,
        effective_sort=effective_sort,
        viewer_lat=viewer_lat,
        viewer_lng=viewer_lng,
    )

    # For pagination: set has_more=true if we got a full page of results
    # The cursor will naturally handle termination when no more posts exist
    # This is better than requiring len(rows) > limit, which breaks when diversity/distance filters limit results
    has_more = len(rows) >= limit
    items = rows[:limit]
    
    for it in items:
        # Haircut photo
        it["image_url"] = sign_storage_path(it.get("image_url"), expires_in=3600)

        # Promo profile photo (optional)
        it["promo_profile_image_url"] = sign_storage_path(
            it.get("promo_profile_image_url"), expires_in=3600
        )

    next_cursor = _make_next_cursor(items) if has_more else None

    return jsonify(
        {
            "items": items,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }
    )


@api_bp.post("/user/profile")
def update_profile():
    """Update user profile (username, location, role, latitude, longitude, and barbershop for barbers)."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401

    user_id = int(u["id"])
    current_role = u.get("role", "customer")

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    location = data.get("location", "").strip() if data.get("location") else None
    role = data.get("role", "").strip().lower()
    barbershop_id = data.get("barbershop_id")
    lat = data.get("lat")
    lng = data.get("lng")

    # Validation
    if not username:
        return jsonify({"ok": False, "error": "Username is required"}), 400

    if len(username) < 2 or len(username) > 50:
        return jsonify({"ok": False, "error": "Username must be 2-50 characters"}), 400

    err = sanitize_input(username)
    if err:
        return jsonify({"ok": False, "error": err}), 400

    if not role or role not in ["customer", "barber"]:
        return jsonify({"ok": False, "error": "Invalid role"}), 400

    if location and len(location) > 10:
        return jsonify({"ok": False, "error": "Location must be 10 characters or fewer"}), 400

    # Validate latitude/longitude if provided
    if lat is not None:
        try:
            lat = float(lat)
            if not (-90 <= lat <= 90):
                return jsonify({"ok": False, "error": "Latitude must be between -90 and 90"}), 400
        except (TypeError, ValueError):
            return jsonify({"ok": False, "error": "Latitude must be a valid number"}), 400

    if lng is not None:
        try:
            lng = float(lng)
            if not (-180 <= lng <= 180):
                return jsonify({"ok": False, "error": "Longitude must be between -180 and 180"}), 400
        except (TypeError, ValueError):
            return jsonify({"ok": False, "error": "Longitude must be a valid number"}), 400

    # For barbers, barbershop is required
    if role == "barber" and (barbershop_id is None or not isinstance(barbershop_id, int)):
        return jsonify({"ok": False, "error": "Barbershop ID is required for barbers"}), 400

    try:
        # Update user profile with location coordinates
        update_user_profile(user_id, username, location, role, lat, lng)
        print(f"[PROFILE_UPDATE] Updated user {user_id}: username={username}, role={role}, lat={lat}, lng={lng}")

        # If barber, update barbershop
        if role == "barber":
            try:
                update_barber_barbershop(user_id, barbershop_id)
                print(f"[PROFILE_UPDATE] Updated barber {user_id}: barbershop_id={barbershop_id}")
            except Exception as e:
                print(f"[PROFILE_UPDATE] Error updating barbershop: {e}")
                return jsonify({"ok": False, "error": f"Error updating barbershop: {str(e)}"}), 500

        # Update session
        session["user"]["username"] = username
        session["user"]["role"] = role
        session.modified = True

        return jsonify({"ok": True}), 200

    except Exception as e:
        error_msg = str(e)
        print(f"[PROFILE_UPDATE] Error: {error_msg}")
        
        if "duplicate" in error_msg.lower() and "username" in error_msg.lower():
            return jsonify({"ok": False, "error": "Username already in use"}), 400

        return jsonify({"ok": False, "error": error_msg}), 500


@api_bp.get("/user/barbershops")
def get_barbershops():
    """Get all barbershops for autocomplete in profile."""
    try:
        barbershops = get_all_barbershops()
        return jsonify({"barbershops": barbershops}), 200
    except Exception as e:
        print(f"[GET_BARBERSHOPS] Error: {e}")
        return jsonify({"error": "Could not load barbershops"}), 500


@api_bp.get("/user/current-barbershop")
def get_current_barbershop():
    """Get the current barber's barbershop."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401

    user_id = int(u["id"])
    current_role = u.get("role", "customer")

    if current_role != "barber":
        return jsonify({"ok": False, "error": "Only barbers have a barbershop"}), 400

    try:
        barbershop = get_barber_barbershop(user_id)
        if not barbershop:
            return jsonify({"ok": False, "error": "Barber barbershop not found"}), 404
        
        return jsonify({"barbershop": barbershop}), 200
    except Exception as e:
        print(f"[GET_CURRENT_BARBERSHOP] Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


@api_bp.post("/barbershops/create")
def create_new_barbershop():
    """Create a new barbershop and optionally assign it to the current barber."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401

    user_id = int(u["id"])
    current_role = u.get("role", "customer")

    if current_role != "barber":
        return jsonify({"ok": False, "error": "Only barbers can create barbershops"}), 403

    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    postcode = data.get("postcode", "").strip()
    auto_assign = data.get("auto_assign", True)  # Whether to assign to current barber

    # Validation
    if not name:
        return jsonify({"ok": False, "error": "Barbershop name is required"}), 400

    if len(name) > 255:
        return jsonify({"ok": False, "error": "Barbershop name too long (max 255 characters)"}), 400

    if not postcode:
        return jsonify({"ok": False, "error": "Postcode is required"}), 400

    if len(postcode) > 10:
        return jsonify({"ok": False, "error": "Postcode too long"}), 400

    # Sanitize name
    err = sanitize_input(name)
    if err:
        return jsonify({"ok": False, "error": err}), 400

    try:
        # Convert postcode to coordinates
        print(f"[CREATE_BARBERSHOP] Converting postcode '{postcode}' to coordinates...")
        coords = postcode_to_coordinates(postcode)
        
        if not coords:
            return jsonify({"ok": False, "error": f"Could not find coordinates for postcode '{postcode}'. Please check the postcode is correct."}), 400
        
        lat, lng = coords
        
        # Create barbershop
        print(f"[CREATE_BARBERSHOP] Creating barbershop: {name} @ {postcode}")
        barbershop_id = create_barbershop(name, postcode, lat, lng)
        
        # Optionally assign to current barber
        if auto_assign:
            print(f"[CREATE_BARBERSHOP] Assigning barbershop {barbershop_id} to barber {user_id}")
            update_barber_barbershop(user_id, barbershop_id)
        
        return jsonify({
            "ok": True,
            "barbershop_id": barbershop_id,
            "name": name,
            "postcode": postcode,
            "location_lat": lat,
            "location_lng": lng
        }), 201

    except Exception as e:
        error_msg = str(e)
        print(f"[CREATE_BARBERSHOP] Error: {error_msg}")
        return jsonify({"ok": False, "error": f"Error creating barbershop: {error_msg}"}), 500


@api_bp.post("/user/profile-photo")
def upload_profile_photo():
    """Upload a profile photo for the current user."""
    print("[UPLOAD_PROFILE_PHOTO] Starting upload")
    
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401
    
    user_id = int(u["id"])
    
    # Get barber_id if user is a barber
    from .db import _get_conn
    barber_id = None
    
    current_role = u.get("role", "customer")
    if current_role == "barber":
        try:
            with _get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT barber_id FROM Barber WHERE user_id = %s", (user_id,))
                    result = cur.fetchone()
                    if result:
                        barber_id = result[0]
        except Exception as e:
            print(f"[UPLOAD_PROFILE_PHOTO] Error getting barber_id: {e}")
    
    # If not a barber or no barber record, use user_id as fallback
    if not barber_id:
        barber_id = user_id
    
    # Get file from request
    file = request.files.get("photo")
    if not file or file.filename == "":
        return jsonify({"ok": False, "error": "No photo provided"}), 400
    
    print(f"[UPLOAD_PROFILE_PHOTO] File received: {file.filename}")
    
    # Validate file type
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
    file_ext = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else ""
    
    if file_ext not in ALLOWED_EXTENSIONS:
        return jsonify({"ok": False, "error": "File type not allowed. Use jpg, jpeg, png, gif, or webp"}), 400
    
    try:
        # Read file
        file_data = file.read()
        
        # Get image dimensions
        from PIL import Image
        import io
        
        img = Image.open(io.BytesIO(file_data))
        width_px, height_px = img.size
        print(f"[UPLOAD_PROFILE_PHOTO] Image dimensions: {width_px}x{height_px}")
        
        # Upload to Supabase storage
        print(f"[UPLOAD_PROFILE_PHOTO] Uploading to storage (barber_id: {barber_id})")
        storage_path = upload_photo_to_storage(barber_id, file_data, file.filename)
        
        if not storage_path:
            return jsonify({"ok": False, "error": "Failed to upload photo to storage"}), 500
        
        print(f"[UPLOAD_PROFILE_PHOTO] Uploaded to: {storage_path}")
        
        # Get signed URL
        signed_url = sign_storage_path(storage_path, expires_in=3600)
        
        print(f"[UPLOAD_PROFILE_PHOTO] Signed URL: {signed_url}")
        
        if not signed_url:
            return jsonify({"ok": False, "error": "Failed to generate signed URL"}), 500
        
        # Update or create ProfilePhoto database record
        try:
            photo_id = update_or_create_profile_photo(user_id, storage_path, width_px, height_px)
            print(f"[UPLOAD_PROFILE_PHOTO] Updated ProfilePhoto record (photo_id: {photo_id})")
        except Exception as e:
            print(f"[UPLOAD_PROFILE_PHOTO] Warning: Failed to update ProfilePhoto record: {e}")
            # Still return success to user - photo is in storage, database is non-critical
        
        return jsonify({
            "ok": True,
            "image_url": signed_url,
            "filename": file.filename,
            "width": width_px,
            "height": height_px
        }), 201
    
    except Exception as e:
        error_msg = str(e)
        print(f"[UPLOAD_PROFILE_PHOTO] Error: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"Error uploading photo: {error_msg}"}), 500


@api_bp.post("/photos/upload")
def upload_photo():
    """Upload a photo post. Only barbers can upload."""
    print("[UPLOAD_PHOTO] Starting upload_photo request")
    print(f"[UPLOAD_PHOTO] Request method: {request.method}")
    print(f"[UPLOAD_PHOTO] Request content-type: {request.content_type}")
    print(f"[UPLOAD_PHOTO] Request files keys: {list(request.files.keys())}")
    print(f"[UPLOAD_PHOTO] Request form keys: {list(request.form.keys())}")
    
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401
    
    user_id = int(u["id"])
    role = u.get("role", "customer")
    
    if role != "barber":
        return jsonify({"ok": False, "error": "Only barbers can upload photos"}), 403
    
    # Get barber_id from user_id
    from .db import _get_conn
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT barber_id FROM Barber WHERE user_id = %s", (user_id,))
                result = cur.fetchone()
                if not result:
                    return jsonify({"ok": False, "error": "Barber profile not found"}), 404
                barber_id = result[0]
    except Exception as e:
        print(f"[UPLOAD_PHOTO] Error getting barber: {e}")
        return jsonify({"ok": False, "error": "Could not find barber profile"}), 500
    
    # Get file from request
    file = request.files.get("photo")
    print(f"[UPLOAD_PHOTO] File object: {file}")
    if file:
        print(f"[UPLOAD_PHOTO] File details: name={file.filename}, content_type={file.content_type}, size={len(file.read())} bytes")
        file.seek(0)  # Reset file pointer after reading size
    
    if not file or file.filename == "":
        return jsonify({"ok": False, "error": "No photo provided"}), 400
    
    print(f"[UPLOAD_PHOTO] File received: {file.filename}")
    print(f"[UPLOAD_PHOTO] File content-type from request: {file.content_type}")
    
    # Validate file type
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    file_ext = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else ""
    print(f"[UPLOAD_PHOTO] File extension: {file_ext}")
    
    if file_ext not in ALLOWED_EXTENSIONS:
        return jsonify({"ok": False, "error": "File type not allowed. Use jpg, jpeg, png, or webp"}), 400
    
    # Get image dimensions
    width_px = request.form.get("width", type=int)
    height_px = request.form.get("height", type=int)
    
    print(f"[UPLOAD_PHOTO] Image dimensions: {width_px}x{height_px}")
    
    if not width_px or not height_px:
        return jsonify({"ok": False, "error": "Image dimensions required"}), 400
    
    # Get is_post flag (default to True for backward compatibility)
    is_post_str = request.form.get("is_post", "true").lower()
    is_post = is_post_str in ["true", "1", "yes"]
    
    print(f"[UPLOAD_PHOTO] is_post: {is_post}")
    
    # Get selected tag IDs
    tag_ids_str = request.form.get("tag_ids", "")
    tag_ids = []
    if tag_ids_str:
        try:
            tag_ids = [int(x) for x in tag_ids_str.split(",") if x.strip().isdigit()]
        except (ValueError, TypeError):
            return jsonify({"ok": False, "error": "Invalid tag IDs"}), 400
    
    # For gallery photos (is_post=False), require exactly one tag
    if not is_post and len(tag_ids) != 1:
        return jsonify({"ok": False, "error": "Gallery photos require exactly one tag"}), 400
    
    # For posts (is_post=True), require at least one tag
    if is_post and len(tag_ids) == 0:
        return jsonify({"ok": False, "error": "Posts require at least one tag"}), 400
    
    print(f"[UPLOAD_PHOTO] Tag IDs: {tag_ids}")
    
    try:
        # Read file data
        file_data = file.read()
        print(f"[UPLOAD_PHOTO] File data read: {len(file_data)} bytes")
        print(f"[UPLOAD_PHOTO] File data type: {type(file_data)}")
        if file_data:
            print(f"[UPLOAD_PHOTO] First 50 bytes: {file_data[:50]}")
        
        if not file_data:
            return jsonify({"ok": False, "error": "File is empty"}), 400
        
        # Upload to Supabase storage
        print(f"[UPLOAD_PHOTO] Calling upload_photo_to_storage with:")
        print(f"  - barber_id: {barber_id}")
        print(f"  - file_data length: {len(file_data)}")
        print(f"  - filename: {file.filename}")
        
        storage_path = upload_photo_to_storage(barber_id, file_data, file.filename)
        if not storage_path:
            return jsonify({"ok": False, "error": "Failed to upload photo to storage"}), 500
        
        # Create database record
        photo_id = create_haircut_post(barber_id, storage_path, width_px, height_px, tag_ids, is_post=is_post)
        
        print(f"[UPLOAD_PHOTO] Photo uploaded successfully: photo_id={photo_id}, barber_id={barber_id}, path={storage_path}, is_post={is_post}")
        
        return jsonify({
            "ok": True,
            "photo_id": photo_id,
            "storage_path": storage_path,
        }), 201
        
    except Exception as e:
        error_msg = str(e)
        print(f"[UPLOAD_PHOTO] Error uploading photo: {error_msg}")
        import traceback
        print(f"[UPLOAD_PHOTO] Traceback: {traceback.format_exc()}")
        return jsonify({"ok": False, "error": error_msg}), 500


@api_bp.post("/reviews")
def post_review():
    """Create a new review for a barber or barbershop."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401
    
    user_id = int(u["id"])
    data = request.get_json(silent=True) or {}
    
    target_barber_id = data.get("target_barber_id")
    target_barbershop_id = data.get("target_barbershop_id")
    text = data.get("text", "").strip()
    rating = data.get("rating")
    
    # Validate input
    if not text:
        return jsonify({"ok": False, "error": "Review text is required"}), 400
    
    if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"ok": False, "error": "Rating must be between 1 and 5"}), 400
    
    if not target_barber_id and not target_barbershop_id:
        return jsonify({"ok": False, "error": "Either target_barber_id or target_barbershop_id is required"}), 400
    
    try:
        review_id = create_review(
            user_id=user_id,
            target_barber_id=target_barber_id,
            target_barbershop_id=target_barbershop_id,
            text=text,
            rating=rating
        )
        
        # Get the target_barber_user_id if reviewing a barber
        target_barber_user_id = None
        if target_barber_id:
            from .db import _get_conn
            with _get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM Barber WHERE barber_id = %s", (target_barber_id,))
                    row = cur.fetchone()
                    target_barber_user_id = row[0] if row else None
        
        return jsonify({"ok": True, "review_id": review_id, "user_id": user_id, "target_barber_user_id": target_barber_user_id}), 201
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@api_bp.post("/reviews/reply")
def post_review_reply():
    """Create a reply to an existing review."""
    u = session.get("user")
    if not u or not u.get("id"):
        return jsonify({"ok": False, "error": "Not logged in"}), 401
    
    user_id = int(u["id"])
    data = request.get_json(silent=True) or {}
    
    parent_review_id = data.get("parent_review_id")
    text = data.get("text", "").strip()
    
    # Validate input
    if not parent_review_id:
        return jsonify({"ok": False, "error": "parent_review_id is required"}), 400
    
    if not text:
        return jsonify({"ok": False, "error": "Reply text is required"}), 400
    
    try:
        reply_id = create_review_reply(
            user_id=user_id,
            parent_review_id=parent_review_id,
            text=text
        )
        return jsonify({"ok": True, "reply_id": reply_id, "user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@api_bp.get("/reviews")
def get_reviews():
    """Fetch reviews for a barber or barbershop."""
    target_barber_id = request.args.get("target_barber_id", type=int)
    target_barbershop_id = request.args.get("target_barbershop_id", type=int)
    user_data = session.get("user")
    current_user_id = user_data.get("id") if user_data else None
    
    print(f"[GET_REVIEWS] Request received: target_barber_id={target_barber_id}, target_barbershop_id={target_barbershop_id}, current_user_id={current_user_id}")
    
    if not target_barber_id and not target_barbershop_id:
        print("[GET_REVIEWS] Error: Neither target_barber_id nor target_barbershop_id provided")
        return jsonify({"ok": False, "error": "Either target_barber_id or target_barbershop_id is required"}), 400
    
    try:
        print(f"[GET_REVIEWS] Calling get_reviews_with_replies with barber_id={target_barber_id}, current_user_id={current_user_id}")
        reviews = get_reviews_with_replies(
            target_barber_id=target_barber_id,
            target_barbershop_id=target_barbershop_id,
            current_user_id=current_user_id
        )
        print(f"[GET_REVIEWS] Success! Retrieved {len(reviews)} reviews")
        return jsonify({"ok": True, "reviews": reviews}), 200
    except Exception as e:
        print(f"[GET_REVIEWS] Exception: {str(e)}")
        import traceback
        print(f"[GET_REVIEWS] Traceback: {traceback.format_exc()}")
        return jsonify({"ok": False, "error": str(e)}), 500


@api_bp.post("/reviews/<int:review_id>/vote")
def vote_on_review(review_id: int):
    """Vote on a review or reply as helpful."""
    user_data = session.get("user")
    current_user_id = user_data.get("id") if user_data else None
    
    print(f"[VOTE_REVIEW] Request received: review_id={review_id}, user_id={current_user_id}")
    
    if not current_user_id:
        print("[VOTE_REVIEW] Error: User not logged in")
        return jsonify({"ok": False, "error": "Must be logged in to vote"}), 401
    
    try:
        # Try to add the vote
        success = add_helpful_vote(review_id, current_user_id)
        
        if success:
            print(f"[VOTE_REVIEW] Vote added successfully")
            vote_count = get_helpful_vote_count(review_id)
            return jsonify({"ok": True, "message": "Vote added", "helpful_vote_count": vote_count}), 200
        else:
            print(f"[VOTE_REVIEW] User already voted on this review")
            return jsonify({"ok": False, "error": "You already voted on this"}), 400
    except Exception as e:
        print(f"[VOTE_REVIEW] Exception: {str(e)}")
        import traceback
        print(f"[VOTE_REVIEW] Traceback: {traceback.format_exc()}")
        return jsonify({"ok": False, "error": str(e)}), 500


@api_bp.delete("/reviews/<int:review_id>/vote")
def remove_vote_on_review(review_id: int):
    """Remove a helpful vote from a review or reply."""
    user_data = session.get("user")
    current_user_id = user_data.get("id") if user_data else None
    
    print(f"[REMOVE_VOTE] Request received: review_id={review_id}, user_id={current_user_id}")
    
    if not current_user_id:
        print("[REMOVE_VOTE] Error: User not logged in")
        return jsonify({"ok": False, "error": "Must be logged in"}), 401
    
    try:
        success = remove_helpful_vote(review_id, current_user_id)
        
        if success:
            print(f"[REMOVE_VOTE] Vote removed successfully")
            vote_count = get_helpful_vote_count(review_id)
            return jsonify({"ok": True, "message": "Vote removed", "helpful_vote_count": vote_count}), 200
        else:
            print(f"[REMOVE_VOTE] No vote found to remove")
            return jsonify({"ok": False, "error": "No vote to remove"}), 404
    except Exception as e:
        print(f"[REMOVE_VOTE] Exception: {str(e)}")
        import traceback
        print(f"[REMOVE_VOTE] Traceback: {traceback.format_exc()}")
        return jsonify({"ok": False, "error": str(e)}), 500
