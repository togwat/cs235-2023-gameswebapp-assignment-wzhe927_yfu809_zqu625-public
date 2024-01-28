from __future__ import annotations

from flask import redirect, url_for, session
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from games.domainmodel.model import User
import games.adapters.repository.abstractrepo as repo
from hashlib import sha256
from password_validator import PasswordValidator


def login_required(view):
    """Decorator for redirecting to login page if login is required"""

    @wraps(view)
    def wrap(**kwargs):
        """Redirect to login page if no user is found in session or repo"""
        if 'username' not in session or get_user(session['username']) is None:
            session.clear()
            return redirect(url_for('authentication_bp.login'))

        return view(**kwargs)

    return wrap


def add_user(username: str, password: str):
    """Add new user to repo for registration"""
    if repo.repo_instance.get_user(username) is None:
        # add new user, if user doesn't exist
        new_user = User(username, hash_password(password))
        repo.repo_instance.add_user(new_user)
    else:
        # username taken, registration fail
        raise NameNotUniqueException


def get_user(username: str) -> User | None:
    user = repo.repo_instance.get_user(username)
    if user:
        return user
    else:
        return None


def hash_password(password: str) -> str:
    """Return password string using sha256"""
    return sha256(password.encode()).hexdigest()


def check_password(plain: str, hashed: str) -> bool:
    """Check hashed password vs plaintext password and returns true/false"""
    return sha256(plain.encode()).hexdigest() == hashed


class ValidatePassword:
    """
    Password validator that makes sure a password is at least length 7, and
    contain at least a number, an uppercase letter, and a lowercase letter
    """
    def __init__(self, message=None):
        self.__message = message
        # default message
        if not message:
            self.__message = "Password failed requirements."

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(7) \
            .has().digits() \
            .has().uppercase() \
            .has().lowercase()
        if not schema.validate(field.data):
            raise ValidationError(self.__message)


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    # at least length 7, has at least one number, uppercase, lowercase
    # Regexp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{7,}
    password = PasswordField('Password:', validators=[
        DataRequired(),
        Length(min=7),
        ValidatePassword()])
    password_repeat = PasswordField('Repeat password:', validators=[
        DataRequired(),
        EqualTo('password')])
    submit = SubmitField('Register')


class NameNotUniqueException(Exception):
    """This username is taken"""
    pass
