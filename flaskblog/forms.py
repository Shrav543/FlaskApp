
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from flaskblog.models import User


# here we write classes and flask converts them to hmtl template

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),
                        Length(max=30), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register ')

    """This are the methods that are run on submit"""

    def validate_username(self, username1):
        user = User.query.filter_by(username=username1.data).first()
        
        if user:
            raise ValidationError('Username is Taken')

    """this is checking if the user exists with the above condition"""
        

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already associated with other account'
                                  )


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(),
                        Length(max=30), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')
