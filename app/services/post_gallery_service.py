from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from app.db.queries import fetch_discover_posts


def _safe_int_list(value: Any) -> List[int]:
    if not isinstance(value, list):
        return []
    out: List[int] = []
    for x in value:
        if isinstance(x, int):
            out.append(x)
    return out


def _resolve_effective_sort(filter_ids: List[int], effective_sort: Optional[str]) -> str:
    if effective_sort in ("most_recent", "highest_rated", "closest"):
        return effective_sort
    if 2 in filter_ids:
        return "most_recent"
    if len(filter_ids) > 1:
        return "most_recent"
    if filter_ids == [1]:
        return "highest_rated"
    if filter_ids == [0]:
        return "closest"
    return "most_recent"


def _parse_cursor(cursor: Any) -> Optional[Tuple[datetime, int]]:
    if cursor is None:
        return None
    if not isinstance(cursor, dict):
        return None
    created_at = cursor.get("created_at")
    photo_id = cursor.get("photo_id")
    if not isinstance(created_at, str) or not isinstance(photo_id, int):
        return None
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt, photo_id)


def query_post_gallery(payload: Dict[str, Any]) -> Dict[str, Any]:
    filter_ids = _safe_int_list(payload.get("filter_ids"))
    tag_ids = _safe_int_list(payload.get("tag_ids"))
    barber_ids = _safe_int_list(payload.get("barber_ids"))
    barbershop_ids = _safe_int_list(payload.get("barbershop_ids"))
    limit = payload.get("limit")
    if not isinstance(limit, int) or limit < 1 or limit > 60:
        limit = 18

    effective_sort = _resolve_effective_sort(filter_ids, payload.get("effective_sort"))

    cursor_tuple = _parse_cursor(payload.get("cursor"))

    rows = fetch_discover_posts(
        tag_ids=tag_ids,
        barber_ids=barber_ids,
        barbershop_ids=barbershop_ids,
        cursor=cursor_tuple,
        limit=limit,
        effective_sort=effective_sort,
    )

    items = []
    for r in rows:
        items.append(
            {
                "item_type": "post",
                "post_id": r["photo_id"],
                "created_at": r["created_at"].isoformat().replace("+00:00", "Z"),
                "image_url": r["image_url"],
                "image_width_px": r["width_px"],
                "image_height_px": r["height_px"],
            }
        )

    has_more = len(items) == limit

    next_cursor = None
    if items:
        last = rows[-1]
        next_cursor = {
            "created_at": last["created_at"].isoformat().replace("+00:00", "Z"),
            "photo_id": last["photo_id"],
        }

    return {"items": items, "next_cursor": next_cursor, "has_more": has_more}