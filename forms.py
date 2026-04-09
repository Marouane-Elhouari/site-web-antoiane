from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
 
 
class RegistrationForm(FlaskForm):
    fname    = StringField('First Name', 
                          validators=[
                              DataRequired(), 
                              Length(min=2, max=50, message='First name must be 2-50 characters'),
                              Regexp('^[A-Za-z0-9_]+$', message='First name can only contain letters, numbers, and underscores')
                          ])
    lname    = StringField('Last Name', 
                          validators=[
                              DataRequired(), 
                              Length(min=2, max=50, message='Last name must be 2-50 characters'),
                              Regexp('^[A-Za-z0-9_]+$', message='Last name can only contain letters, numbers, and underscores')
                          ])
    username = StringField('Username', 
                          validators=[
                              DataRequired(), 
                              Length(min=3, max=30, message='Username must be 3-30 characters'),
                              Regexp('^[A-Za-z0-9_]+$', message='Username can only contain letters, numbers, and underscores')
                          ])
    email    = StringField('Email', 
                          validators=[
                              DataRequired(message='Email is required'), 
                              Email(message='Please enter a valid email address'),
                              Length(min=5, max=120, message='Email must be 5-120 characters')
                          ])
    password = PasswordField('Password', 
                            validators=[
                                DataRequired(), 
                                Length(min=8, max=128, message='Password must be 8-128 characters')
                            ])
    confirm_password = PasswordField('Confirm Password',
                             validators=[
                                 DataRequired(), 
                                 EqualTo('password', message='Passwords must match')
                             ])
    submit   = SubmitField('Register')
 
 
class LoginForm(FlaskForm):
    username = StringField('Username',   validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')
 
 
class VerificationForm(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify Email')


class AntoineCalculationForm(FlaskForm):
    liquid_id   = SelectField('Select Liquid', coerce=int, validators=[DataRequired()])
    temperature = FloatField('Temperature (°C)', validators=[DataRequired()])
    submit      = SubmitField('Calculate Pressure')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email Address', 
                       validators=[
                           DataRequired(message='Email is required'),
                           Email(message='Please enter a valid email address')
                       ])
    submit = SubmitField('Send Reset Code')


class ResetPasswordForm(FlaskForm):
    reset_code = StringField('Reset Code', 
                           validators=[
                               DataRequired(message='Reset code is required'),
                               Length(min=6, max=6, message='Reset code must be exactly 6 digits')
                           ])
    new_password = PasswordField('New Password', 
                                validators=[
                                    DataRequired(message='New password is required'),
                                    Length(min=8, max=128, message='Password must be 8-128 characters')
                                ])
    confirm_password = PasswordField('Confirm New Password',
                                    validators=[
                                        DataRequired(message='Please confirm your new password'),
                                        EqualTo('new_password', message='Passwords must match')
                                    ])
    submit = SubmitField('Reset Password')