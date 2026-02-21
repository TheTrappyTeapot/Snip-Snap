from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

from app.db.queries import create_haircut_post, filter_existing_tag_ids

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
        return render_template(
            "barber_dashboard.html",
            title="Barber Dashboard",
            errors=[],
            success=None,
            form_data={"tags": ""},
        )

    @app.post("/barber_dashboard/upload_post")
    def upload_post():
        errors = []

        photo = request.files.get("photo")
        if not photo or photo.filename == "":
            errors.append("Photo is required.")
            safe_name = ""
            ext = ""
            width_px = 0
            height_px = 0
        else:
            safe_name = secure_filename(photo.filename)
            ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
            if ext not in ALLOWED_EXTENSIONS:
                errors.append("Invalid image type. Allowed: jpg, jpeg, png, webp.")

            try:
                image = Image.open(photo.stream)
                width_px, height_px = image.size
                photo.stream.seek(0)
            except (UnidentifiedImageError, OSError):
                errors.append("Uploaded file is not a valid image.")
                width_px = 0
                height_px = 0

        tags_raw = (request.form.get("tags") or "").strip()
        tag_ids = []
        if tags_raw:
            try:
                tag_ids = sorted({int(x.strip()) for x in tags_raw.split(",") if x.strip()})
            except ValueError:
                errors.append("Tags must be comma-separated numeric IDs (e.g. 1,2,9).")

        if tag_ids:
            try:
                valid_tag_ids = filter_existing_tag_ids(tag_ids)
                invalid_tag_ids = sorted(set(tag_ids) - set(valid_tag_ids))
                if invalid_tag_ids:
                    errors.append(
                        "Unknown tag IDs: " + ", ".join(str(tag_id) for tag_id in invalid_tag_ids)
                    )
                tag_ids = valid_tag_ids
            except Exception:
                errors.append("Could not validate tags right now. Try again.")

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

        upload_dir = Path(app.root_path) / "static" / "uploads" / "haircuts"
        upload_dir.mkdir(parents=True, exist_ok=True)

        stored_name = f"{uuid4().hex}.{ext}"
        file_path = upload_dir / stored_name
        image_url = f"/static/uploads/haircuts/{stored_name}"

        try:
            photo.save(file_path)
            barber_id = 1  # TODO: replace with logged-in barber ID once auth is implemented
            create_haircut_post(
                barber_id=barber_id,
                image_url=image_url,
                width_px=width_px,
                height_px=height_px,
                tag_ids=tag_ids,
            )
        except Exception:
            if file_path.exists():
                file_path.unlink()
            return (
                render_template(
                    "barber_dashboard.html",
                    title="Barber Dashboard",
                    errors=["Could not save post to the database."],
                    success=None,
                    form_data={"tags": tags_raw},
                ),
                500,
            )

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
