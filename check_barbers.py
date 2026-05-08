#!/usr/bin/env python
from app.app import create_app
from app.db import get_barber_public_by_user_id

app = create_app()
with app.app_context():
    # Check specific IDs
    print('Checking specific user IDs:')
    for bid in range(1, 10):
        b = get_barber_public_by_user_id(bid)
        if b:
            print(f"  Barber ID {bid}: {b.get('username')} ({b.get('first_name')} {b.get('last_name')})")
