#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pandas import DataFrame
from pandas import Series
import socket
import pymongo
from pymongo import MongoClient

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

def addReservation(reservation):
    reservations.insert_many(reservation.to_dict('records'))

# connect to database
dbUsername = "root"
dbPassword = "BVs4xuuxW0X9"
dbIp = input("Enter MongoDB IP: ")
#dbPort = input("Enter MongoDB port: ")
connectionUri = "mongodb://{0}:{1}@{2}:{3}".format(dbUsername, dbPassword, dbIp, "27017")
client = MongoClient(connectionUri)
db = client.reservation_system

hotels = db.hotels
airlines = db.airlines
cars = db.cars

reservations = db.reservations

# get methods
def GetHotels():
    global hotels
    cursor = hotels.find()
    retVar = DataFrame(list(cursor))
    retVar = list(retVar.name)
    return retVar

def GetAirlines():
    global airlines
    cursor = airlines.find()
    retVar = DataFrame(list(cursor))
    retVar = list(retVar.name)
    return retVar

def GetCars():
    cursor = cars.find()
    retVar = DataFrame(list(cursor))
    retVar = list(retVar.name)
    return retVar

# reserve methods
def ReserveHotel(hotel, startDate, endDate):
    localHotels = GetHotels()
    if hotel in localHotels:
        global reservations
        reservation = {
                "type":"hotel", 
                "detail":hotel, 
                "startDate":startDate, 
                "endDate":endDate}
        reservations.insert_one(reservation)
        return "hotel reserved"
    else:
        return False

def ReserveAirline(airline, startDate, endDate):
    if airline in airlines:
        global reservations
        reservation = { 
                "type":"airline",
                "etail":airline,
                "startDate":startDate,
                "endDate":endDate}
        reservations.insert_one(reservation)
        return "airline reserved"
    else:
        return False

def ReserveCar(car, startDate, endDate):
    if car in cars:
        global reservations
        reservation = {
                "type":"car",
                "detail":car,
                "startDate":startDate,
                "endDate":endDate}
        reservations.insert_one(reservation)
        return "car reserved"
    else:
        return False

def GetAllReservations(): 
    global reservations
    cursor = reservations.find()
    retVar = list(cursor)
    return retVar

def GetHotelReservations():
    global reservations
    hotelReservations = DataFrame(list(reservations.find({'type' : "hotel"})))
    if hotelReservations.empty:
        return ""
    hotelReservations = hotelReservations.drop("_id", axis=1)
    hotelReservations = hotelReservations.drop("type", axis=1)
    hotelReservations = hotelReservations.rename(columns={"detail":"hotel"})
    return hotelReservations.to_string()

def GetAirlineReservations():
    global reservations
    airlineReservations = DataFrame(list(reservations.find({'type' : 'airline'})))
    if airlineReservations.empty:
        return ""
    airlineReservations = airlineReservations.drop("_id", axis=1)
    airlineReservations = airlineReservations.drop("type", axis=1)
    airlineReservations = airlineReservations.rename(columns={"detail":"airline"})
    return airlineReservations.to_string()

def GetCarReservations():
    global reseravtions
    carReservations = DataFrame(list(reservations.find({'type':"car"})))
    if carReservations.empty:
        return ""
    carReservations = carReservations.drop("_id", axis=1)
    carReservations = carReservations.drop("type", axis=1)
    carReservations = carReservations.rename(columns={"detail":"car"})
    return carReservations.to_string()

def DeleteHotelReservation(hotel, startDate, endDate):
    global reservations
    drop = {
            "type" : "hotel",
            "detail" : hotel,
            "startDate" : startDate,
            "endDate" : endDate}
    reservations.delete_one(drop)
    return True

def DeleteAirlineReservation(airline, startDate, endDate):
    global reservations
    drop = {
            "type" : "airline",
            "detail" : airline,
            "startDate" : startDate,
            "endDate" : endDate}
    reservations.delete_one(drop)
    return True

def DeleteCarReservation(car, startDate, endDate):
    global reservations
    drop = {
            "type" : "car",
            "detail" : car,
            "startDate" : startDate,
            "endDate" : endDate}
    reservations.delete_one(drop)
    return True

# server stuff
ip = getIp()
print("My IP: {0}".format(ip))
server = SimpleXMLRPCServer((ip, 8800), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

server.register_function(GetHotels, "GetHotels")
server.register_function(GetAirlines, "GetAirlines")
server.register_function(GetCars, "GetCars")

server.register_function(ReserveHotel, "ReserveHotel")
server.register_function(ReserveAirline, "ReserveAirline")
server.register_function(ReserveCar, "ReserveCar")

server.register_function(GetAllReservations, "GetAllReservations")
server.register_function(GetHotelReservations, "GetHotelReservations")
server.register_function(GetAirlineReservations, "GetAirlineReservations")
server.register_function(GetCarReservations, "GetCarReservations")

server.register_function(DeleteHotelReservation, "DeleteHotelReservation")
server.register_function(DeleteAirlineReservation, "DeleteAirlineReservation")
server.register_function(DeleteCarReservation, "DeleteCarReservation")

server.serve_forever()
