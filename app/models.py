from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import g

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


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    picture = Column(String(250))

    # Add a method to generate auth tokens here
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
    @staticmethod
    def create(login_session):

        # Abort if user already exists
        user = g.db_session.query(User).filter_by(email=login_session['email']).first()
        if user:
            return user.id

        # Create new user
        user = User(username=login_session['username'], email=login_session['email'],
                    picture=login_session['picture'])

        # Persist in database
        g.db_session.add(user)
        g.db_session.commit()

        # return id of created user
        return User.getID(login_session['email'])

    @staticmethod
    def getID(email):
        try:
            user = g.db_session.query(User).filter_by(email=email).one()
            return user.id
        except:
            return None

    @staticmethod
    def getInfo(user_id):
        return g.db_session(User).filter_by(id=user_id).one()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
        }


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
