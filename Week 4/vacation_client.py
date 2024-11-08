#!/usr/bin/python3

# imports
import xmlrpc.client
from time import sleep

# connect to servers
connectionString = "http://{0}:{1}"

ip = input("Enter hotel server IP: ")
port = input("Enter hotel server port: ")
hotelString = connectionString.format(ip, port)
print("Connecting to: {0}".format(hotelString))
hotelServer = xmlrpc.client.ServerProxy(hotelString)

ip = input("Enter airline server IP: ")
port = input("Enter airline server port: ")
airlineString = connectionString.format(ip, port)
print("Connecting to {0}".format(airlineString))
airlineServer = xmlrpc.client.ServerProxy(airlineString)

ip = input("Enter car server IP: ")
port = input("Enter car server port: ")
carString = connectionString.format(ip, port)
print("Connecting to {0}".format(carString))
carServer = xmlrpc.client.ServerProxy(carString)

connected = True

# assignment part
if connected:
    print("Getting hotel list...")
    try:
        print(hotelServer.GetHotels())
    except ConnectionRefusedError:
        print("Hotel server unreachable! Aborting!")
        connected = False
print("")

if connected:
    print("Getting airline list...")
    try:
        print(airlineServer.GetAirlines())
    except ConnectionRefusedError:
        print("Airline server unreachable! Aborting!")
        connected = False
print("")

if connected:
    print("Getting car list...")
    try:
        print(carServer.GetCars())
    except ConnectionRefusedError:
        print("Car server unreachable! Aborting!")
        connected = False
print("")


if connected:
    print("Reserving hotel...")
    try:
        print(hotelServer.ReserveHotel("Motel 6", "tomorrow", "next week"))
    except ConnectionRefusedError:
        print("Hotel server unreachable! Aborting!")
        conntected = False

        print("Deleing existing reservations!")
        airlineServer.DeleteAllReservations()
        carServer.DeleteAllReservations()
print("")

if connected:
    print("Reserving airline...")
    try:
        print(airlineServer.ReserveAirline("Private Jet", "now", "midnight"))
    except ConnectionRefusedError:
        print("Airline server unreachable! Aborting!")
        connected = False

        print("Deleting existing reservations!")
        hotelServer.DeleteAllReservations()
        carServer.DeleteAllReservations()
print("")

print("Sleeping for 5 seconds...")
sleep(5)
print("")

if connected:
    print("Reserving car...")
    try:
        print(carServer.ReserveCar("Lexus", "next week", "a month from now"))
    except ConnectionRefusedError:
        print("Car server unreachable! Aborting!")
        connected = False

        print("Deleting existing reservations!")
        hotelServer.DeleteAllReservations()
        airlineServer.DeleteAllReservations()
print("")

print("Getting reservations...")

print("Getting hotel reservations...")
print(hotelServer.GetHotelReservations())
print("")

print("Getting airline reservations...")
print(airlineServer.GetAirlineReservations())
print("")

print("Getting car reservations...")
print(carServer.GetCarReservations())
print("")
