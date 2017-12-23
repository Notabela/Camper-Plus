from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,\
    SubmitField, DateField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, optional


class LoginForm(FlaskForm):
    """Login Form for Admins and Parents"""
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Sign in")


class SignupFormAdmin(FlaskForm):
    """Signup Form for Admin - Not Used Yet"""
    first_name = StringField('First name',
                             validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name',
                            validators=[DataRequired("Please enter your last name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter your email address.")])
    password = PasswordField(
        'Password',
        validators=[DataRequired("Please enter a password."),
                    Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField('Sign up')


class CreateParentForm(FlaskForm):
    """Form for Admin to Create a New Parent"""
    first_name = StringField('First name',
                             validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    birth_date = DateField("Birthday", validators=[DataRequired("Please enter your Birthday.")])
    gender = SelectField(label='Gender',
                         choices=[('M', 'Male'), ('F', 'Female')],
                         validators=[DataRequired("Please select a gender.")])
    email = StringField('Email Address', validators=[DataRequired("Please enter your email address."),
                                                     Email("Please enter your email address.")])
    phone = StringField('Phone Number', validators=[DataRequired("Please enter your phone name.")])
    street_address = StringField('Street Address',
                                 validators=[DataRequired("Please enter your street address.")])
    city = StringField('City', validators=[DataRequired("Please enter your City.")])
    state = StringField('State', validators=[DataRequired("Please enter your State.")])
    zipcode = IntegerField('Zip Code', validators=[DataRequired("Please enter your zipcode.")])
    submit = SubmitField('SAVE')


class CreateChildForm(FlaskForm):
    """Form for Admin to Create New Child"""

    first_name = StringField('First name', validators=[DataRequired("Please enter  first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter  last name.")])
    birth_date = DateField('Birthday', validators=[DataRequired("Please enter  birthday.")])
    grade = IntegerField('Grade', validators=[DataRequired("Please enter grade of the camper .")])
    gender = SelectField(label='Gender',
                         choices=[('M', 'Male'), ('F', 'Female')],
                         validators=[DataRequired("Please select a gender.")])
    medical_notes = TextAreaField('Medical Notes')
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('Zip Code')
    parent_first_name = StringField("Parent's first name",
                                    validators=[DataRequired("Please enter parent's first name.")])
    parent_last_name = StringField("Parent's last name",
                                   validators=[DataRequired("Please enter your last name.")])
    submit = SubmitField('SAVE')


class ChildEnrollmentForm(FlaskForm):
    """Form for Parent to Enroll a new Child"""
    child_first_name = StringField(label='First name',
                                   validators=[DataRequired("Please enter child's first name.")])
    child_last_name = StringField(label='Last name',
                                  validators=[DataRequired("Please enter  child's last name.")])
    child_birth_date = DateField(label='Birthday',
                                 validators=[DataRequired("Please enter child's birthday.")])
    child_grade = IntegerField(label='Grade',
                               validators=[DataRequired("Please enter child's grade.")])
    child_gender = SelectField(label='Gender',
                               choices=[('M', 'Male'), ('F', 'Female')],
                               validators=[DataRequired("Please select a gender.")])
    medical_notes = TextAreaField(label='Medical Notes', validators=[optional()])
    street_address = StringField(label='Street Address', validators=[optional()])
    city = StringField(label='City', validators=[optional()])
    state = StringField(label='State', validators=[optional()])
    zipcode = IntegerField(label='Zip Code', validators=[optional()])
    other_parent_name = StringField(label="Parent/Guardian's Name", validators=[optional()])
    other_parent_birth_date = DateField(label="Parent/Guardian's Birth Date",
                                        validators=[optional()])
    other_parent_email = StringField(label="Parent/Guardian's Email", validators=[optional()])
    other_parent_cell = StringField(label="Parent/Guardian's Cell", validators=[optional()])
    consent = SelectField(label='', choices=[('y', "Yes, I consent")], validators=[DataRequired()])
    submit = SubmitField(label='NEXT')
