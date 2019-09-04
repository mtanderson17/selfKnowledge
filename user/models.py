import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    password = db.Column(db.password())
    created_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)


    def __init__(self, first_name, last_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
