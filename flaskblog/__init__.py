from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask (__name__) # instance of Flask class #__name__ is the name of the module. can be __main__ of if imported will be name of the file that imports.

# this is required while using forms 
app.config['SECRET_KEY'] = 'df963732f50bff2f4051378117aa7f4b'

#we need to specify the path for the database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login' #this is used for @login_required decorator
login_manager.login_message_category = 'info'


# this needs to be after db for circular import
#also when we run the app
from flaskblog import routes 