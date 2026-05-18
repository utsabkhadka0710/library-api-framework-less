from .connection import get_connection


def get_authors(name=None, sort=None, order="desc",id=None):
    conn = get_connection()
    cur = conn.cursor()

    base_query = "SELECT id, name FROM authors"

    if id:
        base_query += " WHERE id = %s"

        cur.execute(base_query, (id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row
    
    params= []

    if name:
        base_query += " WHERE name ILIKE %s "
        params.append(f"%{name}%")

    #SORTING (safe)
    allowed_sort_fields = {
        "name": "name",
        "created_at": "created_at",
        "id": "id"
    }

    sort_field = allowed_sort_fields.get(sort,"id")

    order = order.lower()
    if not order in ["asc","desc"]:
        order = "desc"

    base_query += f" ORDER BY {sort_field} {order}"

    cur.execute(base_query,params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows



def create_author(name, email):
    conn = get_connection()

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO authors(name, email) VALUES (%s, %s) RETURNING id, name, email;",
            (name, email)
            )
        
        new_author = cur.fetchone()

        conn.commit()
    
    except:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

    return new_author



def put_author(id, email):
    conn = get_connection()
    cur = conn.cursor()

    if not get_authors(id=id):
        return None
    
    query = """
    """


def delete_author(id=None):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id,name FROM authors WHERE id = %s",(id,))
        author_row = cur.fetchone()

        if author_row:
            select_books_query = """
                            SELECT
                                id as book_id,
                                title,
                                isbn,
                                published_year
                            FROM books
                            WHERE author_id = %s
                            """
            cur.execute(select_books_query,(id,))
            books_rows = cur.fetchall()

            query = "DELETE FROM authors WHERE id = %s"
            cur.execute(query,(id,))
            conn.commit()

        cur.close()
        conn.close()

        return author_row,books_rows if author_row else ()

        
    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()




def get_books(title=None, author=None, year=None, sort=None, order="desc",id=None):
    conn = get_connection()
    cur = conn.cursor()

    base_query = """
            SELECT
                books.id,
                books.title,
                books.isbn,
                books.published_year,
                books.author_id,
                authors.name
            FROM books
            JOIN authors ON books.author_id=authors.id
    """

    if id:
        base_query = base_query + " WHERE books.id = %s"
        cur.execute(base_query, (id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row


    conditions = []
    params = []

    if title:
        conditions.append("books.title ILIKE %s")
        params.append(f"%{title}%")

    if author:
        conditions.append("authors.name ILIKE %s")
        params.append(f"%{author}%")

    if year:
        conditions.append("books.published_year = %s")
        params.append(year)


    if conditions:
        base_query += " WHERE " + " AND " .join(conditions)


    allowed_sorted_fields = {
        "title": "books.title",
        "published_year": "books.published_year",
        "created_year": "books.created_at"
    }

    sort_field = allowed_sorted_fields.get(sort,"books.id")

    order = order.lower()
    if order not in ["asc","desc"]:
        order = "desc"

    base_query += f" ORDER BY {sort_field} {order}"
    

    cur.execute(base_query,params)
    
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows



def create_book(title, isbn, published_year, author_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO books (title, isbn, published_year, author_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, isbn, published_year, author_id""",
            (title, isbn, published_year, author_id)
        )

        new_book = cur.fetchone()
        print(new_book)
    
        conn.commit()

    except:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
        
    return new_book


def put_book(id, title, isbn, published_year, author_id ):
    
    conn = get_connection()
    cur = conn.cursor()

    if not get_authors(id=author_id):
        return None
    
    params = (title, isbn, published_year, author_id, id)

    query = """WITH updated_book AS (
                    UPDATE books
                    SET(title, isbn, published_year, author_id) = (%s, %s, %s, %s)
                    WHERE id = %s
                    RETURNING id, title, isbn, published_year, author_id
                )
                SELECT
                    ub.id, ub.title, ub.isbn, ub.published_year, authors.id, authors.name
                    FROM updated_book as ub
                    JOIN authors ON ub.author_id = authors.id
                """
    
    try: 
        cur.execute(query,params)
        conn.commit()

        row = cur.fetchone()

        print(row)

        cur.close()
        conn.close()

        return row

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()



def delete_book(id=None):
    conn = get_connection()
    cur = conn.cursor()

    try:

        select_query = """
                        SELECT
                            books.id,
                            books.title,
                            books.isbn,
                            books.published_year,
                            books.author_id,
                            authors.name
                        FROM books
                        JOIN authors ON books.author_id = authors.id
                        where books.id = %s
                        """
        cur.execute(select_query,(id,))
        row = cur.fetchone()

        if row:
            query = "DELETE FROM books WHERE id = %s "
            cur.execute(query,(id,))
            conn.commit()

        cur.close()
        conn.close()

        return row

        
    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
