#!/usr/bin/env python

# utility to manipulate route information for a user
# usage: mroute.py [-i|-d|-a] <cacheserver> <email> <route>

import sys,socket,getopt

def usage ():
    sys.stderr.write ("mroute.py [-i|-d|-a] <cacheserver> <email> [imaproute [pop3route]]\n")
    sys.stderr.write ("\n")
    sys.stderr.write (" -i  show route information for account specified by <email>\n")
    sys.stderr.write (" -a  add the route information specified by imaproute and|or pop3route to the memcached server <cacheserver>\n")
    sys.stderr.write ("     if only one route is specified, it is treated as an imap route\n")
    sys.stderr.write ("     if a second route is specified, it is treated as the pop3 route\n")
    sys.stderr.write (" -d  delete the route information of the account from the cache server (routes are ignored)\n")
    sys.stderr.write ("\n")
    sys.stderr.write (" -v  be verbose about what's going on\n")
    sys.stderr.write (" -h  print this help\n")
    sys.stderr.write ("\n")

def debug (*args):
    if verbose == 0: return
    for a in args: sys.stderr.write (a)

def main (args):
    global verbose

    verbose=0
    try: copts, cargs = getopt.getopt (args, "viadh")
    except getopt.GetoptError, e:
        sys.stderr.write ("%s\n" % e)
        usage ()
        sys.exit (1)

    copts = [ x[0] for x in copts ]

    if ("-h" in copts):
        usage ()
        sys.exit (0)

    if ("-v" in copts):
        verbose=1

    hasi = hasa = hasd = 0

    if ("-i" in copts): hasi = 1
    if ("-a" in copts): hasa = 1
    if ("-d" in copts): hasd = 1

    if (hasi + hasa + hasd) != 1:
        sys.stderr.write ("Please specify exactly one of -i|-a|-d\n")
        sys.exit (1)

    if hasi == 1:
        if len (cargs) != 2:
            sys.stderr.write ("-i requires 2 arguments: <cacheserver> <email>\n")
            sys.exit (1)
    elif hasa == 1:
        if len (cargs) < 3:
            sys.stderr.write ("-a requires at least 3 arguments: <cacheserver> <email> <imaproute> [<pop3route>]\n")
            sys.exit (1)
    elif hasd == 1:
        if len (cargs) != 2:
            sys.stderr.write ("-d requires 2 arguments: <cacheserver> <email>\n")
            sys.exit (1)


    cacheserver = cargs[0]
    account = cargs[1]

    cacheservername, cacheserverport = cacheserver.split (":")

    c = socket.socket (socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    c.connect ((cacheservername, int(cacheserverport)))

    if hasi == 1:
        for proto in ("IMAP", "POP3"):
            sys.stdout.write ("protocol: %s\n" % proto)
            buff = "get %s:%s\r\n" % (proto,account)
            debug (">> ",repr(buff),"\n")
            c.send (buff)
            buff = c.recv (1024)
            debug ("<< ", repr(buff), "\n")
            if buff.startswith ("VALUE "): sys.stdout.write(buff)
            else: print "NOT FOUND"

    elif hasa == 1:
        routes = cargs[2:]
        imaproute = routes[0]
        buff = "add %s:%s 0 0 %d\r\n%s\r\n" % ("IMAP", account, len(imaproute), imaproute)
        debug (">> ",repr(buff),"\n")
        c.send (buff)
        buff = c.recv (1024)
        debug ("<< ", repr(buff), "\n")
        if len(routes) > 1:
            pop3route = routes[1]
            buff = "add %s:%s 0 0 %d\r\n%s\r\n" % ("POP3", account, len(pop3route), pop3route)
            debug (">> ",repr(buff),"\n")
            c.send (buff)
            buff = c.recv (1024)
            debug ("<< ", repr(buff), "\n")
    elif hasd == 1:
        for proto in ("IMAP", "POP3"):
            sys.stdout.write ("deleting route info, protocol: %s\n" % proto)
            buff = "delete %s:%s\r\n" % (proto, account)
            debug (">> ", repr(buff), "\n")
            c.send (buff)
            buff = c.recv (1024)
            debug (buff)

    c.close()

if __name__ == '__main__':
    main (sys.argv[1:])

