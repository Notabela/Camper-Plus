from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class SignupForm(Form):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    email = StringField('Email')
    password = PasswordField('Password')
    # change this later to specify the possible roles the user can be
    role = StringField('Role')
    submit = SubmitField('Sign up')
