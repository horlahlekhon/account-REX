from flask_testing import TestCase

from project.app import app, database
from project.app.models import *

class BaseTestCase(TestCase):

    def create_app(self):

        """
            Base test case
        """
        app.config.from_object('project.app.config.TestingConfig')
        return app

    def setUp(self):
        database.create_all()
        database.session.commit()

    def tearDown(self):
        database.session.remove()
        database.drop_all()


