"""
Script to remove all haircutphotos where is_post = false,
keeping only the most recent 8 photos.
"""

from ..db import _get_conn

def cleanup_non_post_photos():
    """
    Deletes all non-post haircutphotos except for the 8 most recent ones.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            # First, find the 8 most recent non-post photos
            cur.execute(
                """
                SELECT photo_id FROM HaircutPhoto
                WHERE is_post = false
                ORDER BY created_at DESC
                LIMIT 8
                """
            )
            keep_ids = [row[0] for row in cur.fetchall()]
            
            print(f"Keeping {len(keep_ids)} photos with IDs: {keep_ids}")
            
            # Delete all non-post photos except those 8
            if keep_ids:
                placeholders = ','.join(['%s'] * len(keep_ids))
                cur.execute(
                    f"""
                    DELETE FROM HaircutPhoto
                    WHERE is_post = false AND photo_id NOT IN ({placeholders})
                    """,
                    keep_ids
                )
            else:
                # If there are no photos to keep, delete all non-post photos
                cur.execute(
                    """
                    DELETE FROM HaircutPhoto
                    WHERE is_post = false
                    """
                )
            
            deleted_count = cur.rowcount
            conn.commit()
            
            print(f"Deleted {deleted_count} non-post photos")
            print(f"Remaining non-post photos: {len(keep_ids)}")

if __name__ == "__main__":
    cleanup_non_post_photos()
    print("Cleanup complete!")
