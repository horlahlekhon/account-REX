from functools import wraps
from ...app import logger
from ..models.user import User
from ..services.authentication_service import Authentication as auth
from flask import g, request

def auth_required(func):
    @wraps(func)
    def authorization(*args , **kwargs):

        data, status = auth.get_logged_in_user(request.headers.get("Authorization", ""))
        usr = data.get("data")

        if not usr:
            print("data {}, status {}".format(data, status))
            return data, status
        
        g.user = usr["name"]
        print("OOOOOOOOOHHHHHHHHHHHH no logged in user == {}".format(g.user))
        return func(*args, **kwargs)
    return authorization

