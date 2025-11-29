from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


def utc_now():
    """Return current UTC time with timezone awareness."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """Parent/User model for authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    child_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    events = db.relationship('Event', backref='creator', lazy='dynamic',
                             foreign_keys='Event.created_by')
    messages_sent = db.relationship('Message', backref='sender', lazy='dynamic')
    snack_duties = db.relationship('Event', backref='snack_parent', lazy='dynamic',
                                   foreign_keys='Event.snack_duty_parent_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Event(db.Model):
    """Calendar event model."""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, index=True)
    event_type = db.Column(db.String(50), default='general')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    snack_duty_parent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f'<Event {self.title} on {self.date}>'


class Message(db.Model):
    """Message model for broadcasts between parents."""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    is_broadcast = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Message {self.subject}>'
