from ..models.user import User
from .blacklist_service import save_token
from ..services.user_service import register_new_user
from ...app import logger
from .user_service import get_user


class Authentication:

    @staticmethod
    def login(data):
        try:
            user = User.get_user_by_id(data["user_id"])

            pwstatus = user.check_password(data["password"])
            if user and pwstatus:
                auth_token = user.encode_jwt()
                logger.debug("user login request with: user_id={}, password={}".format(data["user_id"], data["password"]))
                if auth_token:
                    response_obj = {
                        "status" : "success",
                        "message" : "successfully logged in",
                        "auth_token" : auth_token.decode()
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
                "message" : "something terrible is wrong , trace == {}".format(e)
            }
            return response_obj, 500

    @staticmethod
    def logout(header):
        if header:
            token = header.split(" ")[1]
        else:
            token = ' '
        decoded_token = User.decode_jwt(str(token))
        print("decoddddddddeeeeeeeeeeeed token in logout : {}, token itself :  {}".format(decoded_token, token))
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
        
        if decoded_token["status"] == "valid":
            user = decoded_token["data"]
            usr = User.json(User.get_user_by_id(user["user_id"]))
            response_obj = {
                "status" : "success",
                "data" : usr
            }
            return response_obj, 200
        return decoded_token, 401

