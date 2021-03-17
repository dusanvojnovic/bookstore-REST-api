from ma import ma
from models.bookstore import BookstoreModel
from models.book import BookModel
from schemas.book import BookSchema

class BookstoreSchema(ma.SQLAlchemyAutoSchema):
    books = ma.Nested(BookSchema, many = True)
    class Meta:
        model = BookstoreModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True