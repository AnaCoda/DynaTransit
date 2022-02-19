#pip install flask
#pip install geopy
#pip install SQLAlchemy
#pip install Bcrypt
#pip install flask_login
#pip install functools  
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "jua868424241e29d0ae0d88abed3a6df3"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)

from dynatransit import routes