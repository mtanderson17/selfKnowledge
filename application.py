from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment 
from flask_admin import Admin
from flask_login import LoginManager 

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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from user.models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from user.views import user_app
    app.register_blueprint(user_app)

    from admin.views import admin_app
    app.register_blueprint(admin_app)

    from auth.auth import auth
    app.register_blueprint(auth)

    from admin.views import MyAdminIndexView
    admin.init_app(app, index_view=MyAdminIndexView())
    moment.init_app(app)


    return app


