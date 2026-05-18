from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from router import Router
from handlers import home,authors,books
import json

router = Router()

router.add("GET","/",home.home_handler)
router.add("GET","/authors",authors.authors_handler)
router.add("GET","/books",books.books_handler)
router.add("GET", "/books/<id>",books.books_handler)
router.add("GET", "/authors/<id>",authors.authors_handler)

router.add("POST","/authors",authors.create_author_handler)
router.add("POST","/books",books.create_book_handler)

router.add("DELETE","/authors/<id>",authors.delete_author_handler)
router.add("DELETE","/books/<id>",books.delete_book_handler)

router.add("PUT","/authors/<id>",authors.put_author_handler)
router.add("PUT","/books/<id>",books.put_book_handler)

class MyHandler(BaseHTTPRequestHandler):

    def response_sender(self,status_code=404,response_data= {"error":"Not found"}):
        self.send_response(status_code)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=4).encode())


    def do_GET(self):
        print("Request received", self.path)

        parsed = urlparse(self.path)
        path = parsed.path
        query_params = parse_qs(parsed.query)

        handler, params = router.resolve("GET",path)

        try:
            if handler:
                status_code, response_data = handler(query_params,params)
            else:
                status_code, response_data = 404, {"error": "Not found"}
        
        except Exception as e:
            print("Error:", e)
            status_code, response_data = 500, {"error": "Internal Server Error"}

        self.response_sender(status_code,response_data)




    def do_POST(self):
        print("Request received ",self.path)
        
        parsed = urlparse(self.path)
        path = parsed.path
            
        content_length = int(self.headers.get('Content-Length',0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            data = {}

        handler = router.resolve("POST",path)[0]

        try:
            if handler:
                status_code, response_data = handler(data)
            else:
                status_code, response_data = 404, {"error":"Not Found"}

        except Exception as e:
            print("Error:", e)
            status_code, response_data = 500, {"error": "Internal Server Error"}

        self.response_sender(status_code,response_data)




    def do_PUT(self):
        print("Request received ",self.path)

        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            data = {}

        handler, params = router.resolve("PUT",path)

        try:
            status_code, response_data = handler(data, params)

        except:
            status_code, response_data = 404, {"error": "Not Found"}

        self.response_sender(status_code,response_data)

        

    def do_DELETE(self):

        print("Request received ",self.path)

        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        handler, params = router.resolve("DELETE",path)

        try:
            if handler:
                status_code, response_data= handler(params)
            else:
                status_code, response_data = 404, {"error": "Not found"}

        except Exception as e:
            print("Error: ", e)
            status_code, response_data = 500, {"error": "Internal server error"}
    
        self.response_sender(status_code, response_data)
        


def run():
    server_address = ("",8000)
    httpd = HTTPServer(server_address,MyHandler)

    print("Server Running on http://localhost:8000")

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("Server stopped \"http://localhost\" no more running!! (Keyboard Interrupt)")

    # finally:
    #     httpd.server_close()
    #     print("Server closed cleanly")


if __name__ == "__main__":
    run()
