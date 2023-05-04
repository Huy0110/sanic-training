import uuid

from sanic import Blueprint
from sanic.response import json

from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.decorators.auth import protected
from app.hooks.error import ApiInternalError
from app.models.book import create_book_json_schema, Book

books_bp = Blueprint('books_blueprint', url_prefix='/books')

_db = MongoDB()


@books_bp.route('/')
async def get_all_books(request):
    # # TODO: use cache to optimize api
    print("Request: ", request.app.ctx.redis)
    # async with request.app.ctx.redis as r:
    #     books = await get_cache(r, CacheConstants.all_books)
    #     if books is None:
    #         book_objs = _db.get_books()
    #         books = [book.to_dict() for book in book_objs]
    #         await set_cache(r, CacheConstants.all_books, books)

    book_objs = _db.get_books()
    books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
@protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # # TODO: Save book to database
    inserted = _db.add_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')

    # TODO: Update cache

    return json({'status': 'success'})

@books_bp.route('/<book_id>')
async def get_book(request, book_id):
    # # TODO: use cache to optimize api
    print("Book id: ",book_id)
    book_obj = _db.get_book_by_id(book_id)
    if not book_obj:
        raise ApiInternalError('Book not found')

    return json(book_obj.to_dict())


@books_bp.route('/<book_id>', methods=['PUT'])
@protected  # TODO: Authenticate
async def update_book(request, book_id, username=None):
    body = request.json

    book_obj = _db.get_book_by_id(book_id)
    if not book_obj:
        raise ApiInternalError('Book not found')

    if book_obj.owner != username:
        raise ApiInternalError('User does not have permission to modify book')

    # Update book object
    book_obj.from_dict(body)
    print("Book obj: ", book_obj, body)

    # Update book in database
    result = _db.update_book(book_id, body)
    if not result:
        raise ApiInternalError('Fail to update book')

    # TODO: Update cache

    return json({'status': 'success'})


@books_bp.route('/<book_id>', methods=['DELETE'])
@protected  # TODO: Authenticate
async def delete_book(request, book_id, username=None):
    book_obj = _db.get_book_by_id(book_id)
    if not book_obj:
        raise ApiInternalError('Book not found')

    if book_obj.owner != username:
        raise ApiInternalError('User does not have permission to delete book')

    # Delete book from database
    result = _db.delete_book(book_id)
    if not result:
        raise ApiInternalError('Fail to delete book')

    # TODO: Update cache

    return json({'status': 'success'})



# TODO: write api get, update, delete book
