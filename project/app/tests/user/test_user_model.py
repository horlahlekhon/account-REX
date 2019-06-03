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
        user = User(str(uuid.uuid4()),"Lekan","Horlahlekhin@gmail.com", "Lekan","Nigeria",True)
        user.save
        auth_token = user.encode_jwt()
        self.assertTrue(auth_token)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_jwt(self):

        """test the decoding of JWT"""
        user = User(str(uuid.uuid4()),"Lekan","Horlahlekhin@gmail.com", "Lekan","Nigeria",True)
        user.save
        auth_token = user.encode_jwt()
        object_id, is_admin = User.decode_jwt(auth_token)
        self.assertTrue( object_id == user.id)
        self.assertTrue( is_admin == user.is_admin)


if __name__ == '__main__':
    unittest.main()
