from flask_restplus import Namespace, fields

class UserDTO:
    api = Namespace('user', description='User related ops')
    user = api.model('user', {
        'name' : fields.String(required=True,  description='user name for registeration'),
        "user_id" : fields.String(required=True, description='The user email, keep in mind , it should be unique'),
        "password" : fields.String(required=True, description="The password to be used to log in"),
        "created_on" : fields.DateTime(dt_format='rfc822', description="The date when this object was created"),
        "last_update" : fields.DateTime(dt_format='rfc822', description="The date of last update"),
        "country": fields.String(description="The country where the user is taxed to"),
        "is_admin" : fields.Boolean(required=True, description="The flag to determine if this user is an adminidterator of \ "
            + "a business or just a regular user delegated to perform basic ops on a business")
    })


class BusinessDTO:
    api = Namespace('business', description='allow operations on business')
    business = api.model('business', {
        'name' : fields.String(required=True, description="The name given to the business"),
        "user_id" : fields.String(required=True, description="The identification fo the owner of this business, as business cannot exist without an owner"),
        "tax_percentage" : fields.Float(required=True, description="The tax percentage of the business to be used to calculate income statement"),
        "country" : fields.String(description="The country where the business operates, input the country of the HQ if there is multiple branches")
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
