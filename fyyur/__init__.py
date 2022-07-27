from flask import Flask, flash, render_template, redirect, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


appFlask = Flask(__name__)
#app configs
appFlask.config['SECRET_KEY'] = '2de5a42478640f40a1000b7886e028eca722'
appFlask.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:inietim607@localhost:5432/alx'
appFlask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# package instances
db = SQLAlchemy(appFlask)
migrate = Migrate(appFlask, db)

from fyyur import views