from application import create_app as create_app_base
from application import db
from mongoengine.connection import _get_db
import unittest

from user.models import User

class UserTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            app.config.from_object('application.config.TestingConfig')
            )
        
    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)
        
    def test_register_user(self):
        # basic registration
        rv = self.app.post('/register', data=dict(
            first_name="Jorge",
            last_name="Escobar",
            username="jorge",
            email="jorge@example.com",
            password="test123",
            confirm="test123"
            ), follow_redirects=True)
        assert User.objects.filter(username='jorge').count() == 1