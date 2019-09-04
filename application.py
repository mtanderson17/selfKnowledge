from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from user.models import User

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()


    from user.views import user_app
    app.register_blueprint(user_app)

    return app

