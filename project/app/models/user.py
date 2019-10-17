from project.app import database, bcrypt, app
from project.app.models.base import Base, ModelMixin
import uuid
import datetime
import jwt
import json
from ...app.misc.utils import DateTimeEncoder


class User(Base):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    # id =  database.Column(database.String, unique=True, nullable=False)
    name = database.Column(database.String(255), nullable=False)
    user_id = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    country = database.Column(database.String(255) )
    businesses = database.relationship('Business', backref='users',  lazy='dynamic', passive_deletes=True)
    is_admin = database.Column(database.Boolean, nullable=False, default=False)

# cascade="all, delete,delete-orphan",
    def __init__(self, name, user_id, password,country,is_admin):
        self.name = name
        self.user_id = user_id
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.country = country
        self.is_admin = is_admin

    def save(self):
        """
            save the new USer model into the database and commit the change
        """
        database.session.add(self)
        database.session.commit()
        return self.user_id

    def json(user):
        """
            create a json repr of the mode so that we can
        """
        #  TODO  what happens when this function is passed a None type this can happen if an object is required and it doesnt exist in db ?
        if user:
            usr =  { "name": user.name, "user_id": user.user_id, "password":user.password, "created_on":user.created_on, "last_update":user.updated_on, "country": user.country,"is_admin": user.is_admin}
            return usr
            # json.dumps(usr, indent=4, separators=(",", ":"), sort_keys=True, cls=DateTimeEncoder)
        return {} # TODO this is bad practice

    def get_object(cls, user_id):
        return get_user_by_id(user_id)

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(user_id=user_id).first()

    def check_password(self, pw):
        return bcrypt.check_password_hash(self.password, pw)

    @staticmethod
    def update_user(user, user_id):
        user_db = User.query.filter_by(user_id = user_id).first()
        if user_db:
            if user.get('name') :
                user_db.name = user["name"]
            if user.get("password"):
                user_db.password = bcrypt.generate_password_hash(user["password"], app.config.get("BCRYPT_LOG_ROUNDS")).decode()
            if user.get('is_admin'):
                user_db.is_admin = user["is_admin"]
            database.session.commit()
            return user_db
        return user_db


    def encode_jwt(self):
        """
        Generate authentication token
        returns : string
        """
        # TODO the jwt token package PyJwt has some issues with RSA keys, where it doesnt allow rsa keys that i generate locally, kindly see to this
        # TODO there might be  a better replacement for PyJwt which works , test them
        try:
            payload = {
                # "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": self.user_id,
                'is_admin': self.is_admin
            }
            token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return e

    @staticmethod
    def decode_jwt(auth_token):
        """
            Validate the auth token and decode it
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return {
                "status" : "valid",
                "data" : {
                    "user_id" : payload['sub'],
                "is_admin" : payload["is_admin"]
                }
            }
        except jwt.ExpiredSignatureError:
            return {
                "status" : "Expired",
                "message" : 'Signature expired. Please log in again.'
            }
        except jwt.InvalidTokenError:
            return {
                "status" : "Invalid",
                "message" : 'Invalid token. Please log in again.'
            }

    def get_all_biz(self):
        return self.businesses

    @classmethod
    def delete_object(cls, id):
        rows = cls.query.filter_by(id = id).delete()
        database.session.commit()
        return rows
