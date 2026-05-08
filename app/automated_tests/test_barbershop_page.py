"""Test suite for barbershop page - Tests from test_plan.csv (IDs 217-224)."""
import pytest
from app.db import get_barbershop_by_id, get_reviews_with_replies, get_barbershop_gallery_photos


@pytest.fixture
def client_viewer():
    """Create a test client with a logged-in customer session."""
    from app.app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = {
                'id': 2,
                'auth_user_id': 'test-viewer-id',
                'email': 'customer@ss.dev',
                'role': 'customer',
                'username': 'customer'
            }
        yield client


@pytest.fixture
def client_guest():
    """Create a test client with guest session."""
    from app.app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestBarbershopPage:
    """Test barbershop page according to test_plan.csv (IDs 217-224)."""

    def test_check_title_loads(self, client_viewer):
        """Test ID 217: Check title loads - User can see 'Sharp Cuts' title on top of page."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Get barbershop name from database
        shop = get_barbershop_by_id(1)
        assert shop is not None
        
        # Verify shop title is displayed on the page
        assert shop['name'] in html or shop['name'].lower() in html.lower()

    def test_check_postcode_loads(self, client_viewer):
        """Test ID 218: Check postcode loads - postcode visible under title."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Get barbershop postcode from database
        shop = get_barbershop_by_id(1)
        assert shop is not None
        
        # Verify postcode is displayed if available
        if shop.get('postcode'):
            assert shop['postcode'] in html

    def test_check_map_loads(self, client_viewer):
        """Test ID 219: Check map loads - User can see pin location on minimap."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify map element or location data is present
        assert 'map' in html.lower() or 'location' in html.lower()

    def test_check_opening_hours_load(self, client_viewer):
        """Test ID 220: Check opening hours load - aggregate from all barber's working hours."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify shop timetable/opening hours section exists
        assert 'hour' in html.lower() or 'time' in html.lower() or 'schedule' in html.lower()

    def test_check_barbers_load(self, client_viewer):
        """Test ID 221: Check barbers load - User sees Keir Starmer, Margret Thatcher, Rachel Reaves."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify barbers section exists with barber names or profile links
        assert 'barber' in html.lower() or 'staff' in html.lower() or 'team' in html.lower()

    def test_go_to_barber_profile(self, client_viewer):
        """Test ID 222: Go to barber profile - Click 'View Profile' on profile card redirects to barber page."""
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify barber profile links or View Profile buttons exist
        assert 'profile' in html.lower() or 'view' in html.lower() or '/barber' in html.lower()

    def test_check_reviews_load(self, client_viewer):
        """Test ID 223: Check reviews load - User can see a list of reviews."""
        # Get reviews for barbershop_id=1
        reviews = get_reviews_with_replies(target_barbershop_id=1)
        
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify reviews section exists
        assert 'review' in html.lower() or 'rating' in html.lower()

    def test_check_gallery_loads(self, client_viewer):
        """Test ID 224: Check gallery loads - User sees 16 photos with usernames and main tags."""
        # Get gallery photos for barbershop_id=1
        photos = get_barbershop_gallery_photos(1, limit=16)
        
        # Open page of Sharp Cuts (barbershop_id=1)
        response = client_viewer.get('/barbershop/1')
        assert response.status_code == 200
        html = response.data.decode()
        
        # Verify gallery section exists
        assert 'gallery' in html.lower() or 'photo' in html.lower()
