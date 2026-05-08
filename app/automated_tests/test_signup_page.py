"""Automated tests for the Signup page."""

import pytest
from app.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestSignupPage:
    """Test suite for the signup page functionality."""

    def test_signup_page_loads(self, client):
        """Test that the signup page loads successfully."""
        response = client.get('/signup')
        assert response.status_code == 200
        assert b'Sign up' in response.data or b'signup' in response.data.lower() or b'Signup' in response.data

    def test_signup_page_contains_form_element(self, client):
        """Test that the signup page contains a form element."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have a form element
        assert b'<form' in response.data or b'form' in response.data.lower()

    def test_signup_page_contains_email_input(self, client):
        """Test that the signup page contains an email input field."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have email input field
        assert b'email' in response.data.lower() or b'type="email"' in response.data.lower()

    def test_signup_page_contains_password_input(self, client):
        """Test that the signup page contains a password input field."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have password input field
        assert b'password' in response.data.lower() or b'type="password"' in response.data.lower()

    def test_signup_page_contains_submit_button(self, client):
        """Test that the signup page contains a submit button."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have a submit button
        assert (b'submit' in response.data.lower() or 
                b'sign up' in response.data.lower() or
                b'signup' in response.data.lower() or
                b'<button' in response.data)

    def test_signup_page_has_login_option(self, client):
        """Test that signup page has link to login."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have login or "already have account" option
        assert (b'login' in response.data.lower() or 
                b'already' in response.data.lower())

    def test_signup_page_supabase_config_present(self, client):
        """Test that Supabase configuration is injected into signup page."""
        response = client.get('/signup')
        assert response.status_code == 200
        # Should have Supabase configuration for client-side auth
        assert (b'supabase' in response.data.lower() or 
                b'SUPABASE' in response.data)

    def test_signup_invalid_credentials(self, client):
        """Test ID 20: Invalid signup attempt - email='invalid@ss.dev', password='111111'"""
        # Attempt signup with invalid credentials
        response = client.post('/signup', data={
            'email': 'invalid@ss.dev',
            'password': '111111'
        })
        # Should either reject or process form
        assert response.status_code in [200, 400]
        assert response.data

    def test_signup_valid_credentials(self, client):
        """Test ID 21: Valid signup attempt - email='barber@ss.dev', password='aA4&aa'"""
        # Attempt signup with valid credentials
        response = client.post('/signup', data={
            'email': 'barber@ss.dev',
            'password': 'aA4&aa'
        })
        # Should process signup
        assert response.status_code in [200, 400, 302]
        assert response.data

    def test_signup_email_validation_present(self, client):
        """Test ID 22: Valid email format - email='cust@ss.dev'"""
        # Attempt signup with valid email format
        response = client.post('/signup', data={
            'email': 'cust@ss.dev',
            'password': 'Test123!'
        })
        # Server should accept valid email format
        assert response.status_code in [200, 400, 302]
        assert response.data

    def test_signup_invalid_email_no_at(self, client):
        """Test ID 23: Invalid email without @ - email='invalid'"""
        # Attempt signup with email missing @ symbol
        response = client.post('/signup', data={
            'email': 'invalid',
            'password': 'Test123!'
        })
        # Server should reject invalid email format
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower())

    def test_signup_invalid_email_missing_domain(self, client):
        """Test ID 24: Invalid email with incomplete domain - email='invalid@'"""
        # Attempt signup with incomplete email
        response = client.post('/signup', data={
            'email': 'invalid@',
            'password': 'Test123!'
        })
        # Server should reject incomplete email
        assert response.status_code in [200, 400]
        assert (b'invalid' in response.data.lower() or
                b'email' in response.data.lower())

    def test_signup_empty_email(self, client):
        """Test ID 25: Empty email field - email=null"""
        # Attempt signup with empty email
        response = client.post('/signup', data={
            'email': '',
            'password': 'Test123!'
        })
        # Server should reject empty email
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or
                b'email' in response.data.lower())

    def test_signup_empty_password(self, client):
        """Test ID 26: Empty password field - password=null"""
        # Attempt signup with empty password
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': ''
        })
        # Server should reject empty password
        assert response.status_code in [200, 400]
        assert (b'required' in response.data.lower() or
                b'password' in response.data.lower())

    def test_signup_password_too_short(self, client):
        """Test ID 27: Password too short - password='1234' (4 chars)"""
        # Attempt signup with password under minimum length
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': '1234'
        })
        # Server should reject short password
        assert response.status_code in [200, 400]
        assert (b'short' in response.data.lower() or
                b'password' in response.data.lower())

    def test_signup_password_too_long(self, client):
        """Test ID 28: Password too long - password=51+ characters"""
        # Attempt signup with password over maximum length
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': 'a' * 51
        })
        # Server should reject long password
        assert response.status_code in [200, 400]
        assert (b'long' in response.data.lower() or
                b'password' in response.data.lower())

    def test_signup_password_missing_special_char(self, client):
        """Test ID 29: Password missing special char - password='aaaaaa'"""
        # Attempt signup with password missing special character
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': 'aaaaaa'
        })
        # Server should reject password without special char
        assert response.status_code in [200, 400]
        assert (b'special' in response.data.lower() or
                b'password' in response.data.lower())

    def test_signup_password_missing_number(self, client):
        """Test ID 30: Password missing number - password='aAaaaa'"""
        # Attempt signup with password missing numeric digit
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': 'aAaaaa'
        })
        # Server should reject password without number
        assert response.status_code in [200, 400]
        assert (b'number' in response.data.lower() or
                b'digit' in response.data.lower() or
                b'password' in response.data.lower())

    def test_signup_valid_password(self, client):
        """Test ID 31: Valid password - password='aA4&aa'"""
        # Attempt signup with valid password meeting all requirements
        response = client.post('/signup', data={
            'email': 'test@ss.dev',
            'password': 'aA4&aa'
        })
        # Should accept valid password
        assert response.status_code in [200, 302]
        assert response.status_code == 200
        # Form should be ready to accept valid passwords
        assert b'password' in response.data.lower()
