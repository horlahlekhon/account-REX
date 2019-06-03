from ..models.user import User
from ..misc.dtos import UserDTO
from ..services.user_service import register_new_user, get_user, get_users
from flask_restplus import Resource
from flask import g, request
from ...app.misc.logger import logger
import datetime

api = UserDTO.api
_user = UserDTO.user

@api.route('/')
class Users(Resource):

    @api.doc("list_of_all_users")
    @api.marshal_list_with(_user, envelope="data")
    def get(self):
        """
        get returns a list of all the users in the system

        Returns:
            dict -- json response that includes a response status and a list of users
        """
        return get_users()

    @api.expect(_user, validate=True)
    @api.response(201, "User successfully created")
    @api.doc("Creates a new user")
    def post(self):
        """
        post creates a new user and register it

        Returns:
            json -- a response message and a response status code as appropriate
        """
        data = request.json
        return register_new_user(data)

@api.route('/<email>')
@api.param('email', "the user's email used to register")
@api.response(404,"user not found")
class UserResource(Resource):

    @api.doc("get a user")
    @api.marshal_with(_user)
    def get(self, email):
        """
        get returns a single user given its unique email

        Arguments:
            email {String} -- an email used to register

        Returns:
            json -- the requested user in json format
        """
        user, code  = get_user(email)
        logger.debug("get request")
        if code == 404:
            api.abort(code=404, message="The User with the email doesnt Exist")
        return user





