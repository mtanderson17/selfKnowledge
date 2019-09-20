import datetime
from sqlalchemy.orm import relationship

from application import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    habits = relationship("Habit", back_populates="user", cascade="all, delete, delete-orphan")


    def __init__(self, email, password):
        self.password = password
        self.email = email 


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    habit_name = db.Column(db.String(),nullable=False)

    user = relationship("User", back_populates="habits")
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
    habit_complete = db.Column(db.Boolean(),default=False)
    day_desc = db.Column(db.String())

    habit = relationship("Habit", back_populates="days")

    def __init__(self,date,habit_id,user_id,habit_complete,day_desc):
        self.date = date
        self.habit_id = habit_id
        self.user_id = user_id
        self.habit_complete = habit_complete
        self.day_desc = day_desc

    def __repr__(self):
        return f'{self.date}:{self.habit_id}:{self.habit_complete}'



