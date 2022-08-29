#need to install simplekml 
#need to install polycircles for local airpots 

import csv 
import os
import simplekml
import logging 


logbook_file = 'Testlog.csv'
airport_database = 'USAirports.csv'

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
kml = simplekml.Kml(open=1)
from polycircles import polycircles


with open( logbook_file, 'r' ) as theFile:
    reader = csv.DictReader(theFile)
    flights = list(reader)
    logging.info('starting with  '+ str(len(flights)) + ' logbook entries')
    
with open( airport_database, 'r' ) as theFile:
    reader = csv.DictReader(theFile)
    usairports = list(reader)

        
#look for ICAO and throw out any with bad data 
for index, flight in enumerate(flights):
    found_from = False
    found_to = False
    for airport in usairports:
        if airport['ident'] == flight['From ']:
            flight["from Lat"]= airport['latitude_deg']
            flight["from Lon"]= airport['longitude_deg']
            found_to = True
        if airport['ident'] == flight['To ']:
            flight["to Lat"]= airport['latitude_deg']
            flight["to Lon"]= airport['longitude_deg']
            found_from = True
    if not (found_to and found_from):    
            logging.info(flights[index])
            flights.pop(index) 
            #print("did not find both")
        

logging.info('found  '+ str(len(flights)) + ' valid routes')

#consolidate routes, and count how many times each one is flow for possible use later 
plotflights = flights.copy() 
for index, flight in enumerate(plotflights):
    flight["count"] = 1
    index2 = index+1 
    while index2 < len(plotflights): 
        if ( ( (flight['From '] == plotflights[index2]['From ']) and (flight['To '] == plotflights[index2]['To ']) ) or  ( ( flight['From '] == plotflights[index2]['To ']) and (flight['To '] == plotflights[index2]['From ']) ) ):
            flight["count"] += 1
            plotflights.pop(index2) #I think this only works becasue I dont pop on the enumerated list...it may still have an issue or two 
        index2 += 1 
        
logging.info('Plotting '+ str(len(plotflights)) + ' consolidated flight routes')


#find local only flights - this does not pop them from the other one yet... 
localflights = plotflights.copy()
for index in range(len(localflights) -1, -1, -1):
    if localflights[index]['From '] != localflights[index]['To ']:
        localflights.pop(index)
logging.info('found  '+ str(len(localflights)) + ' local Flights')


for index, flight in enumerate(localflights):
    polycircle = polycircles.Polycircle(latitude = float(flight['to Lat']),
                                        longitude = float(flight['to Lon']),
                                        radius = 20000,
                                        number_of_vertices = 360)
    pol = kml.newpolygon(name = flight['To '], outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = '990000ff'  # Transparent red

#print(len(plotflights))

for index, flight in enumerate(plotflights):
    linestring = kml.newlinestring(name=flight["From "] + "-" + flight["To "])
    linestring.coords = [(flight["from Lon"],flight["from Lat"]),(flight["to Lon"],flight["to Lat"])]
    linestring.style.linestyle.color = 'ff0000ff'  # Red
    linestring.style.linestyle.width= 2  # 2 pixels


airports=[]
for flight in plotflights:
    airport1 = (flight['To '],flight["to Lon"], flight["to Lat"] )
    airport2 = (flight['From '], flight["from Lon"], flight["from Lat"] )
    if airport1 not in airports:
        airports.append(airport1)
        pnt = kml.newpoint(name=airport1[0], coords=[(airport1[1],airport1[2])]) 
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal2/icon56.png'
    if airport2 not in airports:
        airports.append(airport2)
        pnt = kml.newpoint(name=airport2[0], coords=[(airport2[1],airport2[2])]) 
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal2/icon56.png'

#print(airports)




kml.save(os.path.splitext(__file__)[0] + ".kml")
# to do 
# test from a list of common airports first to narrow down (matbe) 
#collect the locations of the to/from so I can plot pins 

