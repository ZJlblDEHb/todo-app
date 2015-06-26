# -*- encoding: utf-8 -*-


"""
Description.
"""


__author__ = 'ZJlblDEHb'


import datetime
from sqlalchemy.orm.collections import InstrumentedList
from config import DATETIME_FORMAT


def form_output(data, keys):
    if isinstance(data, (list, tuple)):
        return generate_objects_list(data, keys)

    else:
        return generate_single_object(data, keys)


def generate_objects_list(objects, keys):
    output = []
    for next_object in objects:
        output.append(generate_single_object(next_object, keys))
    return output


def generate_single_object(single_object, keys):
    output = {}
    for key in keys:
        attr = getattr(single_object, key)
        if isinstance(attr, InstrumentedList):
            output[key] = [element.id for element in attr]

        elif isinstance(attr, datetime.datetime):
            output[key] = attr.strftime(DATETIME_FORMAT)
        else:
            output[key] = attr

    return output