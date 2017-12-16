from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask import g, url_for

from .. import db


'''
# Base needs to be globally defined so it can be used as a base class
# for the ORM models
# '''


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
        }

        # @staticmethod
        # def create(category_name):
        #     assert category_name
        #     try:
        #         category = Category(category_name)
        #         db.session.add(category)
        #         db.session.commit()
        #         category = db.session.query.filter(name=category_name).one()
        #         return category
        #
        #     except Exception as e:
        #         print(type(e))
        #         print(e.args)
        #         print(e)
        #         return None


class Item(db.Model):
    ''''''
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String(512))
    category_id = Column(Integer, ForeignKey('category.id'))
    date_added = Column(TIMESTAMP, server_default=func.now())
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category': self.category_id,
        }
