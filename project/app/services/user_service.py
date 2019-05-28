from project.app.models.user import User
from project.app import database
import uuid
# from app.errors import DataError
from project.app import logger


def save_new_user(data):
    usr = User.get_object(data["id"])
    if not usr:
        new_user = User(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            country=data["country"],
            is_admin=data['is_admin']
        )
        new_user.save()
        return generate_token(new_user), 200
    return {
            "status": "failed",
            "message": "user already exist"}, 409


def generate_token(user):
    """
        generate a  new authenmtication token for a new user
    """
    try:
        auth_token = user.encode_jwt()
        response_object = {
            "status": "success",
            "message": "successfully created",
            "authentication": auth_token
        }
        return response_object
    except Exception as e:
        response_obj = {
            "status": "failed",
            "message": "Something terrible happened while creating your token"
        }
        logger.debug(response_obj)
        return response_obj


def get_user(id):
    user = User.get_object(id)
    if user:
        logger.debug("user id = {}".format(user.id))
        return user, 200
    response_obj = {
        "status": "failed",
        "message": "The user you requested for cannot be found"
    }
    logger.debug(response_obj["message"])
    return response_obj, 404


def get_users():
    return User.get_all_objects, 200


def update_user(data):
    return User.update_user(data), 200
