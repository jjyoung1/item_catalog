from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, \
    ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    next = HiddenField('next')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    username = \
        StringField('Username',
                    validators=[DataRequired(), Length(1, 64),
                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                       'Usernames must have only letters, '
                                       'underscores, and periods')])

    password = \
        PasswordField('Password',
                      validators=[DataRequired(),
                                  EqualTo('password2',
                                          message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    next = HiddenField('next')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        if (User.query.filter_by(username=field.data).first()):
            raise ValidationError('Username already exists')
