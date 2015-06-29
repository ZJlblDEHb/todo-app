# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging
from mock import patch, Mock
from base import BaseFuncTest
from backend.api.database import SessionWrapper
from backend.api.models import TaskModel
from backend.api.tools import form_output
from backend.api.handlers.tasks import TaskBase


logger = logging.getLogger(__name__)


class TestTask(BaseFuncTest):

    def _task_data(self, counter=0, done=False, progress=0):
        return {
            "title": "task %d" % counter,
            "text": "text for task %d" % counter,
            "done": done,
            "progress": progress
        }

    def test_get_all_tasks(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            tasks = list()
            for i in range(3):
                tasks.append(TaskModel(**self._task_data(counter=i)))
                self.session.add(tasks[-1])

            self.session.commit()

            expected_result = form_output(tasks, TaskBase._fields)

            r = self.client.get('/tasks')
            self.assertEquals(
                r.json,
                expected_result
            )