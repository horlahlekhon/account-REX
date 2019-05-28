import unittest
import datetime

from project.app import database

from project.app.models.user import User
from project.app.services import user_service
from project.app.tests.base import BaseTestCase
import uuid


class TestUserServices(BaseTestCase):

    def test_save_new_user(self):
        """
        test_save_new_user tests the the service that saves new user
        """
        user = {
        "id": str(uuid.uuid4()),
        "name":"Lekan",
        "email":"Horlahlekhin@gmail.com",
         "password":"Lekan",
         "country":"Nigeria",
         "is_admin": True
        }

        res = user_service.save_new_user(user)
        id, is_admin  = User.decode_jwt(res[0]["authentication"])
        self.assertTrue(isinstance(res[0]["authentication"], bytes))
        self.assertTrue(res[0]["status"] == "success")
        self.assertTrue(is_admin)
        self.assertTrue(id == user["id"])
        self.assertTrue(res[1] == 200)

    def test_save_new_wrong_user(self):
        """
        test_save_new_wrong_user tests the save new user service to render reasonable message when 
        wrong details is passed in
        """
        user = {
            "id": str(uuid.uuid4()),
            "name":"Lekan",
            "email":"Horlahlekhin@gmail.com",
            "password":"Lekan",
            "country":"Nigeria",
            "is_admin": True
        }

        res = user_service.save_new_user(user)
        res2 = user_service.save_new_user(user)
        self.assertTrue(res2[0]["status"] == "failed")
        self.assertTrue(res2[0]["message"] == "user already exist")
        


