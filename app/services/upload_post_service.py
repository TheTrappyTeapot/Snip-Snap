from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.db.queries import create_haircut_post, filter_existing_tag_ids

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


@dataclass(frozen=True)
class UploadPostResult:
    ok: bool
    status_code: int
    errors: List[str]
    success: Optional[str]
    form_data: dict


def handle_upload_post(
    *,
    root_path: str,
    barber_id: int,
    photo: Optional[FileStorage],
    tags_raw: str,
) -> UploadPostResult:
    """
    Backend service for the 'upload post' feature.
    - Validates image + tags
    - Saves file to static/uploads/haircuts
    - Writes DB rows (HaircutPhoto + HaircutPhoto_Tag)
    Returns structured result (no template rendering).
    """
    errors: List[str] = []
    tags_raw = (tags_raw or "").strip()

    # ---- Validate photo ----
    if not photo or not getattr(photo, "filename", ""):
        errors.append("Photo is required.")
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

    # ---- Parse + validate tags ----
    tag_ids: List[int] = []
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
                errors.append("Unknown tag IDs: " + ", ".join(str(t) for t in invalid_tag_ids))
            tag_ids = valid_tag_ids
        except Exception:
            errors.append("Could not validate tags right now. Try again.")

    if errors:
        return UploadPostResult(
            ok=False,
            status_code=400,
            errors=errors,
            success=None,
            form_data={"tags": tags_raw},
        )

    # ---- Save file + write DB ----
    upload_dir = Path(root_path) / "static" / "uploads" / "haircuts"
    upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid4().hex}.{ext}"
    file_path = upload_dir / stored_name
    image_url = f"/static/uploads/haircuts/{stored_name}"

    try:
        # Save uploaded file
        photo.save(file_path)

        # Create DB rows
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
        return UploadPostResult(
            ok=False,
            status_code=500,
            errors=["Could not save post to the database."],
            success=None,
            form_data={"tags": tags_raw},
        )

    return UploadPostResult(
        ok=True,
        status_code=200,
        errors=[],
        success="Post uploaded successfully.",
        form_data={"tags": ""},
    )