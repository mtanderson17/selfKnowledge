from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment 

db = SQLAlchemy()
moment = Moment()

from user.models import User

def create_app(config_obj = 'settings.DevelopmentConfig',**config_overrides):
    app = Flask(__name__)

    app.config.from_object(config_obj)

    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()


    from user.views import user_app
    app.register_blueprint(user_app)


    moment.init_app(app)

    return app

