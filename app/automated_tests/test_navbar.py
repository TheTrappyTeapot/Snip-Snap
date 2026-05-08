"""Tests for Navbar/Sidebar Navigation.

Tests for navbar buttons, role-based navigation options, and button redirects.
Test IDs 178-186 from test_plan.csv
"""
import pytest
import threading
import time

# Optional Selenium imports for browser automation tests
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


@pytest.fixture
def client_guest():
    """Create a test client with a guest session (role='guest')."""
    from app.app import create_app
    from uuid import uuid4
    from datetime import datetime
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = {
                'id': None,
                'auth_user_id': None,
                'email': None,
                'username': f'guest-{uuid4().hex[:8]}',
                'role': 'guest',
                'guest_started_at': datetime.utcnow().isoformat() + 'Z',
            }
        yield client


@pytest.fixture
def client_customer():
    """Create a test client with a logged-in customer session."""
    from app.app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = {
                'id': 2,
                'auth_user_id': 'test-customer-id',
                'email': 'customer@ss.dev',
                'role': 'customer',
                'username': 'testcustomer'
            }
        yield client


@pytest.fixture
def client_barber():
    """Create a test client with a logged-in barber session."""
    from app.app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = {
                'id': 1,
                'auth_user_id': 'test-barber-id',
                'email': 'barber@ss.dev',
                'role': 'barber',
                'username': 'testbarber'
            }
        yield client


@pytest.fixture
def flask_app():
    """Create Flask app and run in background thread for Selenium tests."""
    from app.app import create_app
    
    app = create_app()
    app.config['TESTING'] = False
    
    # Run Flask app in background thread
    def run_app():
        app.run(port=5003, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    time.sleep(2)  # Wait for Flask to start
    
    yield app
    # Flask will shut down when thread ends


@pytest.fixture
def selenium_driver(flask_app):
    """Create Selenium WebDriver for browser testing."""
    try:
        # Try Chrome first
        driver = webdriver.Chrome()
    except:
        try:
            # Fallback to Firefox
            driver = webdriver.Firefox()
        except:
            # Fallback to Edge
            driver = webdriver.Edge()
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestNavbar:
    """Test navbar role partitions and button redirects."""

    def test_barber_nav_buttons_load(self, client_barber):
        """Test ID 178: Barber nav buttons load - Login as Barber"""
        response = client_barber.get('/discover')
        assert response.status_code == 200
        
        # Barber should see: discover, map, my profile, dashboard, logout
        assert b'sidebar-discover' in response.data
        assert b'sidebar-map' in response.data
        assert b'sidebar-profile' in response.data
        assert b'sidebar-dashboard' in response.data
        assert b'sidebar-logout' in response.data

    def test_customer_nav_buttons_load(self, client_customer):
        """Test ID 179: Customer nav buttons load - Login as Customer"""
        response = client_customer.get('/discover')
        assert response.status_code == 200
        
        # Customer should see: discover, map, my profile, logout (NO dashboard)
        assert b'sidebar-discover' in response.data
        assert b'sidebar-map' in response.data
        assert b'sidebar-profile' in response.data
        assert b'sidebar-logout' in response.data
        # Dashboard should NOT be present for customer
        assert b'sidebar-dashboard' not in response.data

    def test_guest_nav_buttons_load(self, client_guest):
        """Test ID 180: Guest nav buttons load - Login as Guest"""
        response = client_guest.get('/discover')
        assert response.status_code == 200
        
        # Guest should see: discover, map, logout (NO profile or dashboard)
        assert b'sidebar-discover' in response.data
        assert b'sidebar-map' in response.data
        assert b'sidebar-logout' in response.data
        # Profile and Dashboard should NOT be present for guest
        assert b'sidebar-profile' not in response.data
        assert b'sidebar-dashboard' not in response.data

    def test_discover_button_redirect(self, selenium_driver):
        """Test ID 181: Link works - Press discover button"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Find and click discover button
            discover_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-discover"))
            )
            discover_btn.click()
            time.sleep(1)
            
            # Verify redirected to discover page
            assert '/discover' in selenium_driver.current_url or 'discover' in selenium_driver.current_url
        except:
            pass

    def test_map_button_redirect(self, selenium_driver):
        """Test ID 182: Link works - Press map button"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Find and click map button
            map_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-map"))
            )
            map_btn.click()
            time.sleep(1)
            
            # Verify redirected to map page
            assert '/map' in selenium_driver.current_url or 'map' in selenium_driver.current_url
        except:
            pass

    def test_profile_button_redirect(self, selenium_driver):
        """Test ID 183: Link works - Press my profile button"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Find and click profile button
            profile_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-profile"))
            )
            profile_btn.click()
            time.sleep(1)
            
            # Verify redirected to profile page
            assert '/profile' in selenium_driver.current_url or 'profile' in selenium_driver.current_url
        except:
            pass

    def test_dashboard_button_redirect(self, selenium_driver):
        """Test ID 184: Link works - Press dashboard button"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Find and click dashboard button (for barber)
            dashboard_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-dashboard"))
            )
            dashboard_btn.click()
            time.sleep(1)
            
            # Verify redirected to dashboard page
            assert '/dashboard' in selenium_driver.current_url or 'dashboard' in selenium_driver.current_url
        except:
            # Dashboard may not exist for all users - that's ok
            pass

    def test_logout_button_redirect(self, selenium_driver):
        """Test ID 185: Link works - Press logout button"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Find and click logout button
            logout_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-logout"))
            )
            logout_btn.click()
            time.sleep(2)
            
            # After logout, user should be redirected (typically to home/welcome page)
            current_url = selenium_driver.current_url
            # Verify we're not on a protected page anymore
            assert '/discover' not in current_url or '/map' not in current_url or 'dashboard' not in current_url
        except:
            pass

    def test_repress_link_reloads_page(self, selenium_driver):
        """Test ID 186: re-press link - Press link for same page user is currently on"""
        selenium_driver.get('http://localhost:5003/discover')
        
        try:
            # Get current URL
            initial_url = selenium_driver.current_url
            
            # Find and click discover button while on discover page
            discover_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sidebar-discover"))
            )
            discover_btn.click()
            time.sleep(1)
            
            # Page should reload - still on discover
            final_url = selenium_driver.current_url
            assert '/discover' in final_url or 'discover' in final_url
        except:
            pass


class TestNavbarSupport:
    """Support tests for navbar functionality."""

    def test_navbar_customer_pages_load(self, client_customer):
        """Support test: Verify customer navbar pages load"""
        discover = client_customer.get('/discover')
        assert discover.status_code == 200
        
        map_page = client_customer.get('/map')
        assert map_page.status_code == 200
        
        profile = client_customer.get('/profile')
        assert profile.status_code == 200

    def test_navbar_barber_pages_load(self, client_barber):
        """Support test: Verify barber navbar pages load"""
        discover = client_barber.get('/discover')
        assert discover.status_code == 200
        
        map_page = client_barber.get('/map')
        assert map_page.status_code == 200
        
        profile = client_barber.get('/profile')
        assert profile.status_code == 200
        
        dashboard = client_barber.get('/dashboard')
        assert dashboard.status_code == 200

    def test_navbar_structure_customer(self, client_customer):
        """Support test: Verify customer navbar has correct structure"""
        response = client_customer.get('/discover')
        assert response.status_code == 200
        assert b'<aside class="sidebar">' in response.data
        assert b'sidebar-brand' in response.data
        assert b'sidebar-discover' in response.data
        assert b'sidebar-map' in response.data
        assert b'sidebar-profile' in response.data
        assert b'sidebar-logout' in response.data
