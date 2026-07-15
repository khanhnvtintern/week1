import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "Not Found"})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Server running at http://{HOST}:{PORT}/api/health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
