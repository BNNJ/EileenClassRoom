from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Event, Message, User
from datetime import date

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page with overview."""
    if current_user.is_authenticated:
        today = date.today()
        upcoming_events = Event.query.filter(Event.date >= today)\
            .order_by(Event.date).limit(5).all()
        recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
        parent_count = User.query.count()
        return render_template('main/dashboard.html',
                               upcoming_events=upcoming_events,
                               recent_messages=recent_messages,
                               parent_count=parent_count)
    return render_template('main/index.html')


@bp.route('/parents')
@login_required
def parents():
    """List all parents in the classroom."""
    all_parents = User.query.order_by(User.name).all()
    return render_template('main/parents.html', parents=all_parents)
