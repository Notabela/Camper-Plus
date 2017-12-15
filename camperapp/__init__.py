"""Camper+ Web Application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

# db_path = "postgresql+psycopg2://localhost/camper_plus"
mock_db_path = "sqlite:///test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = mock_db_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "0QZSIXW7U50133JZuZ6gpkwZ9yYCXY"
heroku = Heroku(app)
db = SQLAlchemy(app)

import camperapp.routes

db.create_all()
db.session.commit()