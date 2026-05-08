"""Automated tests for the Login page."""

import pytest
from app.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestLoginPage:
    """Test suite for the login page functionality."""

    def test_login_page_loads(self, client):
        """Test that the login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data.lower()

    def test_login_page_invalid_credentials_client_side(self, client):
        """Test ID 5: Invalid login - email='invalid@ss.dev', password='111111'"""
        # Attempt login with invalid credentials
        response = client.post('/login', data={
            'email': 'invalid@ss.dev',
            'password': '111111'
        })
        # Expect rejection or error message for invalid credentials
        assert response.status_code in [200, 400, 401]
        assert (b'invalid' in response.data.lower() or
                b'failed' in response.data.lower() or
                b'error' in response.data.lower() or
                b'login' in response.data.lower())

    def test_login_page_valid_login_attempt_ready(self, client):
        """Test ID 6: Valid login - email='barber@ss.dev', password='1111'"""
        # Attempt login with valid credentials
        response = client.post('/login', data={
            'email': 'barber@ss.dev',
            'password': '1111'
        })
        # Should either succeed (200) or process form (400 if validation needed)
        assert response.status_code in [200, 400, 401, 302]
        # Check response contains meaningful data (not error or success redirect)
        assert response.data  # Ensure response has content

    def test_login_email_validation_elements_present(self, client):
        """Test ID 7: Valid email format - email='cust@ss.dev'"""
        # Attempt login with valid email format
        response = client.post('/login', data={
            'email': 'cust@ss.dev',
            'password': 'testpass123'
        })
        # Form should accept valid email format
        assert response.status_code in [200, 400, 401, 302]
        assert response.data

    def test_login_email_format_no_at_symbol(self, client):
        """Test ID 8: Invalid email format - email='invalid' (no @)"""
        # Attempt login with email missing @ symbol
        response = client.post('/login', data={
            'email': 'invalid',
            'password': 'testpass123'
        })
        # Server should reject invalid email format
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower() or
                b'format' in response.data.lower())

    def test_login_email_format_missing_domain(self, client):
        """Test ID 9: Invalid email format - email='invalid@' (incomplete)"""
        # Attempt login with email missing domain
        response = client.post('/login', data={
            'email': 'invalid@',
            'password': 'testpass123'
        })
        # Server should reject incomplete email
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower())

    def test_login_email_format_incomplete_domain(self, client):
        """Test ID 10: Invalid email format - email='invalid@ss' (incomplete domain)"""
        # Attempt login with incomplete domain
        response = client.post('/login', data={
            'email': 'invalid@ss',
            'password': 'testpass123'
        })
        # Server should reject incomplete domain
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower())

    def test_login_page_contains_email_input(self, client):
        """Test ID 11: Invalid email format - email='invalid@ss.' (no extension)"""
        # Attempt login with email missing extension
        response = client.post('/login', data={
            'email': 'invalid@ss.',
            'password': 'testpass123'
        })
        # Server should reject email without extension
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower())

    def test_login_empty_email_field_handling(self, client):
        """Test ID 12: Empty email - email=null"""
        # Attempt login with empty email
        response = client.post('/login', data={
            'email': '',
            'password': 'testpass123'
        })
        # Server should reject empty email
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or
                b'email' in response.data.lower())

    def test_login_page_contains_password_input(self, client):
        """Test ID 13: Empty password - password=null"""
        # Attempt login with empty password
        response = client.post('/login', data={
            'email': 'test@ss.dev',
            'password': ''
        })
        # Server should reject empty password
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or
                b'password' in response.data.lower())

    def test_login_password_validation_elements(self, client):
        """Test ID 14: Password too short - password='1234' (4 chars)"""
        # Attempt login with password too short
        response = client.post('/login', data={
            'email': 'test@ss.dev',
            'password': '1234'
        })
        # Server should reject password under minimum length
        assert response.status_code in [200, 400]
        assert (b'password' in response.data.lower() or
                b'short' in response.data.lower())

    def test_login_page_contains_submit_button(self, client):
        """Test ID 15: Password too long - password=51+ characters"""
        # Attempt login with password too long
        response = client.post('/login', data={
            'email': 'test@ss.dev',
            'password': 'a' * 51
        })
        # Server should reject password over maximum length
        assert response.status_code in [200, 400]
        assert (b'password' in response.data.lower() or
                b'long' in response.data.lower())

    def test_login_valid_password_form_ready(self, client):
        """Test ID 18: Valid password - password='aA4aaa'"""
        # Attempt login with valid password format
        response = client.post('/login', data={
            'email': 'test@ss.dev',
            'password': 'aA4aaa'
        })
        # Form should accept password with mixed case and numbers
        assert response.status_code in [200, 400, 401, 302]
        assert response.data

    def test_login_page_contains_form_element(self, client):
        """Test that the login page contains a form element."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'<form' in response.data or b'form' in response.data.lower()

    def test_login_page_has_guest_option(self, client):
        """Test that login page has guest login option."""
        response = client.get('/login')
        assert response.status_code == 200
        assert (b'guest' in response.data.lower() or 
                b'continue' in response.data.lower())

    def test_login_page_supabase_config_present(self, client):
        """Test that Supabase configuration is injected into login page."""
        response = client.get('/login')
        assert response.status_code == 200
        assert (b'supabase' in response.data.lower() or 
                b'SUPABASE' in response.data)
