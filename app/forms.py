from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """Form for parent registration."""
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    child_name = StringField("Child's Name", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    """Form for parent login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EventForm(FlaskForm):
    """Form for creating/editing events."""
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    date = DateField('Date', validators=[DataRequired()])
    event_type = SelectField('Event Type', choices=[
        ('general', 'General'),
        ('snack_duty', 'Snack Duty'),
        ('field_trip', 'Field Trip'),
        ('holiday', 'Holiday'),
        ('meeting', 'Parent Meeting')
    ])
    snack_duty_parent_id = SelectField('Snack Duty Parent', coerce=int, choices=[])


class MessageForm(FlaskForm):
    """Form for sending messages."""
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    body = TextAreaField('Message', validators=[DataRequired()])
