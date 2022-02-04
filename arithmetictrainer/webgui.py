import sys
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from pathlib import Path
from decimal import Decimal, InvalidOperation

from core import Arithmetictrainer
from utils import create_taskgenerators_from_file

PORT = 8000
DATA = Path(__file__).parent.joinpath('data')
HTML_FILE = DATA.joinpath('html/index.html')


taskgen_list = create_taskgenerators_from_file(DATA.joinpath('config'))
trainer = Arithmetictrainer(taskgen_list)

class Handler(BaseHTTPRequestHandler):
    def get_html(self, html_file: Path):
        task = trainer.getTask()
        if not html_file.is_file():
            raise ValueError(f'[{html_file}] is not a file.')
        with open(html_file) as f:
            html = f.read()
        html = html.replace(
                'RESULT_DECIMAL_POINTS', str(task['result_decimal_points']))
        html = html.replace('TASK', task['task'])
        return html.encode()

    def do_GET(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(self.get_html(HTML_FILE))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        print('content length ' + str(content_len))
        data = self.rfile.read(content_len).decode()
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        try:
            # data should have the form 'answer=NUMBER'
            data = data.split('=')[-1]
            trainer.answer(Decimal(data))
        except InvalidOperation:
            print(f'Could not convert "{data}" to Decimal.')


def main():
    with ThreadingHTTPServer(('localhost', PORT), Handler) as httpd:
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt received, exiting.")
            sys.exit(0)

if __name__ == '__main__':
    main()
