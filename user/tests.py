import unittest
from flask import session
import datetime

from application import create_app as create_app_base
from application import db
from user.models import User,Habit,Day

class UserTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(config_obj ='settings.TestingConfig')
        
    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
       

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def user_dict(self):
        return dict(
            email="matt@example.com",
            password="test123",
            confirm="test123"
            )
        
        
    def test_register_user(self):
        # basic registration
        rv = self.app.post('/register', data=self.user_dict(), follow_redirects=True)
        assert User.query.filter_by(email='matt@example.com').count() == 1

    def test_login_user(self):
        # create user
        self.app.post('/register', data=self.user_dict())
        # login user
        rv = self.app.post('/login', data=dict(
            email=self.user_dict()['email'],
            password=self.user_dict()['password']
            ))
        # check the session is set
        with self.app as c:
            rv = c.get('/')
            assert session.get('username') == self.user_dict()['email']

    def test_add_habit(self):
        # create user
        self.app.post('/register', data=self.user_dict())
        # login user
        self.app.post('/login', data=dict(
            email=self.user_dict()['email'],
            password=self.user_dict()['password']
            ))
        #add new habit
        self.app.post('/add_habit',data=dict(habit_name='habit1'))
        user = User.query.filter_by(email='matt@example.com').first()
        habit = Habit.query.filter_by(user_id = user.id).first()

        assert habit.habit_name == 'habit1'

    def test_delete_habit(self):
        # create user
        self.app.post('/register', data=self.user_dict())
        # login user
        self.app.post('/login', data=dict(
            email=self.user_dict()['email'],
            password=self.user_dict()['password']
            ))
        #add new habit
        self.app.post('/add_habit',data=dict(habit_name='habit1'))
        
        #delete habit
        self.app.post('/delete_habit/habit1')
        user = User.query.filter_by(email='matt@example.com').first()
        habit = Habit.query.filter_by(user_id = user.id).first()

        assert habit is None 

    def test_record_day(self):
        # create user
        self.app.post('/register', data=self.user_dict())
        # login user
        self.app.post('/login', data=dict(
            email=self.user_dict()['email'],
            password=self.user_dict()['password']
            ))
        #add new habit
        self.app.post('/add_habit',data=dict(habit_name='habit1'))

        #log habit
        date = datetime.datetime(year=2019,month=1,day=1)
        user = User.query.filter_by(email='matt@example.com').first()
        habit = Habit.query.filter_by(user_id = user.id).first()

        user_id = user.id
        habit_id = habit.id
        
        rv = self.app.post(f'/day/2019/1/1',data=dict(habit_id = habit.id,habit_complete=True,day_desc='testing'))
    
        day_info = Day.query.filter_by(user_id=user_id,habit_id=habit_id,date=date).first()

        assert day_info.habit_complete == True 

        assert day_info.day_desc == 'testing'

        

        

       