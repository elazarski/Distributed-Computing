#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pandas import DataFrame
import socket

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

airlines = ["United", "Private Jet"]

reservations = DataFrame(columns=["airline", "startDate", "endDate"])

def ping():
    return True

# get methods
def GetAirlines():
    return airlines

# reserve methods
def ReserveAirline(airline, startDate, endDate):
    if airline in airlines:
        global reservations
        reservation = {
                "airline":airline,
                "startDate":startDate,
                "endDate":endDate}
        reservations = reservations.append(reservation, ignore_index=True)
        return reservation
    else:
        return False

def GetAirlineReservations():
    global reservations
    return reservations.to_string()

def DeleteAirlineReservation(airline, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.airline == airline) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

def DeleteAllReservations():
    global reservations
    reservations = DataFrame(columns=["airline", "startDate", "endDate"])
    return True

# server stuff
ip = getIp()
print("I am the airline server and I am serving at http://{0}:8800".format(ip))

server = SimpleXMLRPCServer((ip, 8800), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

server.register_function(ping, "ping")
server.register_function(GetAirlines, "GetAirlines")
server.register_function(ReserveAirline, "ReserveAirline")
server.register_function(GetAirlineReservations, "GetAirlineReservations")
server.register_function(DeleteAirlineReservation, "DeleteAirlineReservation")
server.register_function(DeleteAllReservations, "DeleteAllReservations")

server.serve_forever()
