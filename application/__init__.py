__author__ = 'nahla.errakik'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covid.db'

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()