from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import AdminIndexView
from sqlalchemy import inspect

from application import db, admin
from user.models import User,Habit,Day,UserTypeModel

admin_app = Blueprint('admin_app', __name__)

class AdminRequiredMixin(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.user_type == UserTypeModel.ADMIN:
                return True
            else:
                return False
        else:
            return False

    #Maybe add inaccessiable callback 404 to make it look like it doesn't exist


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.user_type == UserTypeModel.ADMIN:
                return True
            else:
                return False
        else:
            return False

class ChildViewHabit(AdminRequiredMixin):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Habit).mapper.column_attrs]

class ChildViewDay(AdminRequiredMixin):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Day).mapper.column_attrs]


admin.add_view(AdminRequiredMixin(User, db.session))
admin.add_view(ChildViewHabit(Habit, db.session))
admin.add_view(ChildViewDay(Day, db.session))