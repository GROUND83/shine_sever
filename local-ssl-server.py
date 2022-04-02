import http.server

import ssl

httpd = http.server.HTTPServer(("0.0.0.0", 3004), http.server.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(
    httpd.socket, certfile="server.crt", keyfile="server.key"
)

httpd.serve_forever()
