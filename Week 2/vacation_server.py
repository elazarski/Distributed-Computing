#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pandas import DataFrame

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


hotels = ["Motel 6", "Air BNB"]
airlines = ["United", "Private Jet"]
cars = ["Lexus, Ford"]

reservations = DataFrame(columns=["type", "detail", "startDate", "endDate"])

# get methods
def GetHotels():
    return hotels
def GetAirlines():
    return airlines
def GetCars():
    return cars

# reserve methods
def ReserveHotel(hotel, startDate, endDate):
    if hotel in hotels:
        global reservations
        reservation = {
                "type":"hotel", 
                "detail":hotel, 
                "startDate":startDate, 
                "endDate":endDate}
        reservations = reservations.append(reservation, ignore_index=True) 
        return reservation
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
        reservations = reservations.append(reservation, ignore_index=True)
        return reservation
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
        reservations = reservations.append(reservation, ignore_index=True)
        return reservation
    else:
        return False

def GetAllReservations(): 
    return reservations.to_string()

def GetHotelReservations():
    hotelReservations = reservations[reservations.type == "hotel"]
    hotelReservations = hotelReservations.T.drop("type").T
    hotelReservations = hotelReservations.rename(columns={"detail":"hotel"})
    return hotelReservations.to_string()

def GetAirlineReservations():
    airlineReservations = reservations[reservations.type == "airline"]
    airlineReservations = airlineReservations.T.drop("type").t
    airlineReservations = airlineReservations.rename(columns={"detail":"airline"})
    return airlineReservations.to_string()

def GetCarReservations():
    carReservations = reservations[reservations.type == "car"]
    carReservations = carReservations.T.drop("type").T
    carReservations = carReservations.rename(columns={"detail":"car"})
    return carReservations.to_string()

def DeleteHotelReservation(hotel, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.type == "hotel") &
            (reservations.detail == hotel) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

def DeleteAirlineReservation(airline, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.type == "airline") &
            (reservations.detail == airline) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

def DeleteCarReservation(car, startDate, endDate):
    global reservations
    drop = reservations[
            (reservations.type == "car") &
            (reservations.detail == car) &
            (reservations.startDate == startDate) &
            (reservations.endDate == endDate)]
    reservations = reservations.drop(drop.index)
    return True

# server stuff
server = SimpleXMLRPCServer(("localhost", 8800), requestHandler=RequestHandler, allow_none=True)
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
