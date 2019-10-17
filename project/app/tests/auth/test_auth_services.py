from project.app.services.authentication_service import Authentication
from project.app.tests.base import BaseTestCase
from project.app.models.user import User


class TestAuthenticationServices(BaseTestCase):

    def test_login_service(self):
        usr = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariOluwaseun","Nigeria",True)
        usr.save()
        data = {
            "user_id" : "Horlahlekhin@gmail.com",
            "password": "LekanAdebariOluwaseun"
        }
        res = Authentication.login(data)
        jwt = User.decode_jwt(res[0]["auth_token"])
        self.assertTrue(res[0]["status"] == "success")
        self.assertTrue(isinstance(res[0]["auth_token"], str))
        self.assertTrue(jwt["status"] == "valid")
        self.assertTrue(jwt["data"]["user_id"] == data["user_id"])

    def test_logout_service(self):
        usr = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariOluwaseun","Nigeria",True)
        usr.save()
        data = {
            "user_id" : "Horlahlekhin@gmail.com",
            "password": "LekanAdebariOluwaseun"
        }
        res = Authentication.login(data)
        header = "Bearer {}".format(res[0]["auth_token"])
        logout = Authentication.logout(header=header)
        self.assertTrue(logout[0]["status"] == "success")

    def test_get_logged_in_user(self):
        usr = User("Lekan","Horlahlekhin@gmail.com", "LekanAdebariOluwaseun","Nigeria",True)
        usr.save()
        data = {
            "user_id" : "Horlahlekhin@gmail.com",
            "password": "LekanAdebariOluwaseun"
        }
        res = Authentication.login(data)
        header = "Bearer {}".format(res[0]["auth_token"])
        data = Authentication.get_logged_in_user(header=header)
        usr = data["data"]
        self.assertTrue(usr["name"] == "Lekan")
