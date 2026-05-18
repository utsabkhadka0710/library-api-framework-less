import db.queries as queries
import re

def is_valid_email(email):
    return (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$",email))



def format_authors(author_row):

    return [
        {
            "id": r[0],
            "name": r[1]
        } for r in author_row
    ]


def authors_handler(query, params=None):

    if params:
        id = params.get("id")
        row = queries.get_authors(id=id)

        if row:
            data = format_authors([row])
            return 200, {
                "status": "success",
                "data": data
            }
        return 404, {
            "error": "Not found",
        }


    name = query.get("name",[None])[0]
    sort = query.get("sort",[None])[0]
    order = query.get("order",["desc"])[0]

    rows = queries.get_authors(name,sort,order)
    data = format_authors(rows)
    return 200, {
        "status":"success",
        "data":data
        }

def create_author_handler(data):
    name = data.get("name")
    email = data.get("email")

    if not name or len(name)<2:
        return 400, {
            "status":"error",
            "message": "name must be atleast 2 characters"
        }
    
    if not email or not is_valid_email(email):     
        return 400,{
            "status": "error",
            "message": "enter a valid Email"
        }


    try:
        row = queries.create_author(name,email)

        author = {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }

        return 201, {
            "status": "success",
            "data": author
            }
    
    except Exception as e:
        print("Unexpected Error:", e)
        return 400, {
            "status": "error",
            "message": "Email already exists"
        }

def delete_author_handler(params):
    id = params.get("id")
    author_row, books_rows = queries.delete_author(id)

    if not author_row:
        return 404, {
            "error": f"author with id:{id} not found"
        }
    
    author_data = format_authors([author_row])


    deleted_book_data = [
        {
            "id": r[0],
            "title": r[1],
            "isbn": r[2],
            "published_year": r[3]
        } for r in books_rows
    ]

    data = [
        {"deleted_author":author_data},
        {"deleted_books_by_author": deleted_book_data}
         ]
    
    return 200, {
        "status": "success",
        "data": data
    }


def put_author_handler(data, params):
    id = params.get("id", None)
    name = data.get("name", None)
    email = data.get("email", None)

    if not queries.get_authors(id=id):
        return 404, {
            "status": "error",
            "message": "Not Found"
        }
    
    if not name or len(name)<2:
        return 400, {
            "status":"error",
            "message": "name must be atleast 2 characters"
        }
    
    if not email or not is_valid_email(email):     
        return 400,{
            "status": "error",
            "message": "enter a valid Email"
        }
    
    try:
        row = queries.put_author(id, name, email)

    except Exception:
        pass