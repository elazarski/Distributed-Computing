#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

server = SimpleXMLRPCServer(("192.168.50.68", 8800), requestHandler=RequestHandler)
server.register_introspection_functions()

def Greeting(data):
    return "Hello ", data

server.register_function(Greeting, "Greeting")

server.serve_forever()
