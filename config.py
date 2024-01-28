from os import environ
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()


class Config:
    TESTING = environ.get('TESTING')

    SECRET_KEY = environ.get('SECRET_KEY')

    REPOSITORY = environ.get('REPOSITORY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    # convert string to boolean value
    echo_value = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo_value.strip().lower() == 'true':
        SQLALCHEMY_ECHO = True
