"""
Reverse geocode user locations: fetch lat/lng and populate postcode.
Uses postcodes.io API to convert coordinates to UK postcodes.

Usage:
    From project root: python -m app.handy_scripts.populate_postcodes_from_coords
    Or from Flask shell: from app.handy_scripts.populate_postcodes_from_coords import populate_postcodes; populate_postcodes()
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db import _get_conn

load_dotenv()

# postcodes.io reverse API endpoint
POSTCODES_IO_REVERSE_URL = "https://api.postcodes.io/postcodes"


def reverse_geocode(lat: float, lng: float) -> str | None:
    """
    Convert latitude/longitude to postcode using postcodes.io API.
    
    Args:
        lat: Latitude
        lng: Longitude
        
    Returns:
        Postcode string (e.g., "SW1A 1AA") or None if not found
    """
    try:
        response = requests.get(
            POSTCODES_IO_REVERSE_URL,
            params={"lon": lng, "lat": lat},
            timeout=10
        )
        
        if not response.ok:
            print(f"  ✗ Reverse geocoding failed (HTTP {response.status_code}) for ({lat}, {lng})")
            return None
        
        data = response.json()
        
        # Check if we got results
        if data.get("status") != 200 or not data.get("result"):
            print(f"  ⚠️  No postcode found for ({lat}, {lng})")
            return None
        
        # Extract postcode from first result
        postcode = data["result"][0].get("postcode")
        if postcode:
            print(f"  ✓ ({lat}, {lng}) → {postcode}")
            return postcode
        else:
            print(f"  ✗ No postcode in result for ({lat}, {lng})")
            return None
            
    except requests.RequestException as e:
        print(f"  ✗ API error for ({lat}, {lng}): {e}")
        return None
    except Exception as e:
        print(f"  ✗ Unexpected error for ({lat}, {lng}): {e}")
        return None


def populate_postcodes():
    """
    Fetch all users with location_lat/location_lng but no postcode,
    reverse geocode their coordinates, and update their postcode in DB.
    """
    print("=" * 70)
    print("Populating postcodes from user coordinates")
    print("=" * 70)
    
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                # Find users with coordinates but missing postcode
                cur.execute("""
                    SELECT user_id, location_lat, location_lng, postcode
                    FROM App_User
                    WHERE location_lat IS NOT NULL
                      AND location_lng IS NOT NULL
                    ORDER BY user_id
                """)
                
                users = cur.fetchall()
                
                if not users:
                    print("✓ No users found with coordinates")
                    return
                
                print(f"\n📍 Found {len(users)} users with coordinates")
                print()
                
                updated_count = 0
                skipped_count = 0
                
                for user_id, lat, lng, existing_postcode in users:
                    # Skip if postcode already exists
                    if existing_postcode:
                        print(f"User {user_id}: ⏭️  Already has postcode '{existing_postcode}'")
                        skipped_count += 1
                        continue
                    
                    print(f"User {user_id}: Reverse geocoding...", end=" ")
                    
                    # Reverse geocode
                    postcode = reverse_geocode(lat, lng)
                    
                    if postcode:
                        # Update database
                        try:
                            with conn.cursor() as update_cur:
                                update_cur.execute(
                                    "UPDATE App_User SET postcode = %s WHERE user_id = %s",
                                    (postcode.strip(), user_id)
                                )
                            conn.commit()
                            print(f" → Updated in DB ✓")
                            updated_count += 1
                        except Exception as e:
                            print(f" → DB update failed: {e}")
                            conn.rollback()
                    else:
                        print(f" → Skipped (no postcode found)")
                        skipped_count += 1
                
                print()
                print("=" * 70)
                print(f"✓ Complete!")
                print(f"  Updated: {updated_count}")
                print(f"  Skipped: {skipped_count}")
                print(f"  Total processed: {len(users)}")
                print("=" * 70)
                
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    populate_postcodes()
