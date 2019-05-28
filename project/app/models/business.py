from project.app import app, database
from sqlalchemy import ForeignKey
import uuid
import datetime
from project.app.models.base import Base


class Business(Base):
    __tablename__ = "businesses"
    # TODO many to one relationship with tghe model User is not well configured, this should be done ASAP

    object_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    id = database.Column(database.String, nullable=False, unique=True)
    name = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.object_id'))
    tax_percentage = database.Column(database.Float, nullable=False)
    country = database.Column(database.String)

    def __init__(self, id, name, user_id, tax_percentage, country ):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.tax_percentage = tax_percentage
        self.country = country


    @classmethod 
    def json(cls, biz):
    #    owner =  User.get_object(biz.owner)
       return {"name":biz.name, "owner" : biz.owner, "tax_percentage": biz.tax_percentage, "country":biz.country } 

    @classmethod
    def add_biz(cls, biz):
        business = Business(biz.name, biz.owner, biz.tax_percentage, biz.country)
        return business.save

    @classmethod
    def update_biz(cls, biz):
        business = Business.get_object(biz.object_id)
        if biz["name"] != '':
            business.name = biz["name"]
        if biz["owner"] != business.owner.object_id and biz["owner"] != 0 :
            owner = User.get_object(biz["owner"])
            business.owner = biz["owner"]
        if biz["tax_percentage"] != 0.0:
            business.tax_percentage = biz["tax_percentage"]
        if biz["country"] != business.country and biz["country"] != 0:
            country = Country.get_object(biz["country"])
            business.country = country.object_id
        database.session.commit()
        return business




    # Business(id=uuid.uuid4(),name="Sisyphus inc.",user_id=1,tax_percentage=2.00, country="Nige
    # Business(bid, "Sisyphus inc.", 1, 2.00, "Nigerua")
    # usr = User(id,"Lekan","Horlahlekhin@gmail.com", "Lekan","Nigeria","true")