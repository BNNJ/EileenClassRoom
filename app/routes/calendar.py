from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Event, User
from app.forms import EventForm
from datetime import date
import calendar as cal

bp = Blueprint('calendar', __name__, url_prefix='/calendar')


@bp.route('/')
@bp.route('/<int:year>/<int:month>')
@login_required
def view(year=None, month=None):
    """Display the calendar with events."""
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    first_day = date(year, month, 1)
    last_day_num = cal.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)

    events = Event.query.filter(
        Event.date >= first_day,
        Event.date <= last_day
    ).order_by(Event.date).all()

    events_by_date = {}
    for event in events:
        day = event.date.day
        if day not in events_by_date:
            events_by_date[day] = []
        events_by_date[day].append(event)

    calendar_data = cal.Calendar(firstweekday=6)
    month_days = calendar_data.monthdayscalendar(year, month)
    month_name = cal.month_name[month]

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template('calendar/view.html',
                           year=year,
                           month=month,
                           month_name=month_name,
                           month_days=month_days,
                           events_by_date=events_by_date,
                           today=today,
                           prev_month=prev_month,
                           prev_year=prev_year,
                           next_month=next_month,
                           next_year=next_year)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new event."""
    form = EventForm()
    parents = User.query.order_by(User.name).all()
    form.snack_duty_parent_id.choices = [(0, 'None')] + [(p.id, f"{p.name} ({p.child_name})") for p in parents]

    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            event_type=form.event_type.data,
            created_by=current_user.id
        )
        if form.snack_duty_parent_id.data and form.snack_duty_parent_id.data != 0:
            event.snack_duty_parent_id = form.snack_duty_parent_id.data

        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('calendar.view'))

    return render_template('calendar/create.html', form=form)


@bp.route('/event/<int:event_id>')
@login_required
def event_detail(event_id):
    """View event details."""
    event = Event.query.get_or_404(event_id)
    return render_template('calendar/event.html', event=event)


@bp.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete an event."""
    event = Event.query.get_or_404(event_id)
    if event.created_by != current_user.id and not current_user.is_admin:
        flash('You can only delete events you created.', 'error')
        return redirect(url_for('calendar.view'))

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('calendar.view'))


@bp.route('/snack-duty')
@login_required
def snack_duty():
    """View snack duty schedule."""
    today = date.today()
    snack_events = Event.query.filter(
        Event.event_type == 'snack_duty',
        Event.date >= today
    ).order_by(Event.date).all()

    return render_template('calendar/snack_duty.html', snack_events=snack_events)
