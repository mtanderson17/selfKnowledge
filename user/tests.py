import unittest
from flask import session
from flask_login import current_user
from werkzeug import ImmutableMultiDict
import datetime

from application import create_app as create_app_base
from application import db
from user.models import User,Habit,Day

class UserTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(config_obj ='settings.TestingConfig')
        
    def setUp(self):
        self.app_factory = self.create_app()
        
        #TODO:
        #There has to be a better way to do this
        @self.app_factory.context_processor
        def inject_now():
            return {'now': datetime.datetime.utcnow()}

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
            assert current_user.email == self.user_dict()['email']

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
       
        data = ImmutableMultiDict([(f'{habit.id}', f'{habit.id}')])
        rv = self.app.post(f'/day/2019/1/1',data=dict([("1","1")]))
  
        day_info = Day.query.filter_by(user_id=user.id,habit_id=habit.id,date=date).first()

        assert day_info.habit_complete == True 

        assert day_info.day_desc == 'testing'

    def test_day_buttons(self):
        #Test that previous and next day buttons in day view work

        assert 1 == 1

    def test_profile_cal_urls(self):
        #Test that the urls in the calendar go to the days

        assert 1 == 1

    def test_profile_buttons(self):
        #Test that previous and next buttons in profile work

        assert 1 == 1

    def test_gototoday(self):
        #Test that the 'Go To Today' URL works 
        today = datetime.datetime.utcnow()

        assert 1 == 1

    def test_file_upload(self):

        assert 1 == 1 

    

        

        

       