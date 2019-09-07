from application import create_app as create_app_base
from application import db
import unittest

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
        
        
    def test_register_user(self):
        # basic registration
        rv = self.app.post('/register', data=dict(
            email="matt@example.com",
            password="test123",
            confirm="test123"
            ), follow_redirects=True)
        print(rv)
        print(User.query.filter_by(email='matt@example.com').count())
        assert User.query.filter_by(email='matt@example.com').count() == 1
       