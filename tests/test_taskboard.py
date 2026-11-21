import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from http.server import ThreadingHTTPServer
from taskboard.storage import TaskStore
from taskboard.service import TaskService
from taskboard.server import make_handler
from taskboard.views import page

class TaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = TaskStore(Path(self.tmp.name)/'tasks.db')
        self.service = TaskService(self.store)
    def tearDown(self):self.tmp.cleanup()
    def test_persistence_and_completion(self):
        task_id = self.service.create('  Write docs  ', 'Luu, Bryan')
        self.assertEqual(TaskStore(self.store.path).list()[0]['title'],'Write docs')
        self.service.complete(task_id)
        self.assertEqual(self.store.list()[0]['done'],1)
    def test_invalid_input(self):
        for title,person in [('', 'Luu, Bryan'),('x'*121,'Luu, Bryan'),('Task','Unknown')]:
            with self.subTest(title=title):
                with self.assertRaises(ValueError):self.service.create(title,person)
    def test_missing_task(self):
        with self.assertRaises(LookupError):self.service.complete(99)
    def test_html_escaping(self):
        self.service.create('<script>alert(1)</script>','Ali, Almis')
        html = page(self.store.list())
        self.assertIn('&lt;script&gt;',html)
        self.assertNotIn('<script>alert(1)</script>',html)
    def test_http_workflow(self):
        server = ThreadingHTTPServer(('127.0.0.1',0),make_handler(self.store))
        thread = threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        try:
            with urlopen(base+'/health') as r:self.assertEqual(json.load(r)['status'],'ok')
            with urlopen(Request(base+'/tasks',data=urlencode({'title':'Review PR','assignee':'Du, Jack'}).encode())) as r:self.assertIn('Review PR',r.read().decode())
            with urlopen(base+'/api/tasks') as r:task_id=json.load(r)[0]['id']
            with urlopen(Request(base+f'/tasks/{task_id}/complete',data=b'')) as r:self.assertIn('Completed',r.read().decode())
            with self.assertRaises(HTTPError) as error:urlopen(Request(base+'/tasks',data=b'title=&assignee=Unknown'))
            self.assertEqual(error.exception.code,400)
            with self.assertRaises(HTTPError) as error:urlopen(base+'/missing')
            self.assertEqual(error.exception.code,404)
        finally:server.shutdown();server.server_close();thread.join()

if __name__ == '__main__':unittest.main()
