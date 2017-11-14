from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import Form
from wtforms import TextAreaField, TextField, StringField
from wtforms import validators
"""   this is not final """

class ParentLoginForm(Form):
    username = TextField(
        'Username',
        validators=[validators.DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[validators.DataRequired()]
    )

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Invalid email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True
class ParentSignupForm(Form):
    

'''class group(Form):
    group_name = StringField('Group name')
    group_color = StringField('Last name')
    group_Quantity = IntegerField('Number of campers')
    camper1_name = StringField('Camper Name')
    camper2_name = StringField('Camper Name')
    camper3_name = StringField('Camper Name')
    camper4_name = StringField('Camper Name')
    camper5_name = StringField('Camper Name')
    submit = SubmitField('Greate a group')'''
