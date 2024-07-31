import pytest
from datetime import datetime, timedelta
from app import app, db
from models import User
import jwt

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Initialize the database here if needed
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def test_user():
    user = User(username='testuser', password='password123')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def expired_token(test_user):
    return jwt.encode(
        {'id': test_user.id, 'exp': datetime.utcnow() - timedelta(minutes=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def test_expired_token(client, expired_token):
    response = client.get('/api/users/1', headers={'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert b'Token expired' in response.data

