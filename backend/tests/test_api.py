"""
Basic API tests for GameVault
"""
import pytest
from app import create_app
from models import db, User, Category, Product


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Seed test categories
        categories = [
            Category(name='items', description='Game Items', icon='⚔️'),
            Category(name='accounts', description='Game Accounts', icon='👤'),
            Category(name='currency', description='In-Game Currency', icon='💰')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_index(client):
    """Test index endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'GameVault API' in response.json['name']


def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'role': 'buyer'
    })
    
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert response.json['user']['username'] == 'testuser'


def test_login_user(client):
    """Test user login"""
    # Register user first
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'role': 'buyer'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_get_categories(client):
    """Test getting categories"""
    response = client.get('/api/categories')
    
    assert response.status_code == 200
    assert len(response.json['categories']) == 3


def test_get_products(client):
    """Test getting products"""
    response = client.get('/api/products')
    
    assert response.status_code == 200
    assert 'products' in response.json


if __name__ == '__main__':
    pytest.main([__file__])
