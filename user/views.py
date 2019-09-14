
from flask import Blueprint, render_template, request, redirect, session, url_for,abort, flash
import bcrypt
import calendar
import datetime

from application import db
from user.models import User, Habit
from user.forms import RegisterForm, LoginForm, HabitForm
from user.decorators import login_required, confirmation_required

user_app = Blueprint('user_app', __name__)

#DATETIME CONFIG - is this the best place to put it?
now = datetime.datetime.now()
year = now.year
month = now.month

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

@user_app.route('/profile')
@user_app.route('/profile/<year>/<month>', methods=('GET', 'POST'))
def profile(year=None,month=None):

    if year is None or month is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

    year = int(year)
    month = int(month)

    cal = calendar.HTMLCalendar().formatmonth(year,month)

    return render_template('user/profile.html', calendar = cal)

@user_app.route('/add_habit', methods=('GET', 'POST'))
@login_required
def add_habit(message=None):
    error = None
  
    user = User.query.filter_by(email=session.get('username')).first()
    habits = Habit.query.filter_by(user_id=user.id).all()
    habits_list = [habit.habit_name for habit in habits]
    form = HabitForm()

    if form.validate_on_submit():
        new_habit_name = form.habit_name.data.lower()
        if new_habit_name in habits_list:
            error = f'habit {new_habit_name} exists'
            return  render_template("user/add_habit.html", form=form, error=error, message=message,habits=habits )

        habit = Habit(
            user_id = user.id,
            habit_name = new_habit_name
        )
        db.session.add(habit)
        db.session.commit()

        
        message =  f'added {new_habit_name} successfully'
        new_habits = Habit.query.filter_by(user_id=user.id).all()

        return  render_template("user/add_habit.html",form=form,error=error,message=message,habits=new_habits)
    return render_template('user/add_habit.html', form=form,message=message,error=error, habits=habits)

@user_app.route('/delete_habit/<habit>',methods=('GET','POST'))
@login_required
def delete_habit(habit):
    error = None
    message = None
    user = User.query.filter_by(email=session.get('username')).first()
    del_habit = Habit.query.filter_by(user_id=user.id, habit_name=habit).first()

    db.session.delete(del_habit)
    db.session.commit()
    
    return redirect(url_for('user_app.add_habit',message=f'{habit} deleted'))

@user_app.route("/day/<year>/<month>/<day>")
@login_required
def day(day,month,year):
    


    return "test"