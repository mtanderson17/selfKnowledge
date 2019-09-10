
from flask import Blueprint, render_template, request, redirect, session, url_for,abort
import bcrypt

from application import db
from user.models import User, Habit
from user.forms import RegisterForm, LoginForm, HabitForm
from user.decorators import login_required

user_app = Blueprint('user_app', __name__)

@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        user = User(
            password=hashed_password.decode('utf-8'),
            email=form.email.data
            )
        db.session.add(user)
        db.session.commit()
       
        new_user = User.query.filter_by(email=form.email.data).first().email
        return f'{new_user} registered'
    return render_template('user/register.html', form=form)

@user_app.route('/login', methods=('GET', 'POST'))
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
    return render_template('user/login.html', form=form, error=error)
    
@user_app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('username')
    return redirect(url_for('user_app.login'))
    
@user_app.route('/profile', methods=('GET', 'POST'))
def profile():
    return render_template('user/profile.html')

@user_app.route('/add_habit', methods=('GET', 'POST'))
@login_required
def add_habit():
    error = None
    message = None
    user = User.query.filter_by(email=session.get('username')).first()

    form = HabitForm()

    if form.validate_on_submit():

        habit = Habit(
            user_id = user.id,
            habit_name = form.habit.data
        )

        db.session.add(habit)
        db.session.commit()

        return  render_template("user/add_habit.html", form=form, error=error, message=message, user=user)
    return render_template('user/add_habit.html', form=form,user=user,message=message,error=error)
