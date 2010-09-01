#!/usr/bin/python

import optparse
import asynchat
import asyncore
import socket
import json
import cPickle as pickle
import os
import hmac
import logging
import marshal

VERSION = 0.0


logging.basicConfig(level=logging.DEBUG)
DEFAULT_PORT = 11235


class Protocol(asynchat.async_chat):
    def __init__(self, conn=None):
        if conn:
            asynchat.async_chat.__init__(self, conn)
        else:
            asynchat.async_chat.__init__(self)

        self.set_terminator("\n")
        self.buffer = []
        self.auth = None
        self.mid_command = False

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def send_command(self, command, data=None):
        if data:
            pdata = pickle.dumps(data)
            command['data-length'] = len(pdata)
            self.push(json.dumps(command) + "\n" + pdata)
        else:
            logging.debug( "<- %s" % json.dumps(command))
            self.push(json.dumps(command) + "\n")

    def found_terminator(self):
        if not self.mid_command:
            logging.debug("-> %s" % ''.join(self.buffer))
            command = json.loads(''.join(self.buffer))
            if 'data-length' in command:
                self.set_terminator(command['data-length'])
                self.mid_command = command
            else:
                self.process_command(command)
        else: # Read the data segment from the previous command
            data = pickle.loads(''.join(self.bugger))
            self.set_terminator("\n")
            self.mid_command = None
            self.process_command(command, data)
        self.buffer = []

    def send_challenge(self):
        self.auth = os.urandom(20).encode("hex")
        self.send_command({"action": "challenge", "msg": self.auth})

    def respond_to_challenge(self, command):
        mac = hmac.new(self.password, command["msg"])
        self.send_command({"action": "auth", "mac": mac.digest().encode("hex")})
        if not self.auth:
            self.send_challenge()

    def verify_auth(self, command):
        mac = hmac.new(self.password, self.auth)
        if command["mac"] == mac.digest().encode("hex"):
            self.auth = "Done"
            logging.info("Authorized other end")
        else:
            self.handle_close()

    def process_command(self, command, data=None):
        commands = {
            'challenge': self.respond_to_challenge,
            'auth': self.verify_auth
            }

        if command["action"] in commands:
            commands[command["action"]](command)
        

class Client(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        
    def conn(self, server, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((server, port))
        asyncore.loop()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()


class Server(asyncore.dispatcher, object):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.mapfn = None
        self.reducefn = None
        self.collectfn = None
        self.datasource = None
        self.password = None

    def run_server(self, password, port=DEFAULT_PORT):
        self.password = password
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(1)
        asyncore.loop()

    def handle_accept(self):
        conn, addr = self.accept()
        sc = ServerChannel(conn, self)
        sc.password = self.password

    def handle_close(self):
        self.close()

    def set_datasource(self, ds):
        self._datasource = ds
    
    def get_datasource(self):
        return self._datasource

    datasource = property(get_datasource, set_datasource)


class ServerChannel(Protocol):
    def __init__(self, conn, server):
        Protocol.__init__(self, conn)
        self.server = server

        self.start_auth()

    def handle_close(self):
        self.close()

    def start_auth(self):
        self.send_challenge()

    

def run_client():
    parser = optparse.OptionParser(usage="%prog [options]", version="%%prog %s"%VERSION)
    parser.add_option("-p", "--password", dest="password", help="password")
    parser.add_option("-P", "--port", dest="port", type="int", default=DEFAULT_PORT, help="port")

    (options, args) = parser.parse_args()

    client = Client()
    client.password = options.password
    client.conn(args[0], options.port)
                      

if __name__ == '__main__':
    run_client()
