from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import g, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import login_manager
from . import db

# You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

'''
# Base needs to be globally defined so it can be used as a base class
# for the ORM models
# '''


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    picture = db.Column(db.String(250))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password=None):
        # If no password is provided, set to a non-verifiable password hash
        if not password:
            self.password_hash = "#"
        else:
            self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(secret_key, expires_in=6000)
        return s.dumps({'id': self.id})

    # Delete this user from database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Return object data in easily serializable format"""
        s_user = {'id': self.id,
                  'username': self.username,
                  'email': self.email,
                  'picture': self.picture,
                  }
        i = 1+1

        return s_user

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Add a method to verify auth tokens here
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except BadSignature:
            return None
        except SignatureExpired:
            return None
        user_id = data['id']
        return user_id

    # Helper functions for User
    #
    # Create a new User
    @staticmethod
    def create(username, email, password=None, picture=None):

        assert (username)
        assert (email)

        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.picture = picture

        # Persist in database
        db.session.add(user)
        db.session.commit()

        # return id of created user
        return User.getID(email)

    @staticmethod
    def getID(email):
        try:
            user = db.session.query(User).filter_by(email=email).one()
            return user.id
        except:
            return None

    @staticmethod
    def getInfo(user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        return user


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
