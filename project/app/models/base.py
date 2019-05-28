from project.app import database, app
import datetime
import jwt



class ModelMixin(object):
    __abstract__ = True

    @classmethod
    def get_object(cls, id):
        """
            return a single object , given its primary key
        """
        return cls.json(cls.query.filter_by(id=id).first())

    @classmethod
    def get_all_objects(cls):
        return [cls.json(user) for user in cls.query.all()]

    @classmethod
    def delete_object(cls, object_id):
        rows = cls.query.filter_by(object_id = object_id).delete()
        #return eval("{}.query.filter_by(object_id = {} ).delete()".format(cls, obj.object_id))
        database.session.commit()
        return rows

    def save(self):
        """
            save the new USer model into the database and commit the change
        """
        database.session.add(self)
        database.session.commit()
        return self.id


# class Country(ModelManager):
#     __tablename__ = "country"

#     object_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
#     name = database.Column(database.String(244), nullable=False, unique=True)
#     zip = database.Column(database.Integer,  nullable=False, unique=True)

#     def __init__(self, name, zip):
#         self.name = name
#         self.zip = zip

class Base(database.Model,ModelMixin):
    __abstract__ = True

    created_on = database.Column(database.DateTime, default=database.func.now())
    updated_on = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())
