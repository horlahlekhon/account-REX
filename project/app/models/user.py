from project.app import database, bcrypt, app
from project.app.models.base import Base, ModelMixin
import uuid
import datetime
import jwt
import json
from ...app.misc.utils import DateTimeEncoder


class User(Base):
    __tablename__ = "users"

    object_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    id =  database.Column(database.String, unique=True, nullable=False)
    name = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    country = database.Column(database.String(255) )
    created_on = database.Column(database.DateTime, default=database.func.now())
    updated_on = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())
    businesses = database.relationship('Business', backref='users', cascade="all, delete-orphan", lazy='dynamic')
    is_admin = database.Column(database.Boolean, nullable=False, default=False)

    def __init__(self,id, name, email, password,country,is_admin):
        self.id = id
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.country = country
        self.is_admin = is_admin

    def save(self):
        """
            save the new USer model into the database and commit the change
        """
        database.session.add(self)
        database.session.commit()
        return self.id

    def json(user):
        """
            create a json repr of the mode so that we can
        """
        #  TODO  what happens when this function is passed a None type this can happen if an object is required and it doesnt exist in db ?
        if user:
            usr =  {"id": user.id, "name": user.name, "email": user.email, "created_on":user.created_on, "last_update":user.updated_on, "country": user.country,"is_admin": user.is_admin}
            return usr
            # json.dumps(usr, indent=4, separators=(",", ":"), sort_keys=True, cls=DateTimeEncoder)
        return {} # TODO this is bad practice

    @staticmethod
    def get_user_by_mail(email):
        return User.query.filter_by(email=email).first()

    def check_password(self, pw):
        return bcrypt.checkpw(pw, self.password)

    @staticmethod
    def update_user(user):
        user_db = User.query.filter_by(user_id = user.object_id).first()
        if user_db:
            if user["name"] != '':
                user_db.name = user["name"]
            if user["email"] != '':
                user_db.email = user["email"]
            if user["password"] != '':
                user_db.password = user["password"]
            if user["is_admin"] != user["is_admin"]:
                user_db.is_admin = user["is_admin"]
            database.session.commit()
            return User.json(user_db)
        return user


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
                "sub": self.id,
                'is_admin': self.is_admin
            }
            token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return str(token)
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
                    "id" : payload['sub'],
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
