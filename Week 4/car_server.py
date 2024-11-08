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

cars = ["Lexus","Ford"]

reservations = DataFrame(columns=["car", "startDate", "endDate"])

def ping():
    return True

# get methods
def GetCars():
    return cars

# reserve methods
def ReserveCar(car, startDate, endDate):
    if car in cars:
        global reservations
        reservation = {
                "car":car,
                "startDate":startDate,
                "endDate":endDate}
        reservations = reservations.append(reservation, ignore_index=True)
        return reservation
    else:
        return False

def GetCarReservations():
    global reservations
    return reservations.to_string()

def DeleteCarReservation(car, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.car == car) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

def DeleteAllReservations():
    global reservations
    reservations = DataFrame(columns=["car", "startDate", "endDate"])
    return True

# server stuff
ip = getIp()
print("I am the car server and I am serving at: http://{0}:8800".format(ip))

server = SimpleXMLRPCServer((ip, 8800), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

server.register_function(ping, "ping")
server.register_function(GetCars, "GetCars")
server.register_function(ReserveCar, "ReserveCar")
server.register_function(GetCarReservations, "GetCarReservations")
server.register_function(DeleteCarReservation, "DeleteCarReservation")
server.register_function(DeleteAllReservations, "DeleteAllReservations")

server.serve_forever()
