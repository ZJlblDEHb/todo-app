# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'asergeev'


import logging
from backend.api.main import app, api
from tasks import Task, TaskList


logger = logging.getLogger(__name__)


api.add_resource(TaskList,  "/")
api.add_resource(Task,      "/tasks/<int:id>")


logger.info("Loaded routes for REST api.")