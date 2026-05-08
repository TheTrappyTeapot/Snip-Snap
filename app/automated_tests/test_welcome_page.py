"""Automated tests for the Welcome page."""

import pytest
from app.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestWelcomePage:
    """Test suite for the welcome page navigation."""

    def test_welcome_page_loads(self, client):
        """Test that the welcome page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Snip-Snap' in response.data

    def test_go_to_login_page(self, client):
        """
        Test ID 1: Navigate to login page
        Partition: Navigation
        Input: Click "Login" button
        Expected: HTTP 200 transfer to login page with form elements
        """
        # Attempt to navigate to login page
        response = client.get('/login')
        assert response.status_code == 200
        # Verify login page content is present
        assert (b'Login' in response.data or 
                b'login' in response.data.lower() or
                b'email' in response.data.lower())

    def test_go_to_signup_page(self, client):
        """
        Test ID 2: Navigate to signup page
        Partition: Navigation
        Input: Click "Sign up" button
        Expected: HTTP 200 transfer to signup page with form elements
        """
        # Attempt to navigate to signup page
        response = client.get('/signup')
        assert response.status_code == 200
        # Verify signup page content is present
        assert (b'Sign up' in response.data or 
                b'signup' in response.data.lower() or 
                b'Signup' in response.data or
                b'email' in response.data.lower())

    def test_continue_as_guest(self, client):
        """
        Test ID 3: Continue as guest with redirect
        Partition: Navigation
        Input: Click "Continue as guest" button
        Expected: HTTP 302/303 redirect to discover page
        """
        # Send POST request to guest/start endpoint (no follow redirects)
        response = client.post('/guest/start', follow_redirects=False)
        
        # Should return redirect status code
        assert response.status_code in [302, 303]
        # Verify redirect location points to discover page
        assert '/discover' in response.location or response.location.endswith('/discover')

    def test_continue_as_guest_with_redirect(self, client):
        """
        Test ID 4: Guest session creation and redirect completion
        Partition: Navigation
        Input: Click "Continue as guest" and follow redirect flow
        Expected: Successfully reach discover page (HTTP 200) with guest role
        """
        # Send POST request to guest/start endpoint with follow redirects enabled
        response = client.post('/guest/start', follow_redirects=True)
        
        # Should successfully reach discover page
        assert response.status_code == 200
        # Verify discover page content is rendered
        assert (b'discover' in response.data.lower() or 
                b'Discover' in response.data or 
                b'DISCOVER' in response.data)
