# db.py

This file contains all the database-related functions and queries.

## What belongs here
- SQL queries and database functions
- Data models and schemas

## What does NOT belong here
- Flask app code (this goes in `app/`)
- HTML templates (these go in `app/templates/`)
- CSS/JS assets (these go in `app/static/`)

## Functions
- `get_user_promo(user_id)`: Retrieve user information based on the provided `user_id`.

## Example usage
```python
from app.db import get_user_promo

user_promo = get_user_promo(1)
print(user_promo)
```

## SQL Queries
- User information query:
```sql
SELECT u.id, u.name, u.role, u.profile_image_url, b.name AS barbershop_name
FROM users u
LEFT JOIN barbershops b ON u.barbershop_id = b.id
WHERE u.id = %s
```