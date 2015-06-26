# -*- encoding: utf-8 -*-


"""
Description.
"""


__author__ = 'ZJlblDEHb'


from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from main import Base, engine


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, default="Anonymous")
    email = Column(String, nullable=False, default="anonymous@mail.com")
    comments = relationship("CommentModel")
    scores = relationship("ScoreModel")
    tm_create = Column(DateTime, nullable=False, default=datetime.utcnow)
    tm_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScoreModel(Base):
    __tablename__ = "scores"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id"), primary_key=True, nullable=False)
    value = Column(Integer, nullable=False, default=0)
    tm_create = Column(DateTime, nullable=False, default=datetime.utcnow)
    tm_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(4048), nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id"))
    tm_create = Column(DateTime, nullable=False, default=datetime.utcnow)
    tm_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class TodoModel(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    text = Column(String(4048), nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    progress = Column(Integer, nullable=False, default=0)
    comments = relationship("CommentModel")
    scores = relationship("ScoreModel")
    tm_create = Column(DateTime, nullable=False, default=datetime.utcnow)
    tm_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)