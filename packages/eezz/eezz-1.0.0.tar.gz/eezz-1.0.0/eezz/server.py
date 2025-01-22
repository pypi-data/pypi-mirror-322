# -*- coding: utf-8 -*-
"""
This module implements the following classes

    * :py:class:`eezz.server.TWebServer` : Implementation of http.server.HTTPServer, prepares the WEB-Socket interface.
    * :py:class:`eezz.server.THttpHandle`: Implementation of http.server.SimpleHTTPRequestHandler, allows special \
    access on local services.
 
"""
import  os
import  re
import  importlib.resources
import  shutil
from    pathlib         import Path

import  http.server
import  http.cookies
from    threading       import Thread
from    urllib.parse    import urlparse
from    urllib.parse    import parse_qs
from    optparse        import OptionParser
from    eezz.websocket  import TWebSocket
from    eezz.http_agent import THttpAgent
from    eezz.service    import TService
import  time
from    loguru          import logger
import  json


class TWebServer(http.server.HTTPServer):
    """ WEB Server encapsulate the WEB socket implementation

    :param Tuple[str,socket] a_server_address: The WEB address of this server
    :param a_http_handler:   The HTTP handler
    :param a_web_socket:     The socket address waiting for WEB-Socket interface
    """
    def __init__(self, a_server_address, a_http_handler, a_web_socket):
        self.m_socket_inx  = 0
        self.m_server_addr = a_server_address
        self.m_web_addr    = (a_server_address[0], int(a_web_socket))
        self.m_web_socket  = TWebSocket(self.m_web_addr, THttpAgent)
        self.m_web_socket.start()
        super().__init__(a_server_address, a_http_handler)

    def shutdown(self):
        """ Shutdown the WEB server """
        self.m_web_socket.shutdown()
        super().shutdown()


class THttpHandler(http.server.SimpleHTTPRequestHandler):
    """ HTTP handler for incoming requests """
    def __init__(self, request, client_address, server):
        self.m_client       = client_address
        self.m_server       = server
        self.m_request      = request
        self.server_version = 'eezzyServer/2.0'
        self.m_http_agent   = THttpAgent()
        super().__init__(request, client_address, server)
    
    def do_GET(self):
        """ handle GET request """
        self.handle_request()
        pass

    def do_POST(self):
        """ handle POST request """
        self.handle_request()

    def shutdown(self, args: int = 0):
        """ Shutdown handler """
        self.m_server.shutdown()

    def handle_request(self):
        """ handle GET and POST requests """
        x_cookie    = http.cookies.SimpleCookie()
        if 'eezzAgent' not in x_cookie:
            x_cookie['eezzAgent'] = 'AgentName'

        x_morsal     = x_cookie['eezzAgent']
        x_result     = urlparse(self.path)
        x_query      = parse_qs(x_result.query)
        x_query_path = x_result.path
        x_resource   = TService().public_path / f'.{x_query_path}'

        if self.m_client[0] in ('localhost', '127.0.0.1'):
            # Administration commands possible only on local machine
            if x_query_path == '/system/shutdown':
                Thread(target=shutdown_function, args=[self]).start()
                return
            if x_query_path == '/system/eezzyfree':
                # Polling request for an existing connection
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(x_result).encode('utf-8'))
                return
            if x_query_path == '/eezzyfree':
                # Assign a user to the administration page
                pass

        if x_resource.is_dir():
            x_resource = TService().root_path / 'index.html'

        if not x_resource.exists():
            self.send_response(404)
            self.end_headers()
            logger.info(f'Cannot load resource {x_resource}')
            return

        if x_resource.suffix in '.html':
            x_result = self.m_http_agent.do_get(x_resource, x_query)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(x_result.encode('utf-8'))
        elif x_resource.suffix in ('.txt', '.bak'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with x_resource.open('rb') as f:
                self.wfile.write(f.read())
        elif x_resource.suffix in ('.png', '.jpg', '.gif', '.mp4', '.ico'):
            self.send_response(200)
            self.send_header('content-type', 'image/{}'.format(x_resource.suffix)[1:])
            self.end_headers()
            with x_resource.open('rb') as f:
                self.wfile.write(f.read())
        elif x_resource.suffix in '.css':
            self.send_response(200)
            self.send_header('content-type', 'text/css')
            self.end_headers()
            with x_resource.open('rb') as f:
                self.wfile.write(f.read())
        elif x_resource.suffix in '.js':
            self.send_response(200)
            self.send_header('content-type', 'text/javascript')
            self.end_headers()
            with x_resource.open('rb') as f:
                self.wfile.write(f.read())
        else:
            logger.error(f'Extension not registered: {x_resource}')


def shutdown_function(handler: THttpHandler):
    handler.shutdown(0)
    time.sleep(2)


if __name__ == "__main__":
    print(""" 
        EezzServer  Copyright (C) 2025  Albert Zedlitz
        This program comes with ABSOLUTELY NO WARRANTY
        This is free software, and you are welcome to redistribute it
        under certain conditions
    """)

    # Parse command line options
    x_opt_parser = OptionParser()
    x_opt_parser.add_option("-d", "--host",      dest="http_host",  default="localhost", help="HTTP Hostname (for example localhost)")
    x_opt_parser.add_option("-p", "--port",      dest="http_port",  default="8000",      help="HTTP Port (default 8000")
    x_opt_parser.add_option("-w", "--webroot",   dest="web_root",   default="eezz/webroot",   help="Web-Root (path to webroot directory)")
    x_opt_parser.add_option("-x", "--websocket", dest="web_socket", default="8100",      help="Web-Socket Port (default 8100)",  type="int")
    x_opt_parser.add_option("-t", "--translate", dest="translate",  action="store_true", help="Optional creation of POT file")

    (x_options, x_args) = x_opt_parser.parse_args()

    dest_dir = Path(x_options.web_root)
    if not dest_dir.exists() and x_options.web_root == 'eezz/webroot':
        logger.warning(f'Continue with bootstrap: creating ./eezz/webroot')
        src_dir = importlib.resources.files('eezz') / 'webroot'
        dest_dir = Path('eezz/webroot')
        shutil.copytree(str(src_dir), dest_dir)

    TService.set_environment(x_options.web_root,  x_options.http_host, x_options.web_socket)

    if TService().public_path.is_dir():
        os.chdir(TService().public_path)
    else:
        x_opt_parser.print_help()
        logger.critical(f'webroot not found. Specify path using option "--webroot <path>"')
        exit(0)

    x_httpd   = TWebServer((x_options.http_host, int(x_options.http_port)), THttpHandler, x_options.web_socket)
    logger.info(f"Starting HTTP Server on {x_options.http_host} at Port {x_options.http_port} ...")

    x_path = Path(TService().resource_path / 'websocket.js')
    if x_path.exists():
        with x_path.open('r') as f:
            x_ws_descr = f.read()
        x_ws_connect = """ws://{host}:{port}""".format(host=x_options.http_host, port=x_options.web_socket)
        x_ws_descr = re.sub(r"""(g_eezz_socket_addr\s*=\s*)("\S+")""", fr"""\1 "{x_ws_connect}" """, x_ws_descr)
        with x_path.open('w') as f:
            f.write(x_ws_descr)

    x_httpd.serve_forever()
    logger.info('shutdown')
    exit(os.EX_OK)
