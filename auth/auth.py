from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from application import db
from auth.forms import RegisterForm, LoginForm
from user.models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=('POST','GET'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login',methods=('GET','POST'))
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data): 
            error = 'Please check your login details and try again'
        else:
            login_user(user)
            return redirect(url_for('user_app.profile'))

    return render_template('auth/login.html', form=form, error=error)
    

@auth.route('/logout',methods=('GET','POST'))
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

'''
@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    
    #What does this do?
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')
        
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
            ).first()
        if user:
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['username'] = form.email.data
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('user_app.profile'))
            else:
                user = None
        if not user:
            error = 'Incorrect credentials'
    return render_template('auth/login.html', form=form, error=error)
    
@auth.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('username')
    return redirect(url_for('auth.login'))
'''