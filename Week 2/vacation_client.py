#!/usr/bin/python3

# imports
import xmlrpc.client
from time import sleep

# connect
s = xmlrpc.client.ServerProxy("http://localhost:8800")

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
