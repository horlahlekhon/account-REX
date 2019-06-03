from project.app.models.user import User
from project.app import database
import uuid
# from app.errors import DataError
from project.app.misc.logger import logger

def validate(data):
    """
    validate validate and verify the data provided when a new user wants to register

    Arguments:
        data {dict} -- the data that is recieved from request of registeration

    Returns:
        dict -- this dictionary describes ewhat happens and flag validated or not
    """
    usr =  User.get_user_by_mail(data["email"])
    logger.debug("user returned check {} ".format(usr))
    if isinstance(usr, User) :
        logger.debug("user exists already with that email == {}".format(usr))
        response_obj = {
            "status" : "failed",
            "message" : "user with that email already exists",
        }
        return response_obj, False
    if data["password"] == "" or len(data["password"]) < 8 :
        logger.debug("Password is too short")
        response_obj = {
            "status" : "failed",
            "message" : "password should be up to 8 characters"
        }
        return response_obj, False
    return {
        "status" : "success",
        "message" : "registered successfully"
    }, True


def register_new_user(data):
    logger.debug("user validation status == {}".format(validate(data)[0]["status"]))
    validation = validate(data)
    if validation[0]["status"] == "success":
        print("user validation status  == {}".format(validate(data)[0]["status"]))
        new_user = User(
            id=uuid.uuid4(),
            name=data["name"],
            email=data["email"],
            password=data["password"],
            country=data["country"],
            is_admin=data['is_admin']
        )
        new_user.save()
        return generate_token(new_user), 200
    return validation[0]["message"], 409


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
        return User.json(user), 200
    response_obj = {
        "status": "failed",
        "message": "The user you requested for cannot be found"
    }
    logger.debug(response_obj["message"])
    return response_obj, 404


def get_users():
    return [user for user in  User.get_all_objects()], 200


def update_user(data):
    return User.update_user(data), 200
