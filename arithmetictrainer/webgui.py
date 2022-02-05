import sys
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from pathlib import Path
from decimal import Decimal, InvalidOperation

from core import Arithmetictrainer
from utils import create_taskgenerators_from_file


class BaseHandler(BaseHTTPRequestHandler):
    """
    Let **do_Get** and **do_POST** both call a **main** method.
    The default **main** method does nothing and should be overriden
    in a subclass.
    
    If it is necessary to know which http method was used we can still
    use **self.command** from BaseHTTPRequestHandler.
    """
    DATA = Path(__file__).parent.joinpath('data')
    INDEX_HTML = DATA.joinpath('html/index.html')
    PLAY_HTML = DATA.joinpath('html/play.html')
    CSS = DATA.joinpath('html/style.css')


    taskgen_list = create_taskgenerators_from_file(DATA.joinpath('config'))
    trainer = Arithmetictrainer(taskgen_list)

    def do_GET(self):
        self.main()

    def do_POST(self):
        self.main()

    def main(self):
        pass

class Handler(BaseHandler):
    def get_html(self, html_file: Path, context={}):
        """
        **html_file** is the path to an html file. 
        **context** should be a dictonary, each key found in the html file
        gets replaced by its value.
        """
        if not html_file.is_file():
            raise ValueError(f'[{html_file}] is not a file.')
        with open(html_file) as f:
            html = f.read()
        with open(html_file) as f:
            html = f.read()
        with open(self.CSS) as f:
            css = f.read()
        html = html.replace('STYLE', css, 1)
        for key in context:
            html = html.replace(key, context[key])
        return html.encode()

    def main(self):
        address = self.requestline.split()[1]
        if address == '/':
            self.handle_index()
        elif address == '/start?':
            self.handle_start_get()
        elif address == '/play':
            self.handle_play_get()
        elif address == '/answer':
            self.handle_answer_post()

    def handle_index(self):
        """
        Handle /.
        """
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        html = self.get_html(self.INDEX_HTML)
        self.wfile.write(html)

    def handle_start_get(self):
        """
        Start the run.
        Configures Arithmetictrainer and redirects to /play.
        """
        self.send_response(302)
        self.send_header('Location', '/play')
        self.end_headers()

    def handle_play_get(self):
        """
        Display the current task.
        """
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        task = self.trainer.getTask()
        context = {
                'RESULT_DECIMAL_POINTS': str(task['result_decimal_points']),
                'TASK': task['task'],
        }
        html = self.get_html(self.PLAY_HTML, context=context)
        self.wfile.write(html)


    def handle_answer_post(self):
        """
        Try to answer the current task.
        """
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len).decode()
        self.send_response(302)
        self.send_header('Location', '/play')
        self.end_headers()
        try:
            # data should have the form 'answer=NUMBER'
            data = data.split('=')[-1]
            self.trainer.answer(Decimal(data))
        except InvalidOperation:
            print(f'Could not convert "{data}" to Decimal.')


def main(port=8000):
    with ThreadingHTTPServer(('localhost', port), Handler) as httpd:
        print("serving at port", port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt received, exiting.")
            sys.exit(0)

if __name__ == '__main__':
    main(8000)
