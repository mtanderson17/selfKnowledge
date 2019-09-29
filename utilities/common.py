
from flask_login import current_user
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from application import db
from user.models import Habit,Day

def get_monthdelta_ints(date,days=0,months=0,years=0):
    new_date = date + relativedelta(days=days,months=months,years=years)
    day = new_date.day
    month = new_date.month
    year = new_date.year 

    return int(day), int(month), int(year)

def validate_data(json_data):
    pass



def process_file_upload(json_data):
    #Get user and habits
    user = current_user
    habits = Habit.query.filter_by(user_id=user.id).all()

    data = json_data['result']
    col_names = data.pop(0)
    df = pd.DataFrame(data, columns=col_names)
    
    #User habits from database
    habits_dict = dict()
    for habit in habits:
        habits_dict[str(habit)] = habit.id
 
    
    #Make sure column headers align to habits
    message = []
    for habit in [x for x in df.columns][1:]:
        if habit.lower() not in [str(habit) for habit in habits]:
            message.append(f'{habit} does not exist in your habits! Please add it!')
            del df[habit]

    #Iterate through rows and make Days
    for index,row in df.iterrows():
        cols = list(row.index)
        date = row[0]
        cols.pop(0) #Remove date
        for value in row[1:]:
            day = Day(
                date = date,
                habit_id = habits_dict[cols.pop(0).lower()],
                user_id = current_user.id,
                habit_complete = bool(value),
                day_desc = None #incorporate this later

            )
            db.session.add(day)
        db.session.commit()
        
 
    


  

 