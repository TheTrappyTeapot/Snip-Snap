import os
from flask import render_template, request, redirect, session, url_for, jsonify
from .auth import verify_supabase_jwt
from .access import login_required, roles_required
from .db import link_auth_user_id, get_app_user_by_auth_user_id, get_app_user_by_email, get_user_promo
from uuid import uuid4
from datetime import datetime

def register_routes(app):

    print("SUPABASE_URL =", os.getenv("SUPABASE_URL"))

    @app.route("/")
    def home():
        return render_template("pages/welcome.html")

    @app.route("/login")
    def login():
        return render_template(
            "pages/login.html",
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_anon_key=os.environ["SUPABASE_ANON_KEY"],
        )

    @app.route("/signup")
    def signup():
        return render_template(
            "pages/signup.html",
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_anon_key=os.environ["SUPABASE_ANON_KEY"],
        )

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("home"))

    # OAuth redirect lands here (browser page that will POST token to /auth/callback)
    @app.route("/auth/redirect")
    def auth_redirect():
        return render_template(
            "pages/auth_redirect.html",
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_anon_key=os.environ["SUPABASE_ANON_KEY"],
        )

    @app.post("/auth/callback")
    def auth_callback():
        print("\n--- AUTH CALLBACK START ---")

        data = request.get_json(silent=True) or {}
        print("Received JSON:", data)

        access_token = data.get("access_token")
        if not access_token:
            print("No access_token received")
            return jsonify({"ok": False, "error": "Missing access_token"}), 400

        print("Access token received. Verifying...")

        try:
            claims = verify_supabase_jwt(access_token)
            print("JWT verified. Claims:", claims)
        except Exception as e:
            print("JWT verification failed:", repr(e))
            return jsonify({"ok": False, "error": str(e)}), 401

        auth_user_id = claims.get("sub")
        email = claims.get("email")

        print("JWT sub:", auth_user_id)
        print("JWT email:", email)

        from .db import get_app_user_by_auth_user_id

        app_user = get_app_user_by_auth_user_id(auth_user_id)
        print("DB lookup result:", app_user)

        if not app_user:
            print("No App_User found for auth_user_id")
            return jsonify({"ok": False, "error": "User not found in App_User"}), 403

        session["user"] = {
            "id": app_user["user_id"],
            "auth_user_id": app_user["auth_user_id"],
            "email": app_user["email"],
            "username": app_user["username"],
            "role": (app_user["role"] or "").strip().lower(),
        }

        print("Session set to:", session["user"])
        print("--- AUTH CALLBACK END ---\n")

        return jsonify({"ok": True})
    
    
    @app.post("/guest/start")
    def guest_start():
        session["user"] = {
            "id": None,
            "auth_user_id": None,
            "email": None,
            "username": f"guest-{uuid4().hex[:8]}",
            "role": "guest",
            "guest_started_at": datetime.utcnow().isoformat() + "Z",
        }
        return redirect(url_for("discover"))
    

    @app.get("/whoami")
    def whoami():
        print("Current session:", session.get("user"))
        return jsonify(session.get("user") or {})
    
    @app.route("/discover")
    @login_required
    def discover():
        return render_template("pages/discover.html")
    
    @app.route("/map")
    @login_required
    def map_page():
        return render_template("pages/map.html")


    @app.route("/profile")
    @roles_required("customer", "barber")   # guests cannot access
    def profile():
        return render_template("pages/profile.html")


    @app.route("/dashboard")
    @roles_required("barber")              # barbers only
    def dashboard():
        return render_template("pages/dashboard.html")

    @app.get("/api/users/<int:user_id>/promo")
    def user_promo(user_id):
        user_data = get_user_promo(user_id)
        if user_data is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user_data)