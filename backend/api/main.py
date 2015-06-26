# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


from flask import Flask
from database import shutdown_session
from flask.ext.restful import Api


app = Flask(__name__)
app.config.from_object('config')
api = Api(app)


app.teardown_appcontext(shutdown_session)