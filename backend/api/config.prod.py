# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-15s - %(levelname)s: %(message)s"
)


SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///database.db"


DATETIME_FORMAT = "%Y%m%dT%H:%M:%S"


APPLICATION_ROOT = "/v1"