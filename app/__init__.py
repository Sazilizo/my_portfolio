# from app import pages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

UPLOAD_FOLDER = 'sqlite:///site.db'
app = Flask(__name__)
with app.app_context():
    app.config["SECRET_KEY"] = "c59944d923f5322fa6a356fb3044ed52"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
    db = SQLAlchemy(app)
    bcrypt = Bcrypt()
    login_manager = LoginManager(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'
    

from app import routes
app.register_blueprint(routes.bp)