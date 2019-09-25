
import datetime
from dateutil.relativedelta import relativedelta

def get_monthdelta_ints(date,days=0,months=0,years=0):
    new_date = date + relativedelta(days=days,months=months,years=years)
    day = new_date.day
    month = new_date.month
    year = new_date.year 

    return int(day), int(month), int(year)