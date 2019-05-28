import unittest

from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager

from project.app import app, database, migrate
from project.app.models import *

manager = Manager(app)

manager.add_command('database', MigrateCommand)


@manager.command
def create_db():
    database.create_all()

@manager.command
def drop_db():
    database.drop_all()

@manager.command
def test():

    """
     test cli command used to trigger test

    """
    tests = unittest.TestLoader().discover('project/app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1




if __name__ == "__main__":
    manager.run()
