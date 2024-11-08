#!/usr/bin/python3

# import xmlrpc
import xmlrpc.client

ip = input("Enter server IP: ")
port = input("Enter port: ")

print("Connecting to http://{0}:{1}".format(ip, port))

s = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))
print(s.Greeting('World'))
print(s.Greeting('John'))
