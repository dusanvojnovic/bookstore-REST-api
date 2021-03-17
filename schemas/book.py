from ma import ma
from models.book import BookModel
from models.bookstore import BookstoreModel

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
        load_only = ("bookstore",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
