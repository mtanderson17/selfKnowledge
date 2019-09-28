from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment 
from flask_admin import Admin

db = SQLAlchemy()
moment = Moment()
admin = Admin()

def create_app(config_obj = 'settings.DevelopmentConfig',**config_overrides):
    app = Flask(__name__)

    app.config.from_object(config_obj)

    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()

    from user.views import user_app
    app.register_blueprint(user_app)

    from admin.views import admin_app
    app.register_blueprint(admin_app)


    admin.init_app(app)
    moment.init_app(app)


    return app


