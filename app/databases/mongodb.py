from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.user import User
from app.models.book import Book
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = f'mongodb://huy:123@localhost:27017/?authSource=trainingSanic&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
        # self.connection_url = connection_url.split('@')[-1]
        print(connection_url)
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]

        self._books_col = self.db[MongoCollections.books]
        self._users_col = self.db[MongoCollections.users]

        # print(self.connection_url)
        print(MongoDBConfig.DATABASE)
        print(MongoCollections.books)

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []
    
    def get_book_by_id(self, book_id, projection=None):
        try:
            query = {'_id': book_id}
            print("query: ", query)
            cursor = self._books_col.find(query, projection=projection)
            print("cursor: ", cursor.count())
            return Book().from_dict(cursor[0])
        except Exception as ex:
            logger.exception(ex)
        return None

    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def update_book(self, book_id: str, update_fields: dict):
        """
        Update a book with the given ID.
        :param book_id: str: ID of the book to update.
        :param update_fields: dict: Dictionary of fields to update.
        :return: bool: True if the book was updated, False otherwise.
        """
        try:
            result = self._books_col.update_one({"_id": book_id}, {"$set": update_fields})
            return result.modified_count > 0
        except Exception as ex:
            logger.exception(ex)
        return False

    def delete_book(self, book_id: str):
        """
        Delete a book with the given ID.
        :param book_id: str: ID of the book to delete.
        :return: bool: True if the book was deleted, False otherwise.
        """
        try:
            result = self._books_col.delete_one({"_id": book_id})
            return result.deleted_count > 0
        except Exception as ex:
            logger.exception(ex)
        return False
            
    def get_user_by_username(self, username: str):
        try:
            query = {'username': username}
            print("query: ", query)
            cursor = self._users_col.find(query)
            print("cursor: ", cursor)
            return User().from_dict(cursor[0])
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def add_user(self, user: User):
        try:
            inserted_doc = self._users_col.insert_one(user.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
    
    # TODO: write functions CRUD with books
