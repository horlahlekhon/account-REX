import unittest
import datetime

from project.app import database

from project.app.models.user import User
from project.app.tests.base import BaseTestCase
import uuid

class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        """
            test the encoding of jwt
        """
        user = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariChelseaRealmadrid","Nigeria",True)
        user.save()
        auth_token = user.encode_jwt()
        self.assertTrue(auth_token)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_jwt(self):

        """test the decoding of JWT"""
        user = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariChelseaRealmadrid","Nigeria",True)
        user.save
        auth_token = user.encode_jwt()
        token_obj = User.decode_jwt(auth_token)
        object_id, is_admin  = token_obj["data"]["user_id"], token_obj["data"]["is_admin"]
        self.assertTrue( object_id == user.user_id)
        self.assertTrue( is_admin == user.is_admin)


if __name__ == '__main__':
    unittest.main()
