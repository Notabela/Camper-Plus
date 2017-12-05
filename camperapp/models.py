"""Models in Camper APP"""
from camperapp import app
from marshmallow import Schema, fields
from datetime import datetime
from camperapp import db
from werkzeug import generate_password_hash, check_password_hash


class CampEvent(db.Model):
    """Camp Event class representing an event on the calendar"""
    __tablename__ = 'campevent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))

    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end
        self.color = None

    def add_color_attr(self):
        if self.group_id is None:
            return
        self.color = self.campgroup.color

    @classmethod
    def convert_calevent_to_campevent(cls, calevent):
        """Converts a Full Calendar calendar event to a CampEvent"""
        title = calevent['title']
        start_time =\
            CampEvent.convert_ISO_datetime_to_py_datetime(calevent['start'])
        end_time =\
            CampEvent.convert_ISO_datetime_to_py_datetime(calevent['end'])
        group_id = int(calevent['group_id'])

        camp_event = CampEvent(title, start_time, end_time)
        camp_event.group_id = group_id

        return camp_event

    @classmethod
    def convert_ISO_datetime_to_py_datetime(cls, ISO_datetime):
        """Converts the ISO datetime to a Python datetime"""
        return datetime.strptime(ISO_datetime, '%Y-%m-%dT%H:%M:%S')

    @classmethod
    def convert_py_datetime_to_ISO_datetime(cls, py_datetime):
        return py_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    def __repr__(self):
        return '<CampEvent {}>'.format(self.title)


class CampEventSchema(Schema):
    """Schema for camp event"""
    id = fields.Int()
    title = fields.Str()
    start = fields.DateTime()
    end = fields.DateTime()
    group_id = fields.Str()
    # this doesn't original exist in db, should be appended before serialization
    color = fields.Str()


class Parent(db.Model):
    """Parent class representing a Parent of Camper(s)"""
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    street_address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.Integer())
    campers = db.relationship('Camper', backref='parent', lazy='dynamic')

    def __repr__(self):
        return '<Parent {}>'.format(self.name)


class Camper(db.Model):
    """Camper class representing a Camper"""
    __tablename__ = 'camper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    birth_date = db.Column(db.Date())
    grade = db.Column(db.Integer())
    gender = db.Column(db.String())
    medical_notes = db.Column(db.String())
    phone = db.Column(db.String())
    street_address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.Integer())
    is_active = db.Column(db.Boolean())
    group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))
    parent_id = db.Column(db.Integer(), db.ForeignKey('parent.id'))

    def age(self):
        from datetime import date
        born = self.birth_date
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day - 1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def __repr__(self):
        return '<Camper {}, {}>'.format(self.last_name, self.first_name)


class CampGroup(db.Model):
    """Group Class representing a Group"""
    __tablename__ = 'campgroup'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    color = db.Column(db.String())
    campers = db.relationship('Camper', backref='campgroup', lazy='dynamic')
    events = db.relationship('CampEvent', backref='campgroup', lazy='dynamic')

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    pwdhash = db.Column(db.String())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    """
    To add a new item to database
    event = CampEvent(params)
    db.session.add(event)
    db.session.commit()

    To add a camper to a group, we can do either of the following/set secondary params
    camper.campgroup = Group
    CampGroup.campers.append(camper)
    camper.group_id = Group.id

    To query events
    User.query.all()  -> get all in the table
    User.query.first()
    User.query.get(3) -> get 3 elements

    User.query.first_or_404() -> returns 404 if not found
    User.query.limit(5) -> returns a query object that that we can use
    limits all our queries to 5 events

    User.query.order_by(User.username.desc()).limit(5).all()
    User.query.filter_by(username='alex', password="something").first()
    User.query.filter_by(username='alex', password="something").update({'password': 'different'})
    db.session.commit() to save our update changes

    db.session.delete(some_object)
    db.session.commit()

    QUERY ONE-TO-MANY RELATIONSHIPS
    #adding a relationship
    post.user_id = something.id
    user.posts.append(post)
    post.user = user

    group.campers.all() -> get all campers in the group
    user.posts.all()
    user.posts.limit(10).all()

    //iteration through
    for i in users.posts:
        print(i)

    Recommendations:
    1. webpack is kind of like Make that transforms you code to be used in production
    2. Gcc is replaced by Babel - transpiles your code to es6, react, etc. to stuff that will
    run on any browser
    3. React, React DOM or Vue
    4. ESlint
    """


# db.create_all()
# db.session.commit()

# class Group(db.Model):
#     __tablename__='group'
#     id = db.Column(db.Integer(), primary_key = True)
#     name = db.Column(db.String())
#     color = db.Column(db.String())
#     quantity = db.Column(db.Integer())
#     camperevents = db.relationship('CampEvent', backref = 'group',
#                         lazy = 'dynamic')
#     camper_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)
#     campers = db.relationship('Camper',backref = 'group',lazy = 'dynamic')
#
#     def __repr__(self):
#         return '<Group {}>'.format(self.name)
#
#
# class Parent(db.Model):
#     __tablename__='parent'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String())
#     email = db.Column(db.String())
#     password = db.Column(db.String())
#     phone_number = db.Column(db.String())
#     camper_id = db.Column(db.Integer, db.ForeignKey('camper.id'), nullable=False)
#     campers = db.relationship('Camper',backref = 'parent',lazy = 'dynamic')
#
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
#
#     def check_password(self, value):
#         return check_password_hash(self.password, value)
#
#     def is_active(self):
#         return self.active is None or self.active
#
#     def get_id(self):
#         return self.id
#
#     def __repr__(self):
#         return '<Parent {}>'.format(self.name)
#
#
#
#
# class CampWorker(db.Model):
#     __tablename__='camperworker'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String())
#     email = db.Column(db.String())
#     password = db.Column(db.String())
#     position = db.Column(db.String())
#     def __repr__(self):
#         return '<CampWorker {}>'.format(self.name)
