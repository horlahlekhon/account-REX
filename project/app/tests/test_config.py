from project.app.tests.base import BaseTestCase

from flask import current_app

from flask_testing import TestCase
from project.app import app

import unittest

class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_secret')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(current_app is None)

class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        # self.assertFalse(app.config['db'] is 'account_rex_test')

class TestProductionConfi(TestCase):

    def create_app(self):
        app.config.from_object('project.app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])

if __name__ == '__main__' :
    unittest.main()


