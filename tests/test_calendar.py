"""Tests for calendar functionality."""
from datetime import date


def test_calendar_requires_login(client):
    """Test calendar page requires authentication."""
    response = client.get('/calendar/')
    assert response.status_code == 302


def test_calendar_page(auth_client):
    """Test calendar page loads when logged in."""
    response = auth_client.get('/calendar/')
    assert response.status_code == 200
    assert b'Calendar' in response.data or b'Sun' in response.data


def test_create_event_page(auth_client):
    """Test create event page loads."""
    response = auth_client.get('/calendar/create')
    assert response.status_code == 200
    assert b'Create' in response.data


def test_create_event(auth_client, app):
    """Test creating an event."""
    response = auth_client.post('/calendar/create', data={
        'title': 'Test Event',
        'description': 'Test description',
        'date': date.today().isoformat(),
        'event_type': 'general',
        'snack_duty_parent_id': 0
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Event created' in response.data


def test_snack_duty_page(auth_client):
    """Test snack duty page loads."""
    response = auth_client.get('/calendar/snack-duty')
    assert response.status_code == 200
    assert b'Snack Duty' in response.data
