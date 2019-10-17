from project.app.services.authentication_service import Authentication
from project.app.misc.dtos import AuthDto

from flask_restplus import Resource
from flask import g, request
from ...app.misc.logger import logger
import datetime

api = AuthDto.api
_auth = AuthDto.user_auth

@api.route("/")
class UserLogin(Resource):
    """
    UserLogin user login resource
    """

    @api.doc("user login")
    @api.expect(_auth, validate=True)
    def post(self):
        request_data = request.json
        data = {
            "user_id" :request_data["email"],
            "password" : request_data["password"]
        }
        return Authentication.login(data)


@api.route("/logout")
class UserLogout(Resource):

    @api.doc("user logout")
    def post(self):
        header = request.headers.get("Authorization")
        return Authentication.logout(header=header)