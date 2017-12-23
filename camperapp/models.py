"""
.. module:: camperapp.models
   :platform: Unix, Windows
   :synopsis: Sql_Alchemy Models for Camper+ web application

.. moduleauthor:: Daniel Obeng, Chris Kwok, Eric Kolbusz, Zhirayr Abrahamyam

"""
import enum
from datetime import datetime, date
from marshmallow import Schema, fields
from camperapp import db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.types as types
from sqlalchemy import Enum

# Site dependant Variables
camp_season = 'SUMMER {}'.format(date.today().strftime("%Y"))
camp_address = 'Camper +<br>160 Convent Avenue<br>New York, NY 10016<br>USA'
registration_cost = 50


class Role(enum.Enum):
    """Role of Users

        Roles that can be assumed by a user
    """
    admin = 'admin'
    parent = 'parent'


def get_user_name(user):
    """Retrieve the display name of users

        Retrieves the print ready names of logged in users
        for rendering on web pages

        Args:
           user (User) : user object from User model

        Returns:
            the first part of the email of users without a name (admins)
            or the print ready name (last name, first name) of users
            with a name (parents)
    """
    if user.role is Role.admin:
        try:
            return user.email[0:user.email.index('@')]
        except ValueError:
            return user.email

    elif user.role is Role.parent:
        try:
            parent = Parent.query.filter_by(id=user.parent_id).first()
            return parent.name()
        except AttributeError:
            return 'Parent'


class LowerCaseString(types.TypeDecorator):
    """Lowercase conversion template SQL Alchemy Models

        Used to initialize the String Columns of Sql Alchemy Models
        for auto conversion of assigned string literals and variables
        to lowercase

        .. note::
            If no value is passed to the field, auto conversion doesn't
            happen
    """
    impl = types.String

    def process_bind_param(self, value, dialect):
        return value.lower() if value is str else value


class CampEvent(db.Model):
    """Model for Camp Events

        SQL Alchemy model for Camp Events for the Camper+ Schedule
    """
    __tablename__ = 'campevent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(LowerCaseString)
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))

    def __init__(self, title, start, end):
        """Camp Event Initializer

            Args:
                title (str) : title of event
                start (datetime) : start time of event
                end (datetime) : end time of event

            .. note::
                each camp event has a color corresponding to its assigned group.
                this parameter is initially None
        """
        self.title = title
        self.start = start
        self.end = end
        self.color = None

    def add_color_attr(self):
        """Add a color to the camp event

            Adds the color of the events Camp Group to the event
        """
        if self.group_id is None:
            return
        self.color = self.campgroup.color

    @classmethod
    def convert_calevent_to_campevent(cls, calevent):
        """Convert Full Calendar calevent dictionary to a Camp Event object

            Converts a calendar event retrieved from the Full Calendar
            calender framework (calEvent) to a CampEvent to store in db

            Args:
               calevent (dict) : calendar event from full calendar

            Returns:
                A CampEvent instance ready to be committed to db
        """
        title = calevent['title']
        start_time =\
            CampEvent.convert_iso_datetime_to_py_datetime(calevent['start'])
        end_time =\
            CampEvent.convert_iso_datetime_to_py_datetime(calevent['end'])
        group_id = int(calevent['group_id'])

        camp_event = CampEvent(title, start_time, end_time)
        camp_event.group_id = group_id

        return camp_event

    @classmethod
    def convert_iso_datetime_to_py_datetime(cls, iso_datetime):
        """Convert ISO standard datetime to python datetime object

            Converts an ISO standard datetime (e.g 2014-10-12T12:45)
            to a python datetime object. The Full Calendar Framework
            uses the ISO standard datetime

            Args:
               iso_datetime (str) : ISO datetime string

            Returns:
                A python datetime object
        """
        return datetime.strptime(iso_datetime, '%Y-%m-%dT%H:%M:%S')

    @classmethod
    def convert_py_datetime_to_iso_datetime(cls, py_datetime):
        """Convert python datetime object to an ISO standard datetime string

            Converts a python datetime object to an ISO standard
            datetime string (e.g 2014-10-12T12:45).
            The Full Calendar Framework uses the ISO standard datetime

            Args:
               py_datetime (datetime) : python datetime object

            Returns:
                An ISO standard datetime string
        """
        return py_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    def __repr__(self):
        return '<CampEvent {}>'.format(self.title)


class CampEventSchema(Schema):
    """Schema for Camp Events

        A Marshmallow Schema template to enable CampEvent
        objects to converted to JSON Objects. See sample code

        .. code-block:: python
            event_schema = CampEventSchema(many=True)
            events = CampEvent.query.all()  # get all data for now
            for event in events:
                event.add_color_attr()
            result = event_schema.dump(events).data
            json = flask.jsonify(result)

        .. warning::
            Be sure to append a color to Camp Events using the ``add_color_attr``
            method before trying to jsonify it.
    """
    id = fields.Int()
    title = fields.Str()
    start = fields.DateTime()
    end = fields.DateTime()
    group_id = fields.Str()
    # this doesn't original exist in db, should be appended before serialization
    color = fields.Str()


class Parent(db.Model):
    """Parent Model

        SQL Alchemy Model of a Parent
    """
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(LowerCaseString)
    last_name = db.Column(LowerCaseString)
    birth_date = db.Column(db.Date())
    gender = db.Column(LowerCaseString)
    email = db.Column(LowerCaseString)
    phone = db.Column(db.String())
    street_address = db.Column(LowerCaseString)
    city = db.Column(LowerCaseString)
    state = db.Column(LowerCaseString)
    zip_code = db.Column(db.Integer())
    campers = db.relationship('Camper', backref='parent', lazy='dynamic')
    user = db.relationship('User', uselist=False, backref='user')

    def name(self):
        """Get a display friendly name of Parent

            Concatenates Parent's last name and first name
            to a display friendly version. Format of name
            is Last name, First name

            Returns:
                'Last name, First name' of Parent
        """
        return "{}, {}".format(self.last_name.capitalize(), self.first_name.capitalize())

    def alt_name(self):
        """Get an alternative display friendly name of Parent

            Concatenates Parent's first name and last name
            to a display friendly version. Format of name
            is Last name, First name

            Returns:
                'First name Last name' of Parent
        """
        return "{} {}".format(self.first_name.capitalize(), self.last_name.capitalize())

    def __repr__(self):
        return '<Parent {}>'.format(self.name())


class Camper(db.Model):
    """Camper Model

        SQL Alchemy Model of a Camper
    """
    __tablename__ = 'camper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(LowerCaseString)
    last_name = db.Column(LowerCaseString)
    birth_date = db.Column(db.Date())
    grade = db.Column(db.Integer())
    gender = db.Column(LowerCaseString)
    medical_notes = db.Column(LowerCaseString)
    phone = db.Column(db.String())
    street_address = db.Column(LowerCaseString)
    city = db.Column(LowerCaseString)
    state = db.Column(LowerCaseString)
    zip_code = db.Column(db.Integer())
    is_active = db.Column(db.Boolean())
    other_parent_name = db.Column(db.String())
    other_parent_birth_date = db.Column(db.Date())
    other_parent_email = db.Column(db.String())
    other_parent_phone = db.Column(db.String())
    group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))
    parent_id = db.Column(db.Integer(), db.ForeignKey('parent.id'))

    def age(self):
        """Get the age of Camper

            Calculates the age of a Camper based on time since
            camper's birth date

            Returns:
                age of Camper
        """
        born = self.birth_date
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:
            # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day - 1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_color(self):
        """Get the color of camper's Camp Group

            Retrieves Camper's assigned Camp Group's color.

            Returns:
                color of camper's Camp Group (camper.campgroup.color)
                or gray if camper has no group

            .. note::
                The default color of Camper's without a group is gray but
                this is should never happen. Campers without groups should
                be put in the default None group created in camperapp.routes.py
        """
        if not self.group_id:
            return 'gray'  # Default color if user has no group
        else:
            return self.campgroup.color

    def name(self):
        """Get a display friendly name of Camper

            Concatenates Campers's last name and first name
            to a display friendly version. Format of name
            is Last name, First name

            Returns:
                'Last name, First name' of Camper
        """
        return "{}, {}".format(self.last_name.capitalize(), self.first_name.capitalize())

    def alt_name(self):
        """Get an alternative display friendly name of Camper

            Concatenates Camper's first name and last name
            to a display friendly version. Format of name
            is Last name, First name

            Returns:
                'First name Last name' of Camper
        """
        return "{} {}".format(self.first_name.capitalize(), self.last_name.capitalize())

    def __repr__(self):
        return '<Camper {}>'.format(self.name())


class CampGroup(db.Model):
    """Camp Group Model

        SQL Alchemy Model of a Camp Group
    """
    __tablename__ = 'campgroup'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(LowerCaseString)
    color = db.Column(db.String())
    campers = db.relationship('Camper', backref='campgroup', lazy='dynamic')
    events = db.relationship('CampEvent', backref='campgroup', lazy='dynamic')

    def __init__(self, name, color):
        """Camp Group Initializer

            Args:
                name (str) : camp group's name
                color (str) : camp group's color in hex format or html color string
        """
        self.name = name
        self.color = color

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class User(db.Model):
    """User Model

        SQL Alchemy Model of a User (for login only)
        Current User types are admins and parents
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String())
    role = db.Column(Enum(Role, name="role"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))  # will be blank if admin

    def __init__(self, email, password, role):
        """User Initializer

            Args:
                email (str) : user's email
                password (str) : user's password
                role (Role) : user's role

            .. note::
                User's password are encrypted on creation using the function
                werkzeug.security.generate_password_hash
        """
        # self.username = username
        self.email = email
        self.role = role
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if password is user's password

            Encrypts password and checks if user's saved password is equal
            to specified password using werkzeug.security.check_password_hash

            Args:
               password (str) : password to be checked

            Returns:
                True if password is user's password else False
        """
        return check_password_hash(self.password, password)

    def get_id(self):
        """Get User's id

            Getter for User's id. Used by flask_login

            Returns:
                user's id in the db
        """
        return self.id

    def is_authenticated(self):
        """Check if User is authenticated

            Check is current user is authenticated.
            Required by Flask Login

            Returns:
                True
        """
        return True

    def is_active(self):
        """Check if User is active

            Check is current user is active.
            Required by Flask Login

            Returns:
                True
        """
        return True
