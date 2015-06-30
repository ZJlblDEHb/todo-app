# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging
from httplib import OK, CREATED,  NOT_FOUND, BAD_REQUEST, INTERNAL_SERVER_ERROR
from flask import request
from flask.ext.restful import Resource
from backend.api.decorators import validate, JSON_INPUT, QUERY_INPUT
from backend.api.database import session_wrapper
from backend.api.models import TaskModel
from backend.api.tools import form_output


logger = logging.getLogger(__name__)


class TaskBase(Resource):
    _fields = ["title", "text", "score", "done", "progress", "tm_create", "tm_update"]


class TaskList(TaskBase):
    """
    Contains handlers for task entities.
    """

    logger.debug("wtf?")

    @validate(
        request=request,
        optional=(
            {
                "name": "title",
                "field_type": str
            },
            {
                "name": "done",
                "field_type": bool
            },
            {
                "name": "limit",
                "field_type": int
            },
            {
                "name": "offset",
                "field_type": int
            }
        ),
        source=QUERY_INPUT
    )
    def get(self, fields):
        """
        :param id:
        :return:
        """
        with session_wrapper() as session:
            query = session.query(TaskModel)

            title, done, limit, offset = [fields.get(key) for key in ("title", "done", "limit", "offset")]
            if title is not None:
                query = query.filter(TaskModel.title.like(title))

            if done is not None:
                query = query.filter(TaskModel.done == done)

            if limit is not None:
                query = query.limit(limit)

            if offset is not None:
                query = query.offset(offset)

            tasks = query.all()

            return form_output(tasks, self._fields), OK

    @validate(
        request=request,
        mandatory=(
            {
                "name": "title",
                "field_type": str
            },
            {
                "name": "text",
                "field_type": str
            },
        ),
        optional=(
            {
                "name": "progress",
                "field_type": int
            },
            {
                "name": "done",
                "field_type": bool
            }

        ),
        source=JSON_INPUT
    )
    def post(self, fields):
        with session_wrapper() as session:
            task = TaskModel(**fields)
            session.add(task)
            session.flush()
            return form_output(task, self._fields), CREATED


class Task(TaskBase):
    """
    Contains handlers for todo entity.
    """

    @validate(request=request)
    def get(self, fields, id):
        """
        :param id:
        :return:
        """
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            return form_output(task, self._fields), OK

    @validate(
        request=request,
        optional=(
            {
                "name": "title",
                "field_type": str
            },
            {
                "name": "text",
                "field_type": str
            },
            {
                "name": "progress",
                "field_type": int
            },
            {
                "name": "done",
                "field_type": bool
            }

        ),
        source=JSON_INPUT
    )
    def put(self, fields, id):
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            for key, value in fields.iteritems():
                setattr(task, key, value)

            session.flush()

            return form_output(task, self._fields), OK

    @validate(request=request)
    def delete(self, fields, id):
        """
        :param id:
        :return:
        """
        with session_wrapper() as session:
            task = session.query(TaskModel).get(id)

            if task is None:
                return "", NOT_FOUND

            session.delete(task)
            session.flush()

            return "", OK