from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld_secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,DB_NAME)
    db.init_app(app)

    

    from .views import views
    from .auth import auth
    

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/auth/') #any route inside the auth will have the prefix /auth/
    
    from .models import User,Note
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    with app.app_context():
        if not os.path.exists('website/'+DB_NAME):
            db.create_all()
            print('database created!')
