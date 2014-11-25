import socketserver
import time
import sys
import threading
import glob
import re

import server.exploder as exploder
import server.config as config

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class SMTPHandler(socketserver.StreamRequestHandler):
    
    def send(self, what):
        self.request.sendall(bytes(what, 'utf-8'))
        
    def handle(self):
        
        
        cip = format(self.client_address[0])
        cport = int(format(self.client_address[1]))
        print ("Request from %s:%u" % (cip,cport) )
        
        line = self.rfile.readline().strip()
        listname = "dev@httpd.apache.org"
        recip = None
        match = re.match(r"GET /([^?]+)\??(.*) HTTP", str(line, 'utf-8'))
        if match:
            listname = match.group(1)
            recip = match.group(2)
        print("Got req for: %s" % listname)
        self.send("Checking whether %s is valid: " % listname)
        listdir = exploder.list_exists(listname)
        if listdir:
            self.send(listdir)
            self.send("\n")
            if recip:
                exploder.remove_recipient(listdir, recip)
                
            recips = exploder.get_recipients(listdir)
            if len(recips) > 0:
                self.send("Recipients are: ")
                self.send(", ".join(recips))
        else:
            self.send("No such list exists")


def start():
    bindHost = config.cconfig.get('SMTP', 'bindTo')
    bindPort = int(config.cconfig.get('SMTP', 'incomingPort'))
    

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((bindHost, bindPort), SMTPHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    