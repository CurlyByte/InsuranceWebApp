from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Creatin object of SQLAlchemy -> db -> database.db that is located in instances folder
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'flaskproject'
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'    
    db.init_app(app)
   
    #Importing(registering) blueprints
    from .views import views 
    from .auth import auth
    from .homepage import homepage
    from .error_handlers import error_handlers

    app.register_blueprint(views, url_prefix="")
    app.register_blueprint(auth, url_prefix ="")
    app.register_blueprint(homepage, url_prefix ="")
    app.register_blueprint(error_handlers, url_prefix="")

    from .models import User, Insurance
    from .auth import login
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app



