# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


from flask import request
from flask.ext.restful import Resource


class Todo(Resource):
    """
    ККИ: получение по ID, редактирование
    """
    __fields = ["id", "name", "descr", "impacts", "tm_create", "tm_update"]


    @errors_handling()
    def get(self, id):
        """
        Получение ККИ по его ID.
        :param id:
        :return:
        """
        with session_wrapper(session=db.session) as session:
            k = session.query(kki.KKI).get(id)

            if k is None:
                return "", 404

            return json_generator.with_data(k, self.__fields), 200

    @errors_handling()
    @validate(mandatory=("id", ), optional=("name", "descr"))
    def put(self, id):
        """
        Редактирование ККИ
        :param id:
        :return:
        """
        with session_wrapper(session=db.session) as session:
            k = session.query(kki.KKI).get(id)

            if k is None:
                return "", 404

            for field in self.__fields:
                value = request.json.get(field)
                if value is not None:
                    setattr(k, field, value)

            session.flush()

            return json_generator.with_data(k, self.__fields), 200