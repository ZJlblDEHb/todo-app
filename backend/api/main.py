# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from flask.ext.restful import Api


Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)


app = Flask(__name__)
app.config.from_object('config')
api = Api(app)