import BaseHTTPServer
import sys
import time

class nginxRespHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self, *posargs, **kwargs):
        global upstream_host, upstream_port
        self.send_response (200)
        self.log_message ("%s" % self.headers)
        self.send_header ("Auth-Status", "OK")
        self.send_header ("Auth-Server", "%s" % upstream_host)
        self.send_header ("Auth-Port", "%s" % upstream_port)
        # self.send_header ("Auth-User", "")
        self.end_headers ()
        self.wfile.write ("")
        self.wfile.close ()

def test (port):
    httpd = BaseHTTPServer.HTTPServer (('', port), nginxRespHandler)
    httpd.serve_forever ()

def help ():
    print """
Usage: routing-lookup-handler [port] [upstream-ip] [upstream-port]

 port           The port number to listen on [default 9000]
 upstream-ip    The IP address of the upstream zimbra server [default 127.0.0.1]
 upstream-port  The port of the upstream zimbra server [default 143]
    """

if __name__ == "__main__":
    global upstream_host, upstream_port

    if "-h" in sys.argv or \
       "--help" in sys.argv or \
       "-u" in sys.argv or \
       "--usage" in sys.argv:
       help()
       sys.exit (1)


    try: port = int(sys.argv[1])
    except IndexError: port = 9000

    try: upstream_host = sys.argv[2]
    except IndexError: upstream_host = "127.0.0.1"

    try: upstream_port = int (sys.argv[3])
    except IndexError: upstream_port = 143

    print "Starting nginx routing lookup handler on port %d (upstream information will be %s:%d for every request) ..." % \
            (port, upstream_host, upstream_port)
    test (port)

