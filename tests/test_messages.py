"""Tests for messaging functionality."""


def test_messages_requires_login(client):
    """Test messages page requires authentication."""
    response = client.get('/messages/')
    assert response.status_code == 302


def test_messages_page(auth_client):
    """Test messages page loads when logged in."""
    response = auth_client.get('/messages/')
    assert response.status_code == 200
    assert b'Messages' in response.data


def test_compose_page(auth_client):
    """Test compose message page loads."""
    response = auth_client.get('/messages/compose')
    assert response.status_code == 200
    assert b'Message' in response.data


def test_send_message(auth_client, app):
    """Test sending a message."""
    response = auth_client.post('/messages/compose', data={
        'subject': 'Test Subject',
        'body': 'Test message body'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Message sent' in response.data


def test_view_message(auth_client, app):
    """Test viewing a message."""
    from app import db
    from app.models import Message, User

    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        message = Message(
            subject='View Test',
            body='Test body',
            sender_id=user.id
        )
        db.session.add(message)
        db.session.commit()
        message_id = message.id

    response = auth_client.get(f'/messages/{message_id}')
    assert response.status_code == 200
    assert b'View Test' in response.data
