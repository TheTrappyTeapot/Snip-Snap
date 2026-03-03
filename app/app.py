import os

from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request, jsonify, abort
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

from app.db.queries import (
    create_haircut_post,
    filter_existing_tag_ids,
    get_barbershops_for_map,
    get_user_promo,
)

from app.services.post_gallery_service import query_post_gallery
from app.services.discover_search_service import get_discover_search_items
from app.services.auth_service import try_get_current_user, require_current_user
from app.services.upload_post_service import handle_upload_post

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def create_app():
    app = Flask(__name__)

    app.config["SUPABASE_PUBLIC_URL"] = os.environ.get("SUPABASE_PUBLIC_URL")
    app.config["SUPABASE_PUBLIC_ANON_KEY"] = os.environ.get("SUPABASE_PUBLIC_ANON_KEY")

    # -------------------------
    # Pages (templates)
    # -------------------------

    @app.get("/")
    def welcome():
        return render_template("welcome.html", title="Welcome Page")

    @app.get("/discover")
    def discover():
        return render_template("discover.html", title="Discover Page")

    @app.get("/map")
    def map_page():
        return render_template("map.html", title="Map")

    @app.get("/barber_dashboard")
    def barber_dashboard():
        """
        Temporary: still renders a dashboard without auth gating.
        Later: require barber role and derive barber_id from session.
        """
        return render_template(
            "barber_dashboard.html",
            title="Barber Dashboard",
            errors=[],
            success=None,
            form_data={"tags": ""},
        )

    # -------------------------
    # Auth / Session API
    # -------------------------

    @app.get("/api/session")
    def api_session():
        """
        Returns session context for the current request.
        - Guest: authenticated false
        - Logged in (valid JWT) but not linked to App_User: authenticated true, linked false
        - Logged in and linked: authenticated true, linked true (+ ids/role)
        """
        try:
            user = try_get_current_user(request)
        except Exception:
            return jsonify({"authenticated": False, "error": "Invalid session token"}), 401

        if user is None:
            token_present = bool(request.headers.get("Authorization", "").strip())
            if token_present:
                return jsonify({"authenticated": True, "linked": False}), 200
            return jsonify({"authenticated": False}), 200

        return jsonify(
            {
                "authenticated": True,
                "linked": True,
                "user_id": user.user_id,
                "role": user.role,
                "auth_user_id": user.auth_user_id,
            }
        )

    @app.get("/api/me/promo")
    def api_me_promo():
        """
        Promo for the currently authenticated user.
        This is the endpoint features should prefer (not /api/users/<id>/promo).
        """
        try:
            user = require_current_user(request)
        except Exception:
            abort(401, description="Not authenticated")

        user_data = get_user_promo(user.user_id)
        if user_data is None:
            abort(404, description="User not found")
        return jsonify(user_data)

    # -------------------------
    # Public API
    # -------------------------

    @app.get("/api/barbershops")
    def api_barbershops():
        try:
            shops = get_barbershops_for_map()
            return jsonify(shops)
        except Exception:
            return jsonify({"error": "Could not load barbershops"}), 500

    @app.post("/api/gallery/posts")
    def api_gallery_posts():
        # Keep public for guests (can be locked down later if desired)
        payload = request.get_json(silent=True) or {}
        try:
            result = query_post_gallery(payload)
            return jsonify(result)
        except Exception:
            return jsonify({"error": "Could not load gallery posts"}), 500

    @app.get("/api/discover/search_items")
    def api_discover_search_items():
        try:
            items = get_discover_search_items()
            return jsonify({"items": items})
        except Exception:
            return jsonify({"error": "Could not load search items"}), 500


    @app.post("/barber_dashboard/upload_post")
    def upload_post():
        # TODO: derive barber_id from authenticated user once barber auth mapping exists
        barber_id = 1

        result = handle_upload_post(
            root_path=app.root_path,
            barber_id=barber_id,
            photo=request.files.get("photo"),
            tags_raw=request.form.get("tags") or "",
        )

        return (
            render_template(
                "barber_dashboard.html",
                title="Barber Dashboard",
                errors=result.errors,
                success=result.success,
                form_data=result.form_data,
            ),
            result.status_code,
        )
    
    return app  


if __name__ == "__main__":
    create_app().run(debug=True)