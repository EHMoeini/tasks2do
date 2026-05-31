from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateTimeLocalField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Optional, ValidationError, Length
import re
from flask_ckeditor import CKEditorField
from datetime import datetime

def validate_password_structure(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit.')
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     raise ValidationError('Password must contain at least one special character.')

def task_deadline_validate(form, field):
    date = field.data
    if form.has_deadline.data:
        if not date:
            raise ValidationError('Deadline is required when "Has deadline" is checked.')
        if date < datetime.now():
            raise ValidationError('Deadline cannot be in the past.')

def space_validator(form, field):
    if " " in field.data:
        raise ValidationError("Spaces are not allowed.")

class RegisterForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Enter your username"}, validators=[DataRequired(), space_validator])
    password = PasswordField('Password', render_kw={"placeholder": "Enter your password"}, validators=[DataRequired(), validate_password_structure, space_validator])
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm your password"}, validators=[DataRequired(), EqualTo('password', message='Passwords must match.'), space_validator])
    submit = SubmitField('Reigster')

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Enter your username"}, validators=[DataRequired(), space_validator])
    password = PasswordField('Password', render_kw={"placeholder": "Enter your password"}, validators=[DataRequired(), space_validator])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField(
        'Task Title',
        render_kw={"placeholder": "Enter your task title"},
        validators=[
            Length(max=100, message="Title must be less than 100 characters."),
            DataRequired(message="Title is required.")
        ]
    )
    
    description = CKEditorField(
        'Description',
        render_kw={"placeholder": "Detailed description (optional)"},
        validators=[Optional()]
    )
    
    has_deadline = BooleanField('Has deadline', default=False)
    
    deadline = DateTimeLocalField(
        'Deadline',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional(), task_deadline_validate]
    )
    
    category = StringField(
        'Category',
        render_kw={"placeholder": "e.g., Work, Personal, Urgent"},
        validators=[Optional(), Length(max=50)]
    )
    
    submit = SubmitField('Create Task')