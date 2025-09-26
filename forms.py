from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, URL, Optional, Regexp
from models import User
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class GeolocationForm(FlaskForm):
    ip_address = StringField('IP Address', validators=[DataRequired()])
    submit = SubmitField('Track Location')

class LinkCheckForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Check Link')

class FileCheckForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Check File')
    
class GCashPaymentForm(FlaskForm):
    phone_number = StringField('GCash Phone Number', validators=[
        DataRequired(),
        Regexp(r'^(09|\+639)\d{9}$', message='Please enter a valid Philippine phone number (e.g., 09123456789 or +639123456789)')
    ])
    reference_number = StringField('Reference Number', validators=[DataRequired(), Length(min=6, max=20)])
    amount = DecimalField('Amount Paid (PHP)', validators=[DataRequired()])
    subscription_duration = SelectField('Subscription Duration', 
                                       choices=[('30', '1 Month - ₱99'), 
                                                ('90', '3 Months - ₱249'), 
                                                ('365', '1 Year - ₱899')],
                                       validators=[DataRequired()])
    auto_renew = BooleanField('Enable Auto-Renewal', default=False)
    submit = SubmitField('Verify Payment')