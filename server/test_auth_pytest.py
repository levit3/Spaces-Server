import json
import jwt
from config import app
from models import User
from datetime import datetime, timedelta
import pytest
from app import db

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(name='testuser', password='P@ssword123', email='testuser@example.com',
                        role='USER',
                        profile_picture="https://i.pinimg.com/236x/6c/74/25/6c74255c82ac875ba9321bb44757407f.jpg")
            db.session.add(user)
            db.session.commit()
        yield testing_client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_protected_route_expired_token(test_client):
    with app.app_context():
        user = User.query.filter_by(name='testuser').first()
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() - timedelta(days=1)  
        }, app.config['SECRET_KEY'], algorithm="HS256")
    
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = test_client.get(f'/api/users/{user.id}', headers=headers, follow_redirects=True)
        
        print(f"Final URL after redirects: {response.request.url}")
        print(f"Response data: {response.data}")
        
        assert response.status_code == 401
        assert b'Token expired' in response.data  
        
def test_protected_route_invalid_token(test_client):
    headers = {
        'Authorization': 'Bearer invalidtoken'
    }
    response = test_client.get('/api/users/1', headers=headers)
    assert response.status_code == 401

# Test accessing a protected route without a token
def test_protected_route_no_token(test_client):
    
    response = test_client.get('/api/users/1')
    assert response.status_code == 401


def test_protected_route_with_token(test_client):
    
    user = User.query.filter_by(name='testuser').first()
    token = jwt.encode({
        'id': user.id, 
        'expiration': str(datetime.utcnow() + timedelta(days=5))
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = test_client.get('/api/users/1', headers=headers)
    print(response.data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['name'] == 'testuser'






