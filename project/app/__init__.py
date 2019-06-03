import os

from  flask_bcrypt import Bcrypt
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from project.app.config  import DevelopmentConfig
import logging
from flask_migrate import Migrate, MigrateCommand
import click
from flask import json
from ..app.misc.logger import logger



import unittest
#from project.app.models import User, Business, Country


app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
bcrypt = Bcrypt(app)
database = SQLAlchemy(app)
from project.app.models.user import User
from project.app.models.business import Business
from project.app.models.blacklist import BlackListToken
migrate =  Migrate(app,  database)

# set defaukt vatriables to be availbla in default shell context
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=database,
               User=User, Business=Business,BlackListToken=BlackListToken
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
from project.app.controllers.user_controller import api as user_namespace
from flask_restplus import Api
from flask import Blueprint

blueprint = Blueprint('api', __name__)

api = Api(
        blueprint,
        title='ACCOUNT-REX',
        version='1.0',
        description="An api for managing the finances of small scale businsesses "
)
api.add_namespace(user_namespace,path='/user')

app.register_blueprint(blueprint, url_prefix='/api')

app.app_context().push()


# postman import 

basedir = os.path.abspath(os.path.dirname(".."))

postman_dir = os.path.join(basedir,'postman.json')

def import_postman():
        # logger.debug("writting to postman file ")
        urlvars = True
        swagger = True
        data = api.as_postman(urlvars=urlvars, swagger=swagger)
        file = open(postman_dir, 'w')
        file.write(json.dumps(data))

with app.app_context():
        import_postman()

