"""Tests for models."""
from datetime import date


def test_user_password_hashing(app):
    """Test password hashing works correctly."""
    from app.models import User

    user = User(
        email='hash@example.com',
        name='Hash Test',
        child_name='Test Child'
    )
    user.set_password('mypassword')

    assert user.password_hash != 'mypassword'
    assert user.check_password('mypassword')
    assert not user.check_password('wrongpassword')


def test_user_repr(app):
    """Test user string representation."""
    from app.models import User

    user = User(email='repr@example.com', name='Test', child_name='Child')
    assert 'repr@example.com' in repr(user)


def test_event_repr(app):
    """Test event string representation."""
    from app.models import Event
    from app import db

    with app.app_context():
        from app.models import User
        user = User(email='event@example.com', name='Test', child_name='Child')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        event = Event(
            title='Test Event',
            date=date.today(),
            created_by=user.id
        )
        assert 'Test Event' in repr(event)


def test_message_repr(app):
    """Test message string representation."""
    from app.models import Message
    from app import db

    with app.app_context():
        from app.models import User
        user = User(email='msg@example.com', name='Test', child_name='Child')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        message = Message(
            subject='Test Subject',
            body='Test body',
            sender_id=user.id
        )
        assert 'Test Subject' in repr(message)
