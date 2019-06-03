from functools import wraps
from ...app import logger
from ..models.user import User
from ..services.authentication_service import Authentication as auth

def auth_required(func):
    @wraps(f)
    def authorization(*args , **kwargs):

        data, status = auth.get_logged_in_user(request)
        usr = data.get("data")

        if not usr:
            return data, status
        g.user = usr["name"]
        return func(*args, **kwargs)
    return authorization

