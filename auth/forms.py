from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError

from application import db
from user.models import User

class RegisterForm(FlaskForm):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
        ]
    )

    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')
    
    def validate_email(form, field):
        if bool(User.query.filter_by(email=field.data).first()):
            raise ValidationError("Email is already in use")

class LoginForm(FlaskForm):
    email = EmailField('Email', [
        validators.DataRequired()
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
        ])

