from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8000
HTML_DIR = Path(__file__).parent.joinpath('data/html')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML_DIR, **kwargs)


with HTTPServer(('localhost', PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
