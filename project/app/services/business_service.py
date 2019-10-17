from project.app.models.business import Business
from project.app.models.user import User
import uuid
from project.app import logger
# from psycopg2 import IntegrityError

def create_biz(biz):
    user = User.get_user_by_mail(biz["user_id"])
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
        biz = user.businesses.filter_by(id=id)
        return biz, 200
    response = {
        "status" : "failed",
        "message" : "the user is not valid"
    }
    return response, 400

def get_all_biz(user=None):
    """
    get_all_biz gets all businesses for  a particular user

    Returns:
        List -- A list of busnesses that belongs to the logged in user
    """
    if user:
        usr = User.get_object(user)
        if usr:
            return usr.businesses.all(), 200
        response_obj = {
            "status" : "failed",
            "message" :  "the user is not valid"
        }
        return response_obj, 403
    return Business.get_all_objects, 200

def update_biz(id, data, user_id):

    user =  User.get_user_by_id(user_id)
    biz = Business.get_object(id)
    if user and biz:
        return Business.update_biz(id, data), 201
    response_obj = {
        "status" :"failed",
        "message" : "The business is not valid"
    }
    return response_obj, 406

def delete_business(user_id, id):
    usr = User.get_user_by_id(user_id)
    if usr:
        bizs = usr.businesses.filter_by(id=id).delete()
        resp = {
            "status" : "success",
            "message" : "entries deleted : {}".format(bizs)
        }
        return resp, 200
    resp = {
        "status" : "failed",
        "message" :"invalid user"
    }
    return resp, 403



