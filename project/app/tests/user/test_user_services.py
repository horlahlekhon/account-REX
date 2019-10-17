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
        "user_id": str(uuid.uuid4()),
        "name":"Lekan",
        "user_id":"Horlahlekhin@gmail.com",
         "password":"LekanAdebariChelseaRealmadrid",
         "country":"Nigeria",
         "is_admin": True
        }

        res = user_service.register_new_user(user)
        token_obj = User.decode_jwt(res[0]["authentication"])
        user_id, is_admin  = token_obj["data"]["user_id"], token_obj["data"]["is_admin"]
        self.assertTrue(isinstance(res[0]["authentication"], str))
        self.assertTrue(res[0]["status"] == "success")
        self.assertTrue(is_admin)
        # self.assertTrue(user_id == user["user_id"])
        self.assertTrue(res[1] == 200)

    def test_save_new_wrong_user(self):
        """
        test_save_new_wrong_user tests the save new user service to render reasonable message when
        wrong details is passed in
        """
        user = {
            "name":"Lekan",
            "user_id":"Horlahlekhin@gmail.com",
            "password":"LekanAdebariChelseaRealmadrid",
            "country":"Nigeria",
            "is_admin": True
        }

        res = user_service.register_new_user(user)
        res2 = user_service.register_new_user(user)
        # self.assertTrue(res2[1]["status"] == "failed")
        self.assertTrue(res2[0] == "user with that user_id already exists")

    def test_get_user(self):
        """
        test_get_user tests the service function that returns a single user given a uuid of the user
        """
        user = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariChelseaRealmadrid","Nigeria",True)
        user_id = user.save()
        usr = user_service.get_user(user_id)
        self.assertTrue(usr[0]["name"] == user.name)
        self.assertFalse(usr[0]["user_id"] == "horl@gmail.com")
        self.assertTrue(isinstance(usr[0]["last_update"], datetime))
        self.assertFalse(usr[1] != 200)

        usr2 = user_service.get_user("23452254")
        self.assertTrue(usr2[1], 404)
        self.assertTrue(usr2[0]["status"], "failed")

    def test_delete_user(self):

        user = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariChelseaRealmadrid","Nigeria",True)
        user_id = user.save()
        count = user_service.delete_user(user_id)
        self.assertTrue(count[0]["status"] == "success")

    def test_update_user(self):
        user = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariChelseaRealmadrid","Nigeria",True)
        user_id = user.save()
        usr = User.get_user_by_id(user_id)
        update = {
            "name" : "Orwell",
            "password":"chelsearealmadrid"
        }
        updated = user_service.update_user(update, user_id)
        self.assertTrue(updated[0].check_password("chelsearealmadrid"))
        self.assertTrue(updated[0].name == update["name"])
        self.assertTrue(updated[0].password != update["password"])
        





