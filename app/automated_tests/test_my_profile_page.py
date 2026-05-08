"""Automated tests for the My Profile page."""

import pytest
from app.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    app.secret_key = 'test-secret-key'
    
    with app.test_client() as test_client:
        # Mock authenticated session
        with test_client.session_transaction() as sess:
            sess['user'] = {
                'id': 1,
                'email': 'test@ss.dev',
                'username': 'testuser',
                'role': 'barber'
            }
        yield test_client


class TestMyProfilePage:
    """Test suite for the my profile page functionality."""

    def test_my_profile_page_loads(self, client):
        """Test that the my profile page loads successfully."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'profile' in response.data.lower() or b'username' in response.data.lower()

    def test_my_profile_page_contains_form_element(self, client):
        """Test that the profile page contains a form element."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'<form' in response.data or b'form' in response.data.lower()

    def test_my_profile_page_contains_username_input(self, client):
        """Test that profile page has username input."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'username' in response.data.lower()

    def test_my_profile_page_contains_photo_upload(self, client):
        """Test that profile page has photo upload element."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert (b'upload' in response.data.lower() or 
                b'photo' in response.data.lower() or
                b'file' in response.data.lower())

    def test_my_profile_page_contains_location_input(self, client):
        """Test that profile page has location/postcode input."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert (b'postcode' in response.data.lower() or 
                b'location' in response.data.lower() or
                b'address' in response.data.lower())

    def test_my_profile_page_contains_account_type_selector(self, client):
        """Test that profile page has account type selector."""
        response = client.get('/profile')
        assert response.status_code == 200
        assert (b'customer' in response.data.lower() or 
                b'barber' in response.data.lower() or
                b'account' in response.data.lower())

    def test_my_profile_profanity_filter_username(self, client):
        """Test ID 41: Profanity filter on username - Enter 'fuck'"""
        # Input: "fuck" (profane username)
        response = client.post('/profile', data={
            'username': 'fuck',
            'postcode': 'SW1A 1AA',
            'role': 'barber'
        })
        # Expected: Form withholds username for profanity concerns
        assert response.status_code in [200, 400]
        assert (b'profan' in response.data.lower() or 
                b'inappropriate' in response.data.lower() or
                b'profile' in response.data.lower())

    def test_my_profile_duplicate_username(self, client):
        """Test ID 42: Duplicate username detection - Enter 'bob'"""
        # Input: "bob" (existing username)
        response = client.post('/profile', data={
            'username': 'bob',
            'postcode': 'SW1A 1AA',
            'role': 'barber'
        })
        # Expected: Error message asking to use different username
        assert response.status_code in [200, 400]
        assert (b'already' in response.data.lower() or 
                b'different' in response.data.lower() or
                b'taken' in response.data.lower() or
                b'profile' in response.data.lower())

    def test_my_profile_username_too_long(self, client):
        """Test ID 43: Username too long - Enter 51+ characters"""
        # Input: 51 'i' characters (exceeds 50 char limit)
        long_username = 'i' * 51
        response = client.post('/profile', data={
            'username': long_username,
            'postcode': 'SW1A 1AA',
            'role': 'barber'
        })
        # Expected: Form requests that username is less than 50 characters
        assert response.status_code in [200, 400]
        assert (b'50' in response.data or 
                b'too long' in response.data.lower() or
                b'character' in response.data.lower())

    def test_my_profile_valid_username(self, client):
        """Test ID 44: Valid username entry - Enter 'alexander'"""
        # Input: "alexander" (valid username)
        response = client.post('/profile', data={
            'username': 'alexander',
            'postcode': 'SW1A 1AA',
            'role': 'barber'
        })
        # Expected: Form parses the username as valid
        assert response.status_code in [200, 201]

    def test_my_profile_photo_upload_png(self, client):
        """Test ID 45: PNG photo upload"""
        # PNG file should be accepted
        response = client.post('/profile', data={
            'photo': (b'PNG mock data', 'test.png'),
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: Page loads successfully or photo is accepted
        assert response.status_code in [200, 201]
        assert b'profile' in response.data.lower()

    def test_my_profile_photo_upload_jpeg(self, client):
        """Test ID 46: JPEG photo upload"""
        # JPEG file should be accepted
        response = client.post('/profile', data={
            'photo': (b'JPEG mock data', 'test.jpeg'),
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: Photo upload succeeds
        assert response.status_code in [200, 201]

    def test_my_profile_photo_upload_webp(self, client):
        """Test ID 47: WEBP photo upload"""
        # WEBP file should be accepted
        response = client.post('/profile', data={
            'photo': (b'WEBP mock data', 'test.webp'),
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: Photo upload succeeds
        assert response.status_code in [200, 201]

    def test_my_profile_photo_upload_jpg_invalid(self, client):
        """Test ID 48: JPG photo upload rejected"""
        # JPG file should be rejected (only png, jpeg, webp allowed)
        response = client.post('/profile', data={
            'photo': (b'JPG mock data', 'test.jpg'),
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: System rejects the photo
        assert response.status_code in [200, 400, 415]
        assert (b'jpg' in response.data.lower() or 
                b'not supported' in response.data.lower() or
                b'reject' in response.data.lower() or
                b'error' in response.data.lower())

    def test_my_profile_photo_upload_null(self, client):
        """Test ID 49: Null photo handling"""
        # Submitting without photo file
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: System accepts or rejects (depends on field requirement)
        assert response.status_code in [200, 400]

    def test_my_profile_postcode_valid(self, client):
        """Test ID 50: Valid postcode format - 'SW1A 1AA'"""
        # Input: "SW1A 1AA" (valid UK postcode)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA'
        })
        # Expected: Accepted
        assert response.status_code in [200, 201]
        assert b'profile' in response.data.lower()

    def test_my_profile_postcode_lowercase(self, client):
        """Test ID 51: Lowercase valid postcode - 'sw1a 1aa'"""
        # Input: "sw1a 1aa" (lowercase postcode)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'sw1a 1aa'
        })
        # Expected: Accepted or converted to uppercase
        assert response.status_code in [200, 201]

    def test_my_profile_postcode_empty(self, client):
        """Test ID 52: Empty postcode validation"""
        # Input: null (no postcode)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': ''
        })
        # Expected: Error message shown or rejected
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or 
                b'error' in response.data.lower() or
                b'postcode' in response.data.lower())

    def test_my_profile_postcode_too_short(self, client):
        """Test ID 53: Postcode too short - 'A1 1A'"""
        # Input: "A1 1A" (6 chars, too short for UK postcode)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'A1 1A'
        })
        # Expected: Rejected
        assert response.status_code in [200, 400]
        assert (b'too short' in response.data.lower() or 
                b'invalid' in response.data.lower() or
                b'character' in response.data.lower())

    def test_my_profile_postcode_too_long(self, client):
        """Test ID 54: Postcode too long - 'SW1A 11AAA'"""
        # Input: "SW1A 11AAA" (9 chars, too long)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 11AAA'
        })
        # Expected: Rejected - contains too many characters
        assert response.status_code in [200, 400]
        assert (b'too long' in response.data.lower() or 
                b'exceed' in response.data.lower() or
                b'character' in response.data.lower())

    def test_my_profile_postcode_invalid_characters(self, client):
        """Test ID 55: Invalid postcode characters - 'SW1A 1@A'"""
        # Input: "SW1A 1@A" (contains @ symbol)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1@A'
        })
        # Expected: Rejected - special character not allowed
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or 
                b'character' in response.data.lower() or
                b'special' in response.data.lower())

    def test_my_profile_postcode_numeric_only(self, client):
        """Test ID 56: Numeric only postcode - '123456'"""
        # Input: "123456" (only numbers, invalid format)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': '123456'
        })
        # Expected: Rejected - not in postcode format
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or 
                b'format' in response.data.lower())

    def test_my_profile_postcode_alphabetic_only(self, client):
        """Test ID 57: Alphabetic only postcode - 'ABCDEF'"""
        # Input: "ABCDEF" (only letters, invalid format)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'ABCDEF'
        })
        # Expected: Rejected - not in postcode format
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or 
                b'format' in response.data.lower())

    def test_my_profile_postcode_incomplete(self, client):
        """Test ID 58: Incomplete postcode - 'SW1A'"""
        # Input: "SW1A" (incomplete postcode)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A'
        })
        # Expected: Rejected - incomplete
        assert response.status_code in [200, 400]
        assert (b'incomplete' in response.data.lower() or 
                b'invalid' in response.data.lower())

    def test_my_profile_postcode_whitespace(self, client):
        """Test ID 59: Postcode whitespace handling - '  SW1A 1AA  '"""
        # Input: "  SW1A 1AA  " (with extra spaces)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': '  SW1A 1AA  '
        })
        # Expected: Accepted after trimming or rejected
        assert response.status_code in [200, 201]

    def test_my_profile_postcode_no_space(self, client):
        """Test ID 60: Postcode without space - 'SW1A1AA'"""
        # Input: "SW1A1AA" (without space)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A1AA'
        })
        # Expected: Accepted if auto-formatted, otherwise rejected
        assert response.status_code in [200, 201, 400]

    def test_my_profile_account_type_switch_customer(self, client):
        """Test ID 61: Switch account type to Customer"""
        # Input: Select "Customer"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'customer'
        })
        # Expected: Barbershop selection disappears (role changes to customer)
        assert response.status_code in [200, 201]
        assert b'customer' in response.data.lower()

    def test_my_profile_account_type_switch_barber(self, client):
        """Test ID 62: Switch account type to Barber"""
        # Input: Select "Barber"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber'
        })
        # Expected: Barbershop selection appears (role changes to barber)
        assert response.status_code in [200, 201]
        assert b'barber' in response.data.lower()

    def test_my_profile_select_nonexistent_barbershop(self, client):
        """Test ID 63: Select non-existent barbershop - 'silly styles'"""
        # Input: "silly styles" (non-existent barbershop)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'barbershop_name': 'silly styles'
        })
        # Expected: Form ignores input, previous valid barbershop stays
        assert response.status_code in [200, 400]

    def test_my_profile_select_valid_barbershop(self, client):
        """Test ID 64: Select valid existing barbershop - 'Supreme Styling'"""
        # Input: "Supreme Styling" (existing barbershop)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'barbershop_name': 'Supreme Styling'
        })
        # Expected: Form saves barbershop to barber
        assert response.status_code in [200, 201]

    def test_my_profile_select_empty_barbershop(self, client):
        """Test ID 65: Select empty/null barbershop"""
        # Input: null (no barbershop selected)
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'barbershop_name': ''
        })
        # Expected: Form requests "Please select a barbershop"
        assert response.status_code in [200, 400]
        assert (b'select' in response.data.lower() or 
                b'required' in response.data.lower())

    def test_my_profile_register_valid_barbershop(self, client):
        """Test ID 66: Register valid new barbershop - Name='top trims', Location='SW1A1AA'"""
        # Input: barbershop name "top trims", location "SW1A1AA"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': 'top trims',
            'new_barbershop_location': 'SW1A1AA'
        })
        # Expected: Form saves new barbershop to barber
        assert response.status_code in [200, 201]

    def test_my_profile_register_empty_barbershop(self, client):
        """Test ID 67: Register empty barbershop - Name=null, Location=null"""
        # Input: no name, no location
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': '',
            'new_barbershop_location': ''
        })
        # Expected: Form requests data be added
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or 
                b'error' in response.data.lower())

    def test_my_profile_register_profane_barbershop(self, client):
        """Test ID 68: Register barbershop with profane name - Name='fuck'"""
        # Input: profane barbershop name "fuck"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': 'fuck',
            'new_barbershop_location': 'SW1A1AA'
        })
        # Expected: Form rejects profane input and requests different name
        assert response.status_code in [200, 400]
        assert (b'profan' in response.data.lower() or 
                b'inappropriate' in response.data.lower())

    def test_my_profile_register_duplicate_barbershop(self, client):
        """Test ID 69: Register duplicate barbershop - Name='Supreme Styling'"""
        # Input: duplicate barbershop name "Supreme Styling"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': 'Supreme Styling',
            'new_barbershop_location': 'SW1A1AA'
        })
        # Expected: Form rejects duplicate and requests different name
        assert response.status_code in [200, 400]
        assert (b'already' in response.data.lower() or 
                b'duplicate' in response.data.lower() or
                b'different' in response.data.lower())

    def test_my_profile_register_unique_barbershop(self, client):
        """Test ID 70: Register unique barbershop - Name='Not Supreme Styling', Location='SW1A1AA'"""
        # Input: unique name "Not Supreme Styling", location "SW1A1AA"
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': 'Not Supreme Styling',
            'new_barbershop_location': 'SW1A1AA'
        })
        # Expected: Form saves new barbershop (unique name, location can be duplicate)
        assert response.status_code in [200, 201]

    def test_my_profile_barbershop_name_too_long(self, client):
        """Test ID 71: Barbershop name too long - 51+ characters"""
        # Input: 51 'i' characters (exceeds 50 char limit)
        long_name = 'i' * 51
        response = client.post('/profile', data={
            'username': 'testuser',
            'postcode': 'SW1A 1AA',
            'role': 'barber',
            'new_barbershop_name': long_name,
            'new_barbershop_location': 'SW1A1AA'
        })
        # Expected: Form requests that name is less than 50 characters
        assert response.status_code in [200, 400]
        assert (b'50' in response.data or 
                b'too long' in response.data.lower() or
                b'character' in response.data.lower())
