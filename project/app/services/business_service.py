from project.app.models.business import Business
from project.app.models.user import User
import uuid
from project.app import logger
# from psycopg2 import IntegrityError

def save_biz(biz):
    user = User.get_object(biz["user_id"])
    if  user:
        business = Business(
            id = uuid.uuid4(),
            name = biz['name'],
            user_id =biz["owner"],
            tax_percentage=biz["tax_percentage"],
            country= biz["country"]
        )
        try:
            user.businesses.append(business)
            response = {
                "status" : "success",
                "message" : " Business saved succesfully"
            }
            logger.debug(response["message"] + "Business id === {bid}, user_id=={uid}".format(bid=business.id, uid=user.id))
            return response, 201
        except Exception as e:
            response = {
                "status" : "failed",
                "message" : "Something isnt right this will be resolved "
            }
            logger.debug(response["message"]+ "Exception trace : {}".format(e))
            return response, 500
    response = {
        "status" : "failed",
        "message": "somehow your user is not valid and are not allowed to add businesses, are you subscribed ?"
    }
    return response, 400


def get_biz(id, user_id):
    """
    get_biz get a single business that belong to a user
    
    Arguments:
        id {String} -- the id of the business
        user_id {String} -- the id of the user that is logged in or the user to which this business to be filtered belongs
    
    Returns:
        Tuple  -- a tuple of response message and a status code if a failure happens; or the required object
        in json format and http status code if there isnt any errors.
    """

    user = User.get_object(user_id)
    if user:
        biz = user.businesses.filter_by(id=id).first()
        if biz:
            return Business.json(biz), 200
        response = {
            "status" : "failed",
            "message" : "The requested business is not found"
        }
        return response, 404
    response = {
        "status" : "failed",
        "message" : "the user is not valid"
    }
    return response, 400

def get_all_biz(user):
    """
    get_all_biz gets all businesses for  a particular user

    Returns:
        List -- A list of busnesses that belongs to the logged in user
    """
    usr = User.get_object(user)
    if user:
        return [Business.json(biz) for biz in usr.busnesses.all()], 200
    response_obj = {
        "status" : "failed",
        "message" :  "the user is not valid"
    }
    return response_obj, 400


