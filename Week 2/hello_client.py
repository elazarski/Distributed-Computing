#!/usr/bin/python3

# import xmlrpc
import xmlrpc.client

s = xmlrpc.client.ServerProxy("http://localhost:8800")
print(s.Greeting('World'))
print(s.Greeting('John'))
