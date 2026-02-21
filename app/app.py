from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename 

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def welcome():
        return render_template("welcome.html", title="Welcome Page")

    @app.get("/discover")
    def discover():
        return render_template("discover.html", title="Discover Page")

    @app.get("/barber_dashboard")
    def barber_dashboard():
        return render_template("barber_dashboard.html", title="Barber Dashboard")

    @app.post("/barber_dashboard/upload_post")
    def upload_post():
        errors = []
        # required photo
        photo = request.files.get("photo")
        if not photo or photo.filename == "":
            errors.append("Photo is required.")
        else:
            safe_name = secure_filename(photo.filename)
            ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
            if ext not in ALLOWED_EXTENSIONS:
                errors.append("Invalid image type. Allowed: jpg, jpeg, png, webp")
        # optional tags
        tags_raw = (request.form.get("tags") or "").strip()
        tag_ids = []
        if tags_raw: 
            try:
                tag_ids = sorted({int(x.strip()) for x in tags_raw.split(",") if x.strip()})
            except ValueError:
                errors.append("Tags must be comma-separated numeric IDs (e.g. 1,2,9).")

        if errors:
            return (
                render_template(
                    "barber_dashboard.html",
                    title="Barber Dashboard",
                    errors=errors,
                    success=None,
                    form_data={"tags": tags_raw},
                ),
                400,
            )
        # TODO: save file + insert into DB via app/db/queries.py, Database not made yet
        return render_template(
            "barber_dashboard.html",
            title="Barber Dashboard",
            errors=[],
            success="Post uploaded successfully.",
            form_data={"tags": ""},
        )
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
