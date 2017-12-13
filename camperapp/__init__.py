"""Camper+ Web Application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://localhost/camper_plus"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "0QZSIXW7U50133JZuZ6gpkwZ9yYCXY"
heroku = Heroku(app)
db = SQLAlchemy(app)

import camperapp.routes
