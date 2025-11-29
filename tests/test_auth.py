"""Tests for authentication."""


def test_home_page(client):
    """Test home page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Eileen's Classroom" in response.data


def test_login_page(client):
    """Test login page loads."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_page(client):
    """Test registration page loads."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Registration' in response.data


def test_register_user(client, app):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'name': 'New Parent',
        'email': 'new@example.com',
        'child_name': 'New Child',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data


def test_login_logout(client, app):
    """Test login and logout."""
    from app import db
    from app.models import User

    with app.app_context():
        user = User(
            email='login@example.com',
            name='Login Test',
            child_name='Test Child'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'login@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Welcome' in response.data

    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data


def test_invalid_login(client):
    """Test invalid login credentials."""
    response = client.post('/auth/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
