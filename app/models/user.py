from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import random, string
from .. import db
from .. import login_manager

# You will use this secret key to create and verify your tokens
secret_key = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False,
                         index=True)
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

    def generate_auth_token(self, expires_in=6000):
        s = Serializer(secret_key, expires_in=expires_in)
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
        except SignatureExpired:
            return None
        except BadSignature:
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
