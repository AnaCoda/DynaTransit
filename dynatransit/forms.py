from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired, Length
from dynatransit.models import User
import re
class RegistrationForm(FlaskForm):
        username = StringField('Username', 
                            validators=[InputRequired(),
                                Length(min=4, max=15)])
        email = StringField ('Email',validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up') 
        def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is Taken. Please choose another one.")
        def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already used. Please choose another one.")


class FindTrip(FlaskForm):
    start = StringField ('From Address:',validators=[DataRequired()])
    end = StringField('To Address:', validators=[DataRequired()])
    
    startTimeFrom = TimeField('Departure Time From:',format='%H-%M', validators=[DataRequired()])
    startTimeTo = TimeField('Departure Time To:',format='%H-%M', validators=[DataRequired()])
   
    arrivalTimeFrom = TimeField('Arrival Time From:',format='%H-%M', validators=[DataRequired()])
    arrivalTimeTo = TimeField('Arrival Time To:',format='%H-%M', validators=[DataRequired()])
   
    date  = DateField('Date',format='%Y-%m-%d', validators=[DataRequired()])
    
    submit = SubmitField('Find a Trip') 

class LoginForm(FlaskForm):
    email = StringField ('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In') 