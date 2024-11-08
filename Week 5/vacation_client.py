#!/usr/bin/python3

# imports
import xmlrpc.client
from time import sleep

# connect
ip = input("Enter server IP: ")
port = input("Enter server port: ")
print("Connecting to http://{0}:{1}".format(ip, port))
s = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))

# assignment part
print("Hotels")
print(s.GetHotels())
print("")

print("Reserving hotel")
print(s.ReserveHotel("Motel 6", "tomorrow", "next week"))
print("")

print("sleeping for 5 seconds")
sleep(5)
print("")

print("Getting reservations")
print(s.GetHotelReservations())
print("")

print("Deleting reservation")
print(s.DeleteHotelReservation("Motel 6", "tomorrow", "next week"))
print("")

print("Getting reservations")
print(s.GetHotelReservations())
print("")
