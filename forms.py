from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
 
 
class RegistrationForm(FlaskForm):
    fname    = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    lname    = StringField('Last Name',  validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username',   validators=[DataRequired(), Length(min=3, max=30)])
    email    = StringField('Email',      validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit   = SubmitField('Register')
 
 
class LoginForm(FlaskForm):
    username = StringField('Username',   validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')
 
 
class AntoineCalculationForm(FlaskForm):
    liquid_id   = SelectField('Select Liquid', coerce=int, validators=[DataRequired()])
    temperature = FloatField('Temperature (°C)', validators=[DataRequired()])
    submit      = SubmitField('Calculate Pressure')