from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from datetime import datetime

from models import User

#Helper function to check if a username is taken
def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name exists")


#Basic User Registration form. Collects a username, and password, and validates them
class UserRegistration(FlaskForm):
    username = StringField(
                'username',
                validators=[DataRequired(), username_exists]
    )
    password = PasswordField(
                'password',
                validators=[DataRequired(), Length(min=5)]
    )
    password2 = PasswordField(
                'Confirm password',
                validators=[DataRequired(), EqualTo('password', "Passwords must match")]
    )

#Basic form for loggin a user in
class LoginForm(FlaskForm):
    username = StringField(
                'username',
                validators=[DataRequired()]
    )

    password = PasswordField(
                'password',
                validators=[DataRequired()]
    )

#Checkin form
class checkInForm(FlaskForm):
    timeIn = DateTimeField(
            'timeIn',
            validators=[DataRequired()]
    )
