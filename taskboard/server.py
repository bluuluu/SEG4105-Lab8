"""HTTP entry point for the group task board."""
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from .storage import TaskStore
from .service import TaskService
from .views import page

def make_handler(store):
    service = TaskService(store)
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, text, content_type='text/html; charset=utf-8'):
            payload = text.encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        def do_GET(self):
            if self.path == '/':return self.respond(200, page(store.list()))
            if self.path == '/health':return self.respond(200, json.dumps({'status':'ok','application':'group-task-board'}), 'application/json')
            if self.path == '/api/tasks':return self.respond(200, json.dumps(store.list()), 'application/json')
            self.respond(404, 'Not found', 'text/plain')
        def do_POST(self):
            try:length = int(self.headers.get('Content-Length', '0'))
            except ValueError:return self.respond(400, 'Invalid Content-Length', 'text/plain')
            if not 0 <= length <= 4096:return self.respond(413, 'Request too large', 'text/plain')
            form = parse_qs(self.rfile.read(length).decode('utf-8', errors='replace'))
            try:
                if self.path == '/tasks':service.create(form.get('title',[''])[0], form.get('assignee',[''])[0])
                elif match := re.fullmatch(r'/tasks/(\d+)/complete', self.path):service.complete(int(match[1]))
                else:return self.respond(404, 'Not found', 'text/plain')
            except ValueError as error:return self.respond(400, str(error), 'text/plain')
            except LookupError as error:return self.respond(404, str(error), 'text/plain')
            self.send_response(303)
            self.send_header('Location', '/')
            self.send_header('Content-Length', '0')
            self.end_headers()
    return Handler

def main():
    store = TaskStore(os.environ.get('TASKBOARD_DB', 'data/tasks.db'))
    server = ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT','8080'))), make_handler(store))
    print('Group Task Board listening on port',server.server_port,flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__ == '__main__':main()
