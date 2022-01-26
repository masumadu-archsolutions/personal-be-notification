from sqlalchemy.exc import DBAPIError, IntegrityError

from app import db
from app.core.exceptions.app_exceptions import AppException
from app.core.exceptions.HTTPException import HTTPException
from app.core.repository.base.crud_repository_interface import CRUDRepositoryInterface


class SQLBaseRepository(CRUDRepositoryInterface):
    model: db.Model

    def __init__(self):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached
        """

        self.db = db

    def index(self):
        """

        :return: {list} returns a list of objects of type model
        """
        data = self.model.query.all()

        return data

    def create(self, obj_in):
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        try:
            obj_data = dict(obj_in)
            db_obj = self.model(**obj_data)
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except IntegrityError as e:
            raise AppException.OperationError(context=e.orig.args[0])

    def update_by_id(self, obj_id, obj_in):
        """
        :param obj_id: {int}
        :param obj_in: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise AppException.NotFoundException(
                f"Resource of id {obj_id} does not exist"
            )
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(context=e.orig.args[0])

    def find_by_id(self, obj_id: int):
        """
        returns an item if its id exists in the database

        :param obj_id: int - id of the user
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.query.get(obj_id)
        if db_obj is None:
            raise AppException.NotFoundException
        return db_obj

    def find(self, filter_param):
        """
        returns an item that satisfies the data passed to it if it exists in the database

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.query.filter_by(**filter_param).first()
        return db_obj

    def find_all(self, filter_param):
        """
        returns all items that satisfies the filter params passed to it

        :param filter_param: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.model.query.filter_by(**filter_param).all()
        return db_obj

    def delete(self, obj_id):

        """

        :param obj_id:
        :return:
        """

        db_obj = self.find_by_id(obj_id)
        if not db_obj:
            raise HTTPException(
                status_code=400, description="Resource does not exist"
            )  # noqa
        db.session.delete(db_obj)
        db.session.commit()
