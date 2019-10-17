from ..models.blacklist import BlackListToken
from ...app import database, logger

def save_token(token):
    black_T = BlackListToken(token=token)

    try:
        database.session.add(black_T)
        database.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        logger.debug("token saved as blacklist: token = {}".format(token))
        return response_object, 200
    except Exception as e:
        logger.debug("token saving failed, trace == {}".format(e))
        response_object = {
            "status" : "failed",
            "message" : e
        }
        return response_object, 500