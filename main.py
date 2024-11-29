from opensky_api import OpenSkyApi
from time import time, gmtime
from math import floor
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Get airport data
df = pd.read_csv("world-airports.csv")

api = OpenSkyApi(username,password)

ner_jets= ["440241", "440d18","440214", "440b18", "4401d7"]
# OE-LOT, OE-HUG, OE-HOZ, OE-XWY, OE-LEM 

for icao in ner_jets:
    data = api.get_flights_by_aircraft(icao,floor(time()) - 2592000, floor(time())-2000)
    if data is not None:
        for flight in data:
            #print the data
            fyear = gmtime(flight.firstSeen).tm_year
            fmon = gmtime(flight.firstSeen).tm_mon
            fday = gmtime(flight.firstSeen).tm_mday
            fhour = gmtime(flight.firstSeen).tm_hour
            fmin = gmtime(flight.firstSeen).tm_min

            dep_name = "Unknown"
            dep_country = "Unknown"
            dep_region = "Unknown"
            dep_municipality = "Unknown"

            if flight.estDepartureAirport is not None:
                dep_airport = df[df["ident"] == flight.estDepartureAirport]
                dep_name = dep_airport["name"].iloc[0]
                dep_country = dep_airport["country_name"].iloc[0]
                dep_region = dep_airport["region_name"].iloc[0]
                dep_municipality = dep_airport["municipality"].iloc[0]
            
            arr_name = "Unknown"
            arr_country = "Unknown"
            arr_region = "Unknown"
            arr_municipality = "Unknown"

            if flight.estArrivalAirport is not None:
                arr_airport = df[df["ident"] == flight.estArrivalAirport]
                arr_name = arr_airport["name"].iloc[0]
                arr_country = arr_airport["country_name"].iloc[0]
                arr_region = arr_airport["region_name"].iloc[0]
                arr_municipality = arr_airport["municipality"].iloc[0]

            callsign = "Unknown"
            if flight.callsign is not None:
                callsign = flight.callsign

            lyear = gmtime(flight.lastSeen).tm_year
            lmon = gmtime(flight.lastSeen).tm_mon
            lday = gmtime(flight.lastSeen).tm_mday
            lhour = gmtime(flight.lastSeen).tm_hour
            lmin = gmtime(flight.lastSeen).tm_min

            

            print(f"Aircraft: {icao}\nCallsign: {callsign}\nFirst seen: {fyear}.{fmon}.{fday} {fhour}:{fmin} GMT\nDeparture: {dep_name}, {dep_country}, {dep_region}, {dep_municipality}\nLast seen: {lyear}.{lmon}.{lday} {lhour}:{lmin} GMT\nArrival: {arr_name}, {arr_country}, {arr_region}, {arr_municipality}\n")
