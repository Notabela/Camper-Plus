"""Models in Camper APP"""

api_key = "AIzaSyDfnLfxNeG45N_tBtUutrB9K6-GYCtD7_I"


from camperapp import app
from app import db
from werkzeug import generate_password_hash, check_password_hash


db = SQLAlchemy()

class CampEvent(db.Model):
    __tablename__='event'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    start = db.Colum(db.DateTime())
    end = db.Column(db.DateTime())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)



    """Camp Event class representing an event on the calendar"""

    def __init__(self, title,start,end,group_id):
        self.title = event_title.title()
        self.start = event_start.title()
        self.end = event_end.title()
        self.group_id = group_id.title()

        """ it is not final """
    def __repr__(self):
        return '<CampEvent {}>'.format(self.title)



class Group(db.Model):
    __tablename__='group'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    color = db.Column(db.String())
    quantity = db.Column(db.Integer())
    camperevents = db.relationship('CampEvent', backref = 'group',lazy = 'dynamic')
    camper1_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)
    camper2_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)
    camper3_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)
    camper4_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)
    camper5_id = db.Column(db.Integer(), db.ForeignKey('camper.id', nullable=False)

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Parent(db.Model):
    __tablename__='parent'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    phone_number = db.Column(db.String())
    camper_id = db.Column(db.Integer, db.ForeignKey('camper.id'), nullable=False)
    campers = db.relationship('Camper',backref = 'parent',lazy = 'dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_active(self):
        return self.active is None or self.active

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Parent {}>'.format(self.name)


class Camper(db.Model):
    __tablename__='camper'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    age = db.Column(db.Integer())
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    groups = db.relationship('Groups',backref = 'camper',lazy = 'dynamic')
    parents = db.relationship('Parent',backref = 'camper',lazy = 'dynamic')
    def __repr__(self):
        return '<Camper {}>'.format(self.name)


class CampWorker(db.Model):
    __tablename__='camperworker'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    position = db.Column(db.String())
    def __repr__(self):
        return '<CampWorker {}>'.format(self.name)
