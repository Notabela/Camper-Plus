from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField, TextAreaField
from camperapp.models import CampGroup
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Sign in")


class SignupFormAdmin(FlaskForm):
    name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField('Sign up')


class CreateParentForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    birth_date = DateField("Birthday")
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')])
    email = StringField('Email Address')
    phone = StringField('Phone Number')
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('Zip Code')
    submit = SubmitField('SAVE')


class CreateChildForm(FlaskForm):
    #_groups = CampGroup.query.order_by(CampGroup.name).all()
    #_group_choices = [(group.id, group.name) for group in _groups]

    first_name = StringField('First name')
    last_name = StringField('Last name')
    birth_date = DateField('Birthday')
    grade = IntegerField('Grade')
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')])
    medical_notes = TextAreaField('Medical Notes')
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('Zip Code')
    parent_first_name = StringField("Parent's first name")
    parent_last_name = StringField("Parent's last name")
    group = SelectField(label='Group', choices=_group_choices)
    submit = SubmitField('SAVE')


class ChildEnrollmentForm(FlaskForm):
    child_first_name = StringField('First name')
    child_last_name = StringField('Last name')
    child_birth_date = DateField('Birthday')
    child_grade = IntegerField('Grade')
    child_gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')])
    medical_notes = TextAreaField('Medical Notes')
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('Zip Code')
    mother_name = StringField("Mom's Name (or other Primary legal guardian)")
    mother_birth_date = DateField("Mom's Birthday")
    mother_email = StringField("Mom's Email")
    mother_cell = StringField("Mom's Cell Phone")
    father_name = StringField("Dad's Name (or other Primary legal guardian)")
    father_birth_date = DateField("Dad's Birthday")
    father_email = StringField("Dad's Email")
    father_cell = StringField("Dad's Cell Phone")
    consent = SelectField('', choices=[('y', "Yes, I consent")])
    submit = SubmitField('NEXT')
