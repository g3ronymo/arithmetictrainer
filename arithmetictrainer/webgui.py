"""
GUI for the browser. 

.. note:: important
    
    Should not be publicly hosted.

"""
import sys
import time
import webbrowser
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from decimal import Decimal, InvalidOperation

from core import Arithmetictrainer
from utils import create_taskgenerators_from_file

DATA = Path(__file__).parent.joinpath('data')
INDEX_HTML = DATA.joinpath('html/index.html')
PLAY_HTML = DATA.joinpath('html/play.html')
END_HTML = DATA.joinpath('html/end.html')
CSS = DATA.joinpath('html/style.css')

def get_html(html_file: Path, css_file=None, context={}):
    """
    **html_file** is the path to an html file.
    **css_file** is the path to an html file. If the html contains the 'STYLE'
    keyword it gets replaced by the content of **css_file**.
    **context** should be a dictonary, each key found in the html file
    gets replaced by its value.
    """
    if not html_file.is_file():
        raise ValueError(f'[{html_file}] is not a file.')
    with open(html_file) as f:
        html = f.read()
    with open(html_file) as f:
        html = f.read()
    if css_file != None:
        with open(CSS) as f:
            css = f.read()
        html = html.replace('STYLE', css, 1)
    for key in context:
        html = html.replace(key, str(context[key]))
    return html.encode()

class BaseHandler(BaseHTTPRequestHandler):
    """
    Let **do_Get** and **do_POST** both call a **main** method.
    The default **main** method does nothing and should be overriden
    in a subclass.
 
    If it is necessary to know which http method was used we can still
    use **self.command** from BaseHTTPRequestHandler.
    """
    config = DATA.joinpath('config')
    num_tasks = 10

    def do_GET(self):
        self.main()

    def do_POST(self):
        self.main()

    def main(self):
        """
        Called on each POST and GET request.
        """
        pass

class Handler(BaseHandler):

    def main(self):
        """
        Called on each POST and GET request.
        Dispatch each request to the appropriat handler method.
        """
        address = self.requestline.split()[1]
        if address in ('/' ,'/?'):
            self.handle_index()
        elif address in ('/start', '/start?'):
            self.handle_start_get()
        elif address in ('/play', '/play?'):
            self.handle_play_get()
        elif address in ('/answer', '/answer?'):
            self.handle_answer_post()
        elif address in ('/end', '/end?'):
            self.handle_end()

    def handle_index(self):
        """
        Handle /.
        """
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        html = get_html(INDEX_HTML, css_file=CSS)
        self.wfile.write(html)

    def handle_start_get(self):
        """
        Start the run.
        Configures Arithmetictrainer and redirects to /play.
        """
        self.send_response(302)
        self.send_header('Location', '/play')
        self.end_headers()
        Handler.start_time = time.time()
        taskgen_list = create_taskgenerators_from_file(Handler.config)
        Handler.trainer = Arithmetictrainer(taskgen_list)
        Handler.trainer.start()

    def handle_play_get(self):
        """
        Display the current task.
        """
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        task = Handler.trainer.getTask()
        context = {
                'RESULT_DECIMAL_POINTS': str(task['result_decimal_points']),
                'TASK': task['task'],
                'SOLVED': Handler.trainer.num_correct_answers,
        }
        html = get_html(PLAY_HTML, css_file=CSS, context=context)
        self.wfile.write(html)


    def handle_answer_post(self):
        """
        Try to answer the current task.
        """
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len).decode()
        try:
            data = data.split('=')[-1]
            Handler.trainer.answer(Decimal(data))
        except InvalidOperation:
            print(f'Could not convert "{data}" to Decimal.')
        self.send_response(302)
        if Handler.trainer.solvedTasks() == Handler.num_tasks:
            self.send_header('Location', '/end')
        else:
            self.send_header('Location', '/play')
        self.end_headers()

    def handle_end(self):
        """
        Handle **/end**.
        """
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        stats = Handler.trainer.getStats()
        context = {
                'SOLVED': stats['num_correct_answers'],
                'WRONG_ANSWERS': stats['num_incorrect_answers'],
                'TIME': stats['time_since_start']
        }
        html = get_html(END_HTML, css_file=CSS, context=context)
        self.wfile.write(html)


def main(port=8000, config=None, num_tasks=10):
    if config != None:
        Handler.config = config
    Handler.num_tasks = num_tasks
    with ThreadingHTTPServer(('localhost', port), Handler) as httpd:
        webbrowser.open_new_tab('localhost' + ':' + str(port))
        print("serving at port", port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt received, exiting.")
            sys.exit(0)

if __name__ == '__main__':
    main()
