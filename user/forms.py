from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError

from user.models import User

class RegisterForm(Form):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
        ]
    )

    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')
    
    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email is already in use")