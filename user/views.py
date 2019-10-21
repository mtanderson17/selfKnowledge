
from flask import Blueprint,render_template, request, redirect, session, url_for,abort, flash,jsonify
from flask_login import login_required, current_user
import flask_excel as excel
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import json


from application import db
from user.models import User, Habit, Day, DayDesc
from user.forms import HabitForm
from utilities.common import get_monthdelta_ints, process_file_upload

user_app = Blueprint('user_app', __name__)



@user_app.route('/add_habit', methods=('GET', 'POST'))
@login_required
def add_habit(message=None):
    error = None
  
    user = current_user
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
    user = current_user
    del_habit = Habit.query.filter_by(user_id=user.id, habit_name=habit).first()

    db.session.delete(del_habit)
    db.session.commit()
    
    return redirect(url_for('user_app.add_habit',message=f'{habit} deleted'))

@user_app.route("/day/<year>/<month>/<day_value>",methods=("GET","POST"))
@login_required
def day(year,month,day_value):

    
    date = datetime.date(int(year),int(month),int(day_value))

    #Values for next and previous button
    prev_day,prev_month,prev_year = get_monthdelta_ints(date,days=-1)
    next_day,next_month,next_year = get_monthdelta_ints(date,days=1)

    #Get user and habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    daydesc = DayDesc.query.filter_by(user_id=current_user.id,date=date).first()
    if daydesc:
        daydesc = daydesc.text
    
    print(daydesc)

   
    #if there is already information in days then prepopulate forms
    day_info_dict = {}
    for habit in habits:
        dayinfo = Day.query.filter_by(user_id=current_user.id,habit_id = habit.id, date=date).first()
        if dayinfo:
            day_info_dict[habit] = dayinfo
        else:
            day_info_dict[habit] = None

 
    #Get data from form
    if request.method == 'POST':
        #Delete current day info
        day_info = Day.query.filter_by(user_id=current_user.id,date=date).all()
        for day in day_info:
            db.session.delete(day)
            db.session.commit()

        #Get Desc Data
        desc = request.form['dayDesc']

        daydesc = DayDesc(
            date = date,
            user_id = current_user.id,
            text = desc 
        )

        db.session.add(daydesc)
        db.session.commit()

        #Get habit data
        data = [int(value) for value in request.form if value != 'dayDesc']
        for habit in habits:
            if habit.id in data:
                habit_complete = True
            else:
                habit_complete = False
            day = Day(
                    date = date,
                    habit_id = habit.id,
                    user_id = current_user.id,
                    habit_complete = habit_complete
                )
            db.session.add(day)
            db.session.commit()

        flash('Day Updated :)','SUCCESS')

        return redirect(url_for('user_app.day',year=year,month=month,day_value=day_value))

 
    if len(habits) == 0:
        #Could potential add link to redirect?
        flash('Go add some habits!','ERROR')

    return render_template('user/day.html',day=day_value,month=month,year=year,
    prev_day = prev_day, prev_month = prev_month, prev_year = prev_year, next_day = next_day, next_month = next_month, next_year = next_year,
    habits=habits, day_info_dict=day_info_dict,daydesc=daydesc)

@user_app.route('/manage_account',methods=('GET','POST'))
@login_required
def manage_account():
    return render_template('user/manage_account.html')

@user_app.route('/upload_data',methods=('GET','POST'))
@login_required
def upload_data():
    if request.method == 'POST':
        try:
            json_data = {"result": request.get_array(field_name='file')}
            flash("File uploaded successfully",'SUCCESS')
        except:
            flash('File Upload Error! - ensure extension is .xlsx, .xls, .xlsx, .csv - ensure first column is valid date - ensure column names align to habits','ERROR')

        messages = process_file_upload(json_data)

        if len(messages) > 0:
            for message in messages:
                flash(message,'ERROR')

        return redirect(url_for('user_app.manage_account'))
    return redirect(url_for("user_app.manage_account"))