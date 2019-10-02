from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField
from wtforms.widgets import TextArea

from application import db
from user.models import User


class HabitForm(FlaskForm):
    habit_name = StringField('New Habit', [validators.DataRequired()])

class DayForm(FlaskForm):
    habit_complete = BooleanField("Complete")
    day_desc = StringField('Desc', widget=TextArea())