from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask import g, url_for

from .. import db
from .category import Category

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

    # Create a new item in the specified category
    @classmethod
    def create(cls, name, description, category_id):
        item = Item(name=name, description=description, category_id=category_id)
        db.session.add(item)
        db.session.commit()
        return 0

    @classmethod
    def getItemsByDate(cls, max=10):
        items = db.session.query(Item).order_by(Item.date_added.desc()).limit(max).all()
        return items

    @classmethod
    def getItemsByCategory(cls, category_id):
        items = db.session.query(Item).filter_by(category_id=category_id).order_by('name')
        return items

