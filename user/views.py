
from flask import Blueprint, render_template
import bcrypt

from application import db
from user.models import User
from user.forms import RegisterForm

user_app = Blueprint('user_app', __name__)

@user_app.route('/login')
def login():
    return "User login"
    
@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        user = User(
            password=hashed_password,
            email=form.email.data
            )
        db.session.add(user)
        db.session.commit()
        #New user doesn't appear to be returning anything
        new_user = User.query.filter_by(email=form.email.data).first().email
        return f'{new_user} registered'
    return render_template('user/register.html', form=form)