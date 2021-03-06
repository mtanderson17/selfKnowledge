import datetime
import enum 
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from application import db



class UserTypeModel(enum.Enum):
    ADMIN = 'ADMIN'
    FREE = 'FREE'
    PAID = 'PAID'

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    user_type = db.Column(db.Enum(UserTypeModel), default = UserTypeModel.FREE)

    #Child
    habits = relationship("Habit", back_populates="user", cascade="all, delete, delete-orphan")

    def __init__(self, email, password):
        self.password = password
        self.email = email 

    def __repr__(self):
        return self.email
    
class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    habit_name = db.Column(db.String(),nullable=False)
    habit_create_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    #Parent (One-to-Many)
    user = relationship("User", back_populates="habits")

    #Child (Many-to-One)
    days = relationship("Day", back_populates='habit',cascade="all, delete, delete-orphan")

    

    def __init__(self,user_id,habit_name):
        self.user_id = user_id
        self.habit_name = habit_name

    def __repr__(self):
        return self.habit_name

class Day(db.Model):
    __tablename__ = 'days'

    id = db.Column(db.Integer(),primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow,nullable=False)
    habit_id = db.Column(db.Integer(),db.ForeignKey('habits.id'))
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    habit_complete = db.Column(db.Boolean())
  
    #Parent
    habit = relationship("Habit", back_populates="days")

    #Child
    daydescs = relationship("DayDesc", back_populates='day',cascade="all, delete, delete-orphan")


    def __init__(self,date,habit_id,user_id,habit_complete):
        self.date = date
        self.habit_id = habit_id
        self.user_id = user_id
        self.habit_complete = habit_complete
       

    def __repr__(self):
        return f'{self.date}:{self.habit_id}:{self.habit_complete}'

class DayDesc(db.Model):
    __tablename__ = 'daydescs'

    id = db.Column(db.Integer(),primary_key=True)
    day_id = db.Column(db.Integer(),db.ForeignKey('days.id'))
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow,nullable=False)
    text = db.Column(db.String())

    #Parent
    day = relationship("Day", back_populates="daydescs")

    def __init__(self,date,user_id,text):
        self.date = date
        self.user_id = user_id
        self.text = text
