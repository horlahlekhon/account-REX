import unittest
from datetime import datetime

from project.app import database

from project.app.models.user import User
from project.app.services import user_service
from project.app.tests.base import BaseTestCase
import uuid


class TestUserServices(BaseTestCase):

    def test_register_new_user(self):
        """
        test_register_new_user tests the the service that saves new user
        """
        user = {
        "id": str(uuid.uuid4()),
        "name":"Lekan",
        "email":"Horlahlekhin@gmail.com",
         "password":"Lekan",
         "country":"Nigeria",
         "is_admin": True
        }

        res = user_service.register_new_user(user)
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

        res = user_service.register_new_user(user)
        res2 = user_service.register_new_user(user)
        self.assertTrue(res2[0]["status"] == "failed")
        self.assertTrue(res2[0]["message"] == "user already exist")

    def test_get_user(self):
        """
        test_get_user tests the service function that returns a single user given a uuid of the user
        """
        user = User(str(uuid.uuid4()),"Lekan","Horlahlekhin@gmail.com", "Lekan","Nigeria",True)
        id = user.save()
        usr = user_service.get_user(id)
        self.assertTrue(usr[0]["name"] == user.name)
        self.assertFalse(usr[0]["email"] == "horl@gmail.com")
        self.assertTrue(isinstance(usr[0]["last_update"], datetime))
        self.assertFalse(usr[1] != 200)

        usr2 = user_service.get_user("23452254")
        self.assertTrue(usr2[1], 404)
        self.assertTrue(usr2[0]["status"], "failed")



