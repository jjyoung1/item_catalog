from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from validate_email import validate_email

Base = declarative_base()

# You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String(64), index=True)
    password_hash = Column(String(64))
    picture = Column(String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

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
    # Checks to see if the User already exists.  If not then it's
    # created.  Otherwise it returns an error
    @staticmethod
    def create(**kargv):
        ''''''
        session = Session()

        username = kargv.get('username')
        password = kargv.get('password')
        email = kargv.get('email')

        # Confirm required arguments provided
        if username is None:
            raise ValueError("Missing required argument: username")
        if password is None:
            raise ValueError("Missing required argument: password")
        if email is None or not validate_email(email) :
            raise ValueError("Missing or illegal email address")

        # Abort if user already exists
        user = session.query(User).filter_by(email=email).one()
        if user:
            return None

        # Create new user
        user = User(username=username, password=password, email=email)

        # Encrypt password
        user.hash_password()
        # Persist in database

        session.remove()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'category': self.category,
            'price': self.price
        }


def init_app(app):
    global engine
    global Session

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)

    # Create factory for Scoped Sessions
    session_factory = sessionmaker(bind = engine)
    Session = scoped_session(session_factory)
