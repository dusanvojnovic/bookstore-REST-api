from flask_restful import Resource
from models.bookstore import BookstoreModel
from schemas.bookstore import BookstoreSchema

NAME_ALREADY_EXISTS = "An bookstore with name '{}' already exists."
ERROR_ADDING = "An error occurred while adding the bookstore."
STORE_NOT_FOUND = "Bookstore not found."
STORE_DELETED = "Booktore deleted."

bookstore_schema = BookstoreSchema()
bookstore_list_schema = BookstoreSchema(many = True)

class Bookstore(Resource):
    @classmethod
    def get(cls, name):
        bookstore = BookstoreModel.find_by_name(name)
        if bookstore:
            return bookstore_schema.dump(bookstore), 200
        else:
            return {"message": STORE_NOT_FOUND}, 404 
    
    @classmethod
    def post(cls, name):
        if BookstoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400 # bad request

        bookstore = BookstoreModel(name = name)
        try:
            bookstore.save_to_db()
        except:
            return {"message": ERROR_ADDING}, 500 # internal server error

        return bookstore_schema.dump(bookstore), 201 # created

    @classmethod
    def delete(cls, name):
        bookstore = BookstoreModel.find_by_name(name)
        if bookstore:
            bookstore.delete_from_db()
            return {"message": STORE_DELETED}, 200
        
        return {"message": STORE_NOT_FOUND}, 404


class BookstoreList(Resource):
    @classmethod
    def get(cls):
        return {"bookstores": bookstore_list_schema.dump(BookstoreModel.find_all())}, 200