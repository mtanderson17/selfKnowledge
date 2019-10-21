from flask_login import current_user
from sqlalchemy import func
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pandas as pd
import json
import chart_studio.plotly as py
import plotly.graph_objs as go

from application import db
from user.models import User, Habit, Day, DayDesc

#Should probably move this to common utilities
def get_profile_html_cal(year,month):
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

    return html_cal

#Aggregate analytics
def load_profile_data(month):
    '''
    load in all relavent data and then pass it to each function for analyzing 
    do not want to make db query for each insight when we will already have data loaded

    '''
    data = {}

    days_with_data = get_data_days_count()
    data['days_with_data'] = days_with_data

    data['month_progress'] = get_month_results(month)

    json_data = json.dumps(data)

    return json_data

def load_habit_data(habit):
    '''
    all functions related to habit detail page, organized in JSON format and returned to browser
    '''
    data = {}

    habit_summary  = get_days_habit_complete(habit)
    data['habit_summary'] = habit_summary
  

    json_data = json.dumps(data)
    return json_data

#Profile functions
def get_data_days_count():
    '''
    Find the earliest day a habit was recorded and return the days delta
    '''
    query = Day.query.filter_by(user_id=current_user.id,habit_complete=True)
    min_date = query.order_by(Day.date.asc()).first()
    max_date = query.order_by(Day.date.desc()).first()

    day_delta = max_date.date - min_date.date

    return str(day_delta.days)


def get_active_days_count():
    '''
    Return the # of days since the user created their account
    '''
  
    day_delta = datetime.datetime.now() - current_user.created_date

    return str(day_delta.days)

def get_month_results(month):
    '''
    Returns the progress for this month
    month: int
    '''
    data = {}

    query = db.session.query(
        Day,Habit
    ).filter_by(user_id = current_user.id,habit_complete=True
    ).filter(func.extract('month',Day.date)==month
    ).join(Habit)


 
    df = pd.read_sql(query.statement,query.session.bind)
    res = df.groupby('habit_name').count()['habit_id']

    return res.to_json()




#Habit analytics
def get_days_habit_complete(habit):
    '''
    Take a habit object and return the # of days its been completed by month
    as well as total of that
    '''
    data = {}
    query = Day.query.filter_by(user_id=current_user.id, habit_id=habit.id)

    df = pd.read_sql(query.statement,query.session.bind)
    df.index = df['date']

    #Returns days habit complete by year/month
    res = df.groupby(pd.Grouper(freq='M')).sum()['habit_complete']
    print(res)
    data['habit_series'] = res.to_json(orient='index',date_format='iso')
    data['habit_sum'] = sum(res)
    data['habit_desc'] = res.describe().to_json()
    
    return json.dumps(data)

def test_func(value):
    
    pass

  
 

