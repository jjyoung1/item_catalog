from sqlalchemy import Column, Integer, String, \
    ForeignKey, TIMESTAMP, func, exc

from .. import db
from sqlalchemy.exc import IntegrityError


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

    @staticmethod
    def create(category_name):
        try:
            assert category_name
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            category = db.session.query(Category).filter_by(name=category_name).one()
            return category
        except IntegrityError as e:
            db.session.rollback()
            raise

    @staticmethod
    def getAll():
        categories = db.session.query(Category)
        return categories
