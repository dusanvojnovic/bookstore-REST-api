from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.book import BookModel
from schemas.book import BookSchema
from marshmallow import ValidationError


NAME_ALREADY_EXISTS = "An book with name '{}' already exists."
ERROR_ADDING = "An error occurred while adding the book."
BOOK_NOT_FOUND = "Book not found."
BOOK_DELETED = "Book deleted."

book_schema = BookSchema()
book_list_schema = BookSchema(many = True)

class Book(Resource):
    @classmethod
    def get(cls, name):
        book = BookModel.find_by_name(name)
        if book:
            return book_schema.dump(book), 200
        return {"message": BOOK_NOT_FOUND}, 404 # not found  

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name):
        if BookModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400 # bad request
        
        book_json = request.get_json()
        book_json["name"] = name

        book = book_schema.load(book_json)
        
        try:
            book.save_to_db()
        except:
            return {"message": ERROR_ADDING}, 500 # internal server error
        
        return book_schema.dump(book), 201 # created 

    @classmethod
    @jwt_required()
    def put(cls, name):
        book_json = request.get_json()
        book = BookModel.find_by_name(name)

        if book:
            book.price = book_json["price"]
        else:
            book_json["name"] = name
            book = book_schema.load(book_json)
           
        book.save_to_db()

        return book_schema.dump(book), 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, name):
        book = BookModel.find_by_name(name)
        if book:
            book.delete_from_db()
            return {"message": BOOK_DELETED}, 200
        return {"message": BOOK_NOT_FOUND}, 404


class BookList(Resource):
    @classmethod
    def get(cls):
        return {"books": book_list_schema.dump(BookModel.find_all())}


