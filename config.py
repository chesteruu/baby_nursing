import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
path_separator = os.path.sep
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'baby_nursing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'something_secret'
