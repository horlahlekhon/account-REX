from models import User, Business, Country

from project.app import logger 


def getBusinesses(correlation_id):
    return Business.get_all_objects 


# def get_user_businesses(correlation_id, user_id):

#    try:
#        usr = User.get_object(user_id)
        
#    except Exception as e:

