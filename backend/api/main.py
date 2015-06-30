# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging
from config import SQLALCHEMY_DATABASE_URI
from flask import Flask
from database import shutdown_session
from flask.ext.restful import Api
from handlers import TaskList, Task


logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
api = Api(app)


app.teardown_appcontext(shutdown_session)


api.add_resource(TaskList,  "/tasks")
api.add_resource(Task,      "/tasks/<int:id>")


logger.info("Loaded routes for REST api.")