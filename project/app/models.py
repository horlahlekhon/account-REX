# from project.app import bcrypt
from project.app import database, app
import datetime
import jwt

class Base(database.Model):
    __abstract__ = True
    created_on = database.Column(database.DateTime, default=database.func.now())
    updated_on = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())


class ModelManager(database.Model):
    
    __abstract__ = True

    @classmethod  
    def getObject(cls, object_id):
        """
            return a single user , given its primary key 
        """
        return cls.json(cls.query.filter_by(id=object_id).first())

    @classmethod 
    def get_all_objects(cls):
        return [cls.json(user) for user in cls.query.all()]

    @classmethod
    def delete_object(cls, object_id):
        rows = cls.query.filter_by(id = object_id).delete()
        #return eval("{}.query.filter_by(id = {} ).delete()".format(cls, obj.id))
        database.session.commit()
        return rows



class ObjectUtilMixin(object):

    @property
    def save(self):
        """
            save the new USer model into the database and commit the change
        """
        database.session.add(self)
        database.session.commit()
        return self.id


class User(ObjectUtilMixin,Base,ModelManager):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    is_admin = database.Column(database.Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, admin=False):
        super().__init__()
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password, 10).decode()
        self.admin = admin
        
    


    def json(user):
        """
            create a json repr of the mode so that we can 
        """
        return {"id": user.id, "name": user.name, "email": user.email, "created_on":user.created_on, "last_update":user.updated_on, "is_admin": user.is_admin}
    
    @classmethod
    def add_user(cls, user):
        user = User(user.email, user.name,user.password, user.admin)
        return user.save
    
    @staticmethod
    def update_user(user):
        user_db = User.query.filter_by(id = user.id).first()
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

    @staticmethod
    def encode_jwt(self, user_id):
        """
        Generate authentication token
        returns : string 
        """
        try:
            payload = {
                # "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
                'is_admin': is_admin
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def decode_jwt(auth_token):
        """
            Validate the auth token and decode it
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload, payload["is_admin"]
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.',False
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.',False
    

class Country(ObjectUtilMixin, ModelManager):
    __tablename__ = "country"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(244), nullable=False, unique=True)
    zip = database.Column(database.Integer,  nullable=False, unique=True)

    def __init__(self, name, zip):
        self.name = name
        self.zip = zip


class Business(ObjectUtilMixin, Base, ModelManager):

    __tablename__ = "business"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(255), nullable=False )
    owner = database.Column(database.Integer, database.ForeignKey('users.id'),nullable=False)
    tax_percentage = database.Column(database.Float, nullable=True)
    country = database.Column(database.Integer, database.ForeignKey('country.id'), nullable=False)

    def __init__(self, name, owner, tax_percentage, country):
        super().__init__()
        self.name = name
        self.owner = owner
        self.tax_percentage  = tax_percentage
        self.country = country
    
    @classmethod 
    def json(cls, biz):
       owner =  User.getObject(biz.owner)
       country = Country.getObject(biz.country)
       return {"name":biz.name, "owner" : owner.name, "tax_percentage": biz.tax_percentage, "country":country } 

    @classmethod
    def add_biz(cls, biz):
        business = Business(biz.name, biz.owner, biz.tax_percentage, biz.country)
        return business.save
    
    @classmethod 
    def update_biz(cls, biz):
        business = Business.getObject(biz.id)
        if biz["name"] != '':
            business.name = biz["name"]
        if biz["owner"] != business.owner.id and biz["owner"] != 0 :
            owner = User.getObject(biz["owner"])
            business.owner = biz["owner"]
        if biz["tax_percentage"] != 0.0:
            business.tax_percentage = biz["tax_percentage"]
        if biz["country"] != business.country and biz["country"] != 0:
            country = Country.getObject(biz["country"])
            business.country = country.id
        database.session.commit()
        return business 













