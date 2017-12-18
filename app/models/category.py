from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func

from .. import db


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
