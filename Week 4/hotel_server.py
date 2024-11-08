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

hotels = ["Motel 6", "Air BNB"]

reservations = DataFrame(columns=["hotel", "startDate", "endDate"])

def ping():
    return True

# get methods
def GetHotels():
    return hotels

# reserve methods
def ReserveHotel(hotel, startDate, endDate):
    if hotel in hotels:
        global reservations
        reservation = {
                "hotel":hotel, 
                "startDate":startDate, 
                "endDate":endDate}
        reservations = reservations.append(reservation, ignore_index=True) 
        return reservation
    else:
        return False

def GetHotelReservations():
    global reservations
    return reservations.to_string()

def DeleteHotelReservation(hotel, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.hotel == hotel) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

def DeleteAllReservations():
    global reservations
    reservations = DataFrame(columns=["hotel", "startDate", "endDate"])
    return True

# server stuff
ip = getIp()
print("I am the hotel server running at: http://{0}:8800".format(ip))

server = SimpleXMLRPCServer((ip, 8800), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

server.register_function(ping, "ping")
server.register_function(GetHotels, "GetHotels")
server.register_function(ReserveHotel, "ReserveHotel")
server.register_function(GetHotelReservations, "GetHotelReservations")
server.register_function(DeleteHotelReservation, "DeleteHotelReservation")
server.register_function(DeleteAllReservations, "DeleteAllReservations")

server.serve_forever()
