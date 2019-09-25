
from flask import Blueprint, render_template, request, redirect, session, url_for,abort, flash
import bcrypt
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

from application import db
from user.models import User, Habit,Day
from user.forms import RegisterForm, LoginForm, HabitForm,DayForm
from user.decorators import login_required, confirmation_required
from utilities.common import get_monthdelta_ints

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

@user_app.route('/profile')
@user_app.route('/profile/<year>/<month>', methods=('GET', 'POST'))
def profile(year=None,month=None):

    if year is None or month is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

    year = int(year)
    month = int(month)

    #Values for next and previous button
    date = datetime.date(year,month,1)
    _,prev_month,prev_year = get_monthdelta_ints(date,months=-1)
    _,next_month,next_year = get_monthdelta_ints(date,months=1)
    

    cal = calendar.HTMLCalendar().formatmonth(year,month)
    soup = BeautifulSoup(cal, 'html.parser')
    for td in soup('td'):
        try:
            day = int(td.text)
            url = f"/day/{year}/{month}/{day}"
            day_url_tag = soup.new_tag("a",href=url)
            day_url_tag.string = str(day) #value of the date, may want to change this to whole td later
            td.string.replace_with(day_url_tag) # take '1' and replace with <a href=url> 1 </a>
        except:
            pass
    html_cal = str(soup.prettify('utf-8',formatter=None))
    html_cal = html_cal[2:-1] #replace the b'' not sure why thats there
    html_cal = html_cal.replace("\\n","")
    html_cal = html_cal.replace("\\","")

    return render_template('user/profile.html', calendar = html_cal,month=month,year=year, prev_month = prev_month, 
    prev_year = prev_year,next_month=next_month,next_year=next_year)

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

@user_app.route("/day/<year>/<month>/<day_value>",methods=("GET","POST"))
@login_required
def day(year,month,day_value):
    error = None
    message = None
    form = DayForm()

    date = datetime.date(int(year),int(month),int(day_value))

    #Values for next and previous button
    prev_day,prev_month,prev_year = get_monthdelta_ints(date,days=-1)
    next_day,next_month,next_year = get_monthdelta_ints(date,days=1)

    #Get user and habits
    user = User.query.filter_by(email=session.get('username')).first()
    habits = Habit.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        habit_id = request.form.get("habit_id") #form hidden input

        #Updating day by deleting record and writing new one, probably better way to do this
        day_info = Day.query.filter_by(user_id=user.id,habit_id = habit_id, date=date).first()
        if day_info:
            db.session.delete(day_info)
            db.session.commit()

        day = Day(
            date = date,
            habit_id = habit_id,
            user_id = user.id,
            habit_complete = form.habit_complete.data,
            day_desc = form.day_desc.data
        )
        db.session.add(day)
        db.session.commit()

        return redirect(url_for("user_app.day",day_value=day_value,month=month,year=year))
    
   
    #if there is already information in days then prepopulate forms
    form_dict = {}
    for habit in habits:
        dayinfo = Day.query.filter_by(user_id=user.id,habit_id = habit.id, date=date).first()
        if dayinfo:
            form = DayForm(obj=dayinfo)
        else:
            form = DayForm()
        form_dict[habit] = form

    #TODO:
    #This does not appear to work
    if habits is None:
        error = 'Go add some habits!'

    return render_template('user/day.html',message=message,error=error,day=day_value,month=month,year=year,
    prev_day = prev_day, prev_month = prev_month, prev_year = prev_year, next_day = next_day, next_month = next_month, next_year = next_year,
    form_dict=form_dict,habits=habits)