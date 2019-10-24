
from flask import Blueprint,render_template, request, redirect, session, url_for,abort, flash,jsonify
from flask_login import login_required, current_user
import flask_excel as excel
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import json
import plotly 
import pandas as pd
import numpy as np


from application import db
from user.models import User, Habit, Day, DayDesc
from utilities.common import get_monthdelta_ints
from insights.utilities import get_profile_html_cal, load_habit_data, load_profile_data


insights_app = Blueprint('insights_app', __name__)

@insights_app.route('/profile')
@insights_app.route('/profile/<year>/<month>', methods=('GET', 'POST'))
@login_required
def profile(year=None,month=None):


    #Values for next and previous button - turn this into dictionary maybe?
    if year is None or month is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

    year = int(year)
    month = int(month)

    date = datetime.date(year,month,1)
    _,prev_month,prev_year = get_monthdelta_ints(date,months=-1)
    _,next_month,next_year = get_monthdelta_ints(date,months=1)
    
    #Inject calendar
    html_cal = get_profile_html_cal(year,month)

    #List of all habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    #Add insights
    insights = load_profile_data(current_user,month)

    return render_template('insights/profile.html', calendar = html_cal,month=month,year=year, prev_month = prev_month, 
    prev_year = prev_year,next_month=next_month,next_year=next_year,habits=habits,insights=insights)


@insights_app.route('/<habit>')
@login_required
def habit_detail(habit):
    habit = Habit.query.filter_by(user_id=current_user.id,habit_name=habit).first()
    insights = json.loads(load_habit_data(current_user,habit))
   

    return render_template('insights/habit_detail.html',habit=habit.habit_name,insights=insights)

@insights_app.route('/testing')
@login_required
def testing():
    import plotly
    import plotly.graph_objects as go 

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
            )
        ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('insights/testing.html',graphJSON=graphJSON,name=current_user.id) 
