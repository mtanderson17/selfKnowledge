import unittest
from flask import session

from application import create_app as create_app_base
from application import db
from user.models import User

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
       