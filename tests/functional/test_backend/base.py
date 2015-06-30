# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


import logging
from test_config import SQLALCHEMY_DATABASE_URI
from flask.ext.testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.api.main import api
from backend.api.database import Base


logger = logging.getLogger(__name__)


class BaseFuncTest(TestCase):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    def create_app(self):
        api.app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        return api.app

    def setUp(self):
        self.connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.Session.configure(bind=self.connection)
        self.session = self.Session(bind=self.connection)

    def tearDown(self):
        self.trans.rollback()
        self.session.close()
        self.connection.close()

    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=cls.engine)
        cls.engine = cls.engine
        cls.Session = sessionmaker()

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(bind=cls.engine)