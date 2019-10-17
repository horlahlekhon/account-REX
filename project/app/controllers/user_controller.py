from ..models.user import User
from ..misc.dtos import UserDTO, BusinessDTO
from ..services.user_service import register_new_user, get_user, get_users, update_user, delete_user
from flask_restplus import Resource
from flask import g, request
from ...app.misc.logger import logger
import datetime
from project.app.misc.middlewares import auth_required
from werkzeug.exceptions import Unauthorized

api = UserDTO.api
_user = UserDTO.user
# _business = BusinessDTO.business

@api.route('/')
class Users(Resource):

    @api.doc("list_of_all_users")
    @api.response(401, "UNAUTHORIZED")
    @api.marshal_list_with(_user, skip_none=True)
    @auth_required
    def get(self):
        """
        get returns a list of all the users in the system

        Returns:
            dict -- json response that includes a response status and a list of users

        :raises Unauthorized: In case of something
        """
        # TODO this endpoint returns null is instead of respoinse message when token is not in the header, read about error handling to solve this issue
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

@api.route('/<user_id>')
@api.param('user_id', "the user's user_id used to register")
@api.response(404,"user not found")
class UserResource(Resource):

    @api.response(201, "User successfully updated")
    @api.doc("Updates an existing user")
    @api.marshal_with(_user)
    def put(self, user_id):
        """
        patch updates an existing user in the system
        
        Returns:
            response dict -- a response object that deals with the request
        """
        data = request.json
        return update_user(data, user_id)

    @api.doc("get a user")
    @api.marshal_with(_user)
    def get(self, user_id):
        """
        get returns a single user given its unique user_id

        Arguments:
            user_id {String} -- an user_id used to register

        Returns:
            json -- the requested user in json format
        """
        user, code  = get_user(user_id)
        if code == 404:
            api.abort(code=404, message="The User with the user_id doesnt Exist")
        return user, code

    
    @api.doc("delete a user")
    @api.response(201, "successfully deleted")
    def delete(self, user_id):
        """
        delete removes a user from the system
        
        Arguments:
            user_id {string} -- the user_id of the user to be removed
        
        Returns:
            tuple -- the response dict and the status code.
        """
        return delete_user(user_id)
    

# @api.route('/business')
# class UserBusiness(Resource):

#     @api.doc("Get all Businesses that belongs to a user")
#     @api.marshal_list_with(_business)
#     def get(self, user_id):
#         """
#         get returns businesses that belongs to a user
        
#         Arguments:
#             user_id {string} -- the user id of the user to whose businesses is to be
        
#         Returns:
#             Response -- the response object that correspond to the request. this returns 404 if the user is not found
#                         and 200 if the user is found plus the list of the passed in user's businesses
#         """

#         return get_user_biz(user_id)









