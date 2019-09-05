from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from user.models import User

def create_app(**config_overrides):
    app = Flask(__name__)

    app.config.from_object('settings.DevelopmentConfig')

    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()


    from user.views import user_app
    app.register_blueprint(user_app)

    return app

