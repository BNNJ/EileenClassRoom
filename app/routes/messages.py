from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Message
from app.forms import MessageForm

bp = Blueprint('messages', __name__, url_prefix='/messages')


@bp.route('/')
@login_required
def list_messages():
    """List all broadcast messages."""
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('messages/list.html', messages=messages)


@bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    """Compose and send a new message."""
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            subject=form.subject.data,
            body=form.body.data,
            sender_id=current_user.id,
            is_broadcast=True
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent to all parents!', 'success')
        return redirect(url_for('messages.list_messages'))

    return render_template('messages/compose.html', form=form)


@bp.route('/<int:message_id>')
@login_required
def view_message(message_id):
    """View a specific message."""
    message = Message.query.get_or_404(message_id)
    return render_template('messages/view.html', message=message)


@bp.route('/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Delete a message."""
    message = Message.query.get_or_404(message_id)
    if message.sender_id != current_user.id and not current_user.is_admin:
        flash('You can only delete messages you sent.', 'error')
        return redirect(url_for('messages.list_messages'))

    db.session.delete(message)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('messages.list_messages'))
