# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


from httplib import OK, CREATED,  NOT_FOUND, BAD_REQUEST, INTERNAL_SERVER_ERROR
from flask import request
from flask.ext.restful import Resource
from database import session_wrapper
from models import TaskModel
from tools import form_output


class TaskBase(Resource):
    _fields = ["title", "text", "score", "done", "progress", "tm_create", "tm_update"]


class TaskList(TaskBase):
    """
    Contains handlers for task entity.
    """

    def get(self):
        """
        :param id:
        :return:
        """
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            return form_output(task, self._fields), OK

    def put(self):
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            for key, value in request.json.iteritems():
                setattr(task, key, value)

            session.flush()

            return form_output(task, self._fields), OK


class Task(TaskBase):
    """
    Contains handlers for todo entity.
    """

    def get(self, id):
        """
        :param id:
        :return:
        """
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            return form_output(task, self._fields), OK

    def put(self, id):
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            for key, value in request.json.iteritems():
                setattr(task, key, value)

            session.flush()

            return form_output(task, self._fields), OK