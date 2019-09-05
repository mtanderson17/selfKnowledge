import datetime

from application import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)


    def __init__(self, email, password):
        self.password = password
        self.email = email 


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
