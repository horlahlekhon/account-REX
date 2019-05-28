import os

from  flask_bcrypt import Bcrypt
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from project.app.config  import DevelopmentConfig
import logging
from flask_migrate import Migrate, MigrateCommand
import click


import unittest
#from project.app.models import User, Business, Country


app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
bcrypt = Bcrypt(app)
database = SQLAlchemy(app)
from project.app.models.user import User
from project.app.models.business import Business
migrate =  Migrate(app,  database)

# set defaukt vatriables to be availbla in default shell context
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=database,
               User=User, Business=Business
               )

# @app.cli.command
# def create_db():
#     database.create_all()

# @app.cli.command
# def drop_db():
#     database.drop_all()

# @app.cli.command
# def test():

#     """
#      test cli command used to trigger test

#     """
#     tests = unittest.testLoader().discover('app/test', pattern='test*.py')
#     test_runner = unittest.TextTestRunner(verbosity=2)
#     test_runner.run(tests)



loglevels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG
}
logger = logging.getLogger(__name__)
formatter = logging.Formatter('{asctime}s {levelname}s {message}s' )
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(loglevels['debug'])


