import db.queries as queries
import re
from datetime import datetime



def is_valid_isbn(isbn):
    return re.match(r"^\d{10}$",isbn)


def is_valid_year(year):
    current_year = datetime.now().year

    try:
        return 1000 <= int(year) <= current_year
    except:
        return False


def format_books(rows):
    return [
        {
            "id": r[0],
            "title": r[1],
            "isbn": r[2],
            "published_year":r[3],
            "author":{
                "author_id": r[4],
                "author_name": r[5]
            }
         } for r in rows
    ]


def books_handler(query, params=None):
    
    if params:
        id = params.get("id")
        row = queries.get_books(id=id)
        if row:
            data = format_books([row])
            return 200, {
                "status": "success",
                "data": data
            }
        return 404, {
            "error": "Not found"
        }
        
    
    title = query.get("title",[None])[0]
    author = query.get("author",[None])[0]
    year = query.get("year",[None])[0]
    sort = query.get("sort",[None])[0]
    order = query.get("order",["desc"])[0]

    rows = queries.get_books(title,author,year,sort,order)

    data = format_books(rows)
    
    return 200, {"status":"success", "data":data}

def create_book_handler(data):
    title = data.get("title")
    isbn = data.get("isbn")
    published_year = data.get("published_year")
    author_id = data.get("author_id")

    if not title or len(title)<1 :
        return 400, {
            "status": "error",
            "message": "title must be atleast 1 character"
        }
    
    if not isbn or not is_valid_isbn(isbn):
        return 400, {
            "status": "invalid isbn"
        }
    
    if not published_year or not is_valid_year(published_year):
        return 400, {
            "status": "error",
            "message": "invalid published_year"
        }
    
    if not author_id:
        return 400, {
            "status": "error",
            "message": "author_id is required"
        }

    if not queries.get_authors(id=author_id):
        return 400, {
            "status": "error",
            "message": "author doesn't exist"
        }
    
    try:
        rows = queries.create_book(title, isbn, published_year, author_id)
        
        book = {
            "id": rows[0],
            "title": rows[1],
            "isbn": rows[2],
            "published_year": rows[3],
            "author_id": rows[4]
        }

        return 200, {
            "status": "success",
            "message": book
        }

    except Exception as e:
        print("Unexpected error: ", e)
        return 400, {
            "status": "error",
            "message": "could not create a book"
        }

def delete_book_handler(params):
    id = params.get("id")
    row = queries.delete_book(id)

    if row:
        data = format_books([row])
        return 200, {
            "status": "success",
            "data": data
        }
    return 404, {
            "error": f"book with id: {id} not found",
        }

def put_book_handler(data, params):
    book_id = params.get("id",None)
    title = data.get("title",None)
    isbn = data.get("isbn",None)
    published_year = data.get("published_year",None)
    author_id = data.get("author_id", None)

    if not title or len(title)<1 :
            return 400, {
                "status": "error",
                "message": "title must be atleast 1 character"
            }

    if not isbn or not is_valid_isbn(isbn):
        return 400, {
            "status": "invalid isbn"
        }
    
    if not published_year or not is_valid_year(published_year):
        return 400, {
            "status": "error",
            "message": "invalid published_year"
        }
    
    if not author_id:
        return 400, {
            "status": "error",
            "message": "author_id is required"
        }
    
    if not queries.get_authors(id=author_id):
        return 400, {
            "status": "error",
            "message": "author doesn't exist"
        }
    
    row = queries.put_book(id=book_id, title=title, isbn=isbn, published_year=published_year, author_id=author_id)

    if row:
        updated_data = format_books([row])
        return 200, {
            "status": "success",
            "data": updated_data
        }

    return 400, {
        "status": "error",
        "message": "coundn't update book"
    }




