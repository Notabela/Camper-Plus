"""Camper+ Web Application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

# db_path = "postgresql+psycopg2://localhost/camper_plus"
# mock_db_path = "sqlite:///test.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "0QZSIXW7U50133JZuZ6gpkwZ9yYCXY"

login_manager.init_app(app)
heroku = Heroku(app)
db = SQLAlchemy(app)

import camperapp.routes