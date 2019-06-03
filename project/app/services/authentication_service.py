from ..models.user import User
from .blacklist_service import save_token
from ..services.user_service import register_new_user
from ...app import logger
from .user_service import get_user


class Authentication:

    @staticmethod
    def login(data):
        try:
            user = User.get_user_by_mail(data["email"])
            if user and user.checkpassword(data["password"]):
                auth_token = user.encode_jwt(user)
                logger.debug("user login request with: email={}, password={}".format(data["email"], data["password"]))
                if auth_token:
                    response_obj = {
                        "status" : "success",
                        "message" : "successfully logged in",
                        "auth token" : auth_token
                    }
                    return response_obj, 201
                response_obj = {
                    "status" : "failed",
                    "message" : "unable to create token, kindly try again"
                }
                return response_obj, 500
            response_obj = {
                "status" : "failed",
                "message" : "username or password isn't correct"
            }
            return response_obj, 401

        except Exception  as e:
            response_obj = {
                "status" : "failed",
                "message" : "something terrible is wrong"
            }
            return response_obj, 500

    @staticmethod
    def logout(header):
        if header:
            token = header.split(" ")[1]
        else:
            token = ' '
        decoded_token = User.decode_jwt(token)
        if decoded_token:
            if  decoded_token["status"] == "valid":
                return save_token(token)
            return decoded_token, 401
        response_obj = {
            "status" : "failed",
            "message" : "invalid token, please provide a valid one."
        }
        return response_obj, 401

    @staticmethod
    def get_logged_in_user(header):
        if header:
            token = header.split(" ")[1]
        else :
            token = " "
        decoded_token = User.decode_jwt(token)
        if decoded_token:
            if decoded_token["status" == "valid"]:
                user = decoded_token["data"]
                usr, code = User.json(get_user(user["id"]))
                response_obj = {
                    "status" : "success",
                    "data" : usr
                }
            return response_obj, 400
        return decoded_token, 400

