from datetime import datetime

"""db and login_manager is defined in the __init__.py from where we are importing them"""
from flaskblog import db,login_manager

"""UserMixin provides default implementations for the methods that Flask-Login 
	expects user objects to have"""
from flask_login import UserMixin

"""this is login manager, which will take care of the user session"""
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	

    """This Model will create a user table that will have details of registered user"""

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True , nullable = False)
	email = db.Column(db.String(20), unique=True , nullable = False)
	image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
	password = db.Column(db.String(60),nullable=False)
	
	"""
	backref means to adding another column named author in the Post model 
	using which we can have all the information of this uset to the Post model 
	Lazy true means that sqlalchemy will in one go.
	posts is not a column here its just the relationship
	this queries the Post Model to find posts by this user

	"""
	posts = db.relationship('Post', backref='author', lazy=True)

	"""	this defines how our method prints"""
	def __repr__(self):
		return f"User('{self.username}','{self.email}', '{self.image_file}')"


class Post(db.Model):
	""" This model will create a table named Post in the database with the columns as below	"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"