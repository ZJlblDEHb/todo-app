# -*- encoding: utf-8 -*-


"""
Description.
"""

__author__ = 'ZJlblDEHb'


from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def shutdown_session(exception=None):
    db_session.remove()


class SessionWrapper(object):
    """
    Context manager for sqlalchemy session.
    """
    def __init__(self, session, exceptions=()):
        """
        :param session: valid sqlalchemy session
        :param exceptions: - list of exceptions which needs to be suppressed
        :return:
        """
        self.session = session
        self.exceptions = exceptions

    def __enter__(self):
        """
        :return: - session object
        """
        return self.session

    def __exit__(self, type, value, traceback):
        """
        :param type:
        :param value: - exception if it was raised in context manager scope else None
        :param traceback:
        :return:
        """
        if value is not None:
            self.session.rollback()
            return isinstance(value, self.exceptions)

        else:
            try:
                self.session.commit()

            except Exception as e:
                self.session.rollback()
                if not isinstance(e, self.exceptions):
                    raise

            return True


def session_wrapper(session=None, exceptions=()):
    if session is None:
        session = db_session

    return SessionWrapper(session, exceptions)