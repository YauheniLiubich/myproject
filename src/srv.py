import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from  urllib.parse import parse_qs
from datetime import datetime

PORT = int(os.getenv('PORT', 8000))
print(f'{PORT}')
now = datetime.now().year

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello"):
            path, qs = self.path.split("?")
            qs = parse_qs(qs)
            if 'name' not in qs:
                name = 'anonymous'
            else:
                name = qs["name"][0]
            if 'age' not in qs:
                born = ''
            else:
                age = qs['age'][0]
                year = now - int(age)
                born = 'You were born in ' + str(year) + ' year'
            msg = f"""
                Hello {name}!
                {born}
                Your path:  {path}
            """
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())

        else:
            return SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print('it works')
    httpd.serve_forever()

