from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import inspect

from application import db, admin
from user.models import User,Habit,Day

admin_app = Blueprint('admin_app', __name__)


class ChildViewHabit(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Habit).mapper.column_attrs]

class ChildViewDay(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Day).mapper.column_attrs]

admin.add_view(ModelView(User, db.session))
admin.add_view(ChildViewHabit(Habit, db.session))
admin.add_view(ChildViewDay(Day, db.session))