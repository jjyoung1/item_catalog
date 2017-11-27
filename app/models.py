from sqlalchemy import Column, Integer, String, ForeignKey
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

# You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

'''
Base needs to be globally defined so it can be used as a base class
for the ORM models
'''
Base = declarative_base()

# Session is the factory for SQLAlchemy sessions.  It's created in the
# Model init_app() function
DBSession = None


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(128))
    email = Column(String(64), nullable=False, unique=True, index=True)
    picture = Column(String(250))

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
    # Checks to see if the User already exists.
    # Returns user.id if created
    # Otherwise it returns the existing user.id
    # @staticmethod
    # def create(username, email, password=None):
    #
    #     assert (username)
    #     assert (email)
    #
    #     # Abort if user already exists
    #     user = g.db_session.query(User).filter_by(email=email).first()
    #     if user:
    #         return user.id
    #
    #     # Create new user
    #     user = User()
    #     user.username = username
    #     user.email = email
    #     user.password = password
    #     user.picture = url_for('static', filename='image/generic_user.jpg')
    #
    #     # Persist in database
    #     g.db_session.add(user)
    #     g.db_session.commit()
    #
    #     # return id of created user
    #     return User.getID(email)

    @staticmethod
    def getID(email):
        try:
            user = g.db_session.query(User).filter_by(email=email).one()
            return user.id
        except:
            return None

    @staticmethod
    def getInfo(user_id):
        s = DBSession()
        user = s.query(User).filter_by(id=user_id).one()
        s.close()
        return user


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
        }

        # @staticmethod
        # def create(category_name):
        #     assert category_name
        #     try:
        #         category = Category(category_name)
        #         g.db_session.add(category)
        #         g.db_session.commit()
        #         category = g.db_session.query.filter(name=category_name).one()
        #         return category
        #
        #     except Exception as e:
        #         print(type(e))
        #         print(e.args)
        #         print(e)
        #         return None


class Item(Base):
    ''''''
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String(512))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category': self.category_id,
        }


def setup_db(app):
    global DBSession
    if DBSession is None:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Base.metadata.create_all(engine)

        # Create factory for Scoped Sessions
        DBSession = scoped_session(sessionmaker(bind=engine))


def init_app(app):
    setup_db(app)
