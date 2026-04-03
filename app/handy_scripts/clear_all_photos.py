"""
Script to completely clear haircutphoto and haircutphoto_tag tables.
"""

from ..db import _get_conn

def clear_all_photos():
    """
    Deletes all records from haircutphoto_tag and haircutphoto.
    Must delete from haircutphoto_tag first due to foreign key constraints.
    """
    with _get_conn() as conn:
        with conn.cursor() as cur:
            # Delete from haircutphoto_tag first (foreign key dependency)
            cur.execute("DELETE FROM HaircutPhoto_Tag")
            tag_deletes = cur.rowcount
            
            # Delete from haircutphoto
            cur.execute("DELETE FROM HaircutPhoto")
            photo_deletes = cur.rowcount
            
            conn.commit()
            
            print(f"Deleted {tag_deletes} haircutphoto_tag rows")
            print(f"Deleted {photo_deletes} haircutphoto rows")

if __name__ == "__main__":
    clear_all_photos()
    print("All haircut photos cleared!")
