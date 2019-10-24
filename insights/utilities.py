from flask_login import current_user
from sqlalchemy import func
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly
import plotly.graph_objects as go 
import plotly_express as px 

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
def load_profile_data(current_user,month):
    '''
    load in all relavent data and then pass it to each function for analyzing 
    do not want to make db query for each insight when we will already have data loaded

    '''
    data = {}

    days_with_data = get_data_days_count(current_user)
    data['days_with_data'] = days_with_data

    data['month_progress'] = get_month_results(current_user,month)
    print(data)

    json_data = json.dumps(data)

    return json_data

def load_habit_data(current_user,habit):
    '''
    all functions related to habit detail page, organized in JSON format and returned to browser
    '''
    data = {}

    habit_summary  = get_days_habit_complete(current_user,habit)
    data['habit_summary'] = habit_summary
    
  

    json_data = json.dumps(data)
 


    return json_data

#Profile functions
def get_data_days_count(current_user):
    '''
    Find the earliest day a habit was recorded and return the days delta
    '''
    query = Day.query.filter_by(user_id=current_user.id,habit_complete=True)
    min_date = query.order_by(Day.date.asc()).first()
    max_date = query.order_by(Day.date.desc()).first()

    day_delta = max_date.date - min_date.date

    return str(day_delta.days)


def get_active_days_count(current_user):
    '''
    Return the # of days since the user created their account
    '''
  
    day_delta = datetime.datetime.now() - current_user.created_date

    return str(day_delta.days)

def get_month_results(current_user,month):
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
def get_days_habit_complete(current_user,habit):
    '''
    Take a habit object and return the # of days its been completed by month
    as well as total of that
    '''
    data = {}

    query = Day.query.filter_by(user_id=current_user.id, habit_id=habit.id)

    df = pd.read_sql(query.statement,query.session.bind)
    df.index = df['date']

    try:
        #Returns days habit complete by year/month
        res = df.groupby(pd.Grouper(freq='M')).sum()['habit_complete']
        graph_data = [
            go.Bar(
                x=res.index, # assign x as the dataframe column 'x'
                y=res.values
                )
            ]

        graphJSON = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)
        
        
        habit_series = res.to_json(orient='index',date_format='iso')
        habit_sum = sum(res)
        habit_desc = res.describe().to_dict()
        month_graph = graphJSON
    except:
        habit_series = 'Add some data :)'
        habit_sum = 'Add some data :)'
        habit_desc = dict(count= 'Oops',
                          mean= 'Oops',
                          min= 'Oops',
                          max= 'Oops'
                            )
        month_graph = None

    data['habit_series'] = habit_series
    data['habit_sum'] = habit_sum
    data['habit_desc'] = habit_desc
    data['month_graph'] = month_graph 
    
    return data

def test_func(value):
    
    pass

  
 

