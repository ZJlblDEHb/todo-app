# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging
import simplejson as json
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

    def test_get_all_tasks_filter_by_all(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            done_tasks = list()
            for i in range(5):
                is_done = i % 2 == 0
                task = TaskModel(**self._task_data(counter=int(is_done), done=is_done))
                if is_done:
                    done_tasks.append(task)

                self.session.add(task)

            self.session.commit()

            params = {
                "title": "task 1",
                "done": "true"
            }

            expected_result = form_output(done_tasks, TaskBase._fields)

            r = self.client.get('/tasks', query_string=params)
            self.assertEquals(
                r.json,
                expected_result
            )

    def test_get_task_by_id(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            tasks = list()
            for i in range(5):
                tasks.append(TaskModel(**self._task_data(counter=i)))
                self.session.add(tasks[-1])

            self.session.commit()

            expected_result = form_output(tasks[2], TaskBase._fields)

            r = self.client.get('/tasks/%d' % tasks[2].id)
            self.assertEquals(
                r.json,
                expected_result
            )

    def test_delete_task_by_id(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            task = TaskModel(**self._task_data(counter=0))
            self.session.add(task)
            self.session.commit()

            r = self.client.delete('/tasks/%d' % task.id)

            result = self.session.query(TaskModel).all()

            self.assertEquals(
                len(result),
                0
            )

    def test_post_new_task(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            input_data = self._task_data(counter=0)
            self.client.post('/tasks', data=json.dumps(input_data), content_type='application/json')

            task = self.session.query(TaskModel).first()

            self.assertEquals(
                input_data,
                {key: getattr(task, key) for key in input_data.keys()}
            )

    def test_update_task(self):
        with patch('backend.api.handlers.tasks.session_wrapper') as session_wrapper_mock:

            session_wrapper_mock.return_value = SessionWrapper(session=self.session)

            input_data = self._task_data(counter=0, done=False)
            task = TaskModel(**input_data)
            self.session.add(task)
            self.session.commit()

            self.client.put('/tasks/%d' % task.id, data=json.dumps({"done": True}), content_type='application/json')

            new_task = self.session.query(TaskModel).get(task.id)
            input_data['done'] = True

            self.assertEquals(
                input_data,
                {key: getattr(new_task, key) for key in input_data.keys()}
            )