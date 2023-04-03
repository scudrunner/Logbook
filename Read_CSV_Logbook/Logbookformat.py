#need to install simplekml 
#need to install polycircles for local airpots 
# 3/31/23 - I have it reading a CSV of my logbook and outputting a form of JSON - need to clean it up
#3/31 added an international airfield database - manually created it with one airport 

#to-do 
# want to export a geojson so I can use it in leaflet

import csv 
import os
import simplekml
import logging 
import json
from datetime import datetime


#  ï»¿   was in the Date index when opening CSV from microsoft  - it is the Byte Order Mark - anoying.... 
#Open your file in Notepad++. From the Encoding menu, select Convert to UTF-8 without BOM, save the file
#  replace the old file with this new file. And it will work, damn sure.

logbook_file = 'Republic.csv'
USA_airport_database = 'USAirports.csv'
Int_airport_database =  'int_airports.csv'

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
kml = simplekml.Kml(open=1)
from polycircles import polycircles


with open( logbook_file, 'r' ) as theFile:
    reader = csv.DictReader(theFile)
    flights = list(reader)
    logging.info('starting with  '+ str(len(flights)) + ' logbook entries')
origin = 'Departure'
destination = 'Arrival'    





with open( USA_airport_database, 'r' ) as theFile:
    reader = csv.DictReader(theFile)
    usaairports = list(reader)

with open( Int_airport_database, 'r' ) as theFile:
    reader = csv.DictReader(theFile)
    intairports = list(reader)

airportlist = intairports + usaairports



#strip white space and capitalize 
for flight in flights:
    flight[origin] = flight[origin].strip()
    flight[origin] = flight[origin].upper()
    flight[destination] = flight[destination].strip()
    flight[destination] = flight[destination].upper()

    #for Republic Flights 
    callsign ='RPA' + flight['Flight Number'][2:]
    flight['Callsign'] = callsign


        
#look for ICAO and throw out any with bad data 
for index, flight in enumerate(flights):
    found_from = False
    found_to = False
    for airport in airportlist:
        if airport['ident'] == flight['Departure']:
            flight["from Lat"]= airport['latitude_deg']
            flight["from Lon"]= airport['longitude_deg']
            flight["from name"] = airport['name']
            found_to = True
        if airport['ident'] == flight['Arrival']:
            flight["to Lat"]= airport['latitude_deg']
            flight["to Lon"]= airport['longitude_deg']
            flight["to name"] = airport['name']
            found_from = True
    if not (found_to and found_from):    
            logging.info(flights[index])
            flights.pop(index) 
            #print("did not find both")
        

logging.info('found  '+ str(len(flights)) + ' valid routes')



#consolidate routes, and count how many times each one is flow for possible use later 
plotflights = []

# for index, sortie in enumerate(plotflights):
#     #plotflights[index]['count'] = 1
#     index2 = index+1 
#     while index2 < len(plotflights): 
#         if ( ( (sortie['Departure'] == plotflights[index2]['Departure']) and (sortie['Arrival'] == plotflights[index2]['Arrival']) ) or  ( ( sortie['Departure'] == plotflights[index2]['Arrival']) and (sortie['Arrival'] == plotflights[index2]['Departure']) ) ):
#             #plotflights[index]['count'] += 1
#             plotflights.pop(index2) #I think this only works becasue I dont pop on the enumerated list...it may still have an issue or two -- but i do pop there.... 
#         index2 += 1 

# If I did not read something in - populate it now to start - did not ned it  
# if (len(plotflights)==0):
#     plotflights1={}
#     plotflights1['Departure'] = flights[0]['Departure']
#     plotflights1['Arrival'] = flights[0]['Arrival']
#     plotflights1['from Lat'] = flights[0]['from Lat']
#     plotflights1["from Lon"] = flights[0]["from Lon"]
#     plotflights1["from name"] = flights[0]["from name"]
#     plotflights1['to Lat'] = flights[0]['to Lat']
#     plotflights1["to Lon"] = flights[0]["to Lon"]
#     plotflights1["to name"] = flights[0]["to name"]
#     plotflights1["count"] = 1
#     plotflights.append(plotflights1)


# print(len(flights))

for index, sortie in enumerate(flights):
    found = False
    for index2, path in enumerate(plotflights):
        
        if ((sortie['Departure'] == path['Departure']) and (sortie['Arrival'] == path['Arrival'])):
            path['count'] +=1
            found = True
            break
    if not found :
            plotflights1={}
            plotflights1['Departure'] = sortie['Departure']
            plotflights1['Arrival'] = sortie['Arrival']
            plotflights1['from Lat'] = sortie['from Lat']
            plotflights1["from Lon"] = sortie["from Lon"]
            plotflights1["from name"] = sortie["from name"]
            plotflights1['to Lat'] = sortie['to Lat']
            plotflights1["to Lon"] = sortie["to Lon"]
            plotflights1["to name"] = sortie["to name"]
            plotflights1["count"] = 1
            plotflights.append(plotflights1)






        
logging.info('Plotting '+ str(len(plotflights)) + ' consolidated flight routes')


#find local only flights - this does not pop them from the other one yet... 
localflights = plotflights.copy()
for index in range(len(localflights) -1, -1, -1):
    if localflights[index]['Departure'] != localflights[index]['Arrival']:
        localflights.pop(index)
logging.info('found  '+ str(len(localflights)) + ' local Flights')


for index, flight in enumerate(localflights):
    polycircle = polycircles.Polycircle(latitude = float(flight['to Lat']),
                                        longitude = float(flight['to Lon']),
                                        radius = 20000,
                                        number_of_vertices = 360)
    pol = kml.newpolygon(name = flight['Arrival'], outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = '990000ff'  # Transparent red

#print(len(plotflights))

for index, flight in enumerate(plotflights):
    linestring = kml.newlinestring(name=flight['Departure'] + "-" + flight['Arrival'])
    linestring.coords = [(flight["from Lon"],flight["from Lat"]),(flight["to Lon"],flight["to Lat"])]
    linestring.style.linestyle.color = 'ff0000ff'  # Red
    linestring.style.linestyle.width= 2  # 2 pixels


airports=[]
for flight in plotflights:
    airport1 = (flight['Arrival'],flight["to Lon"], flight["to Lat"], flight["to name"] )
    airport2 = (flight['Departure'], flight["from Lon"], flight["from Lat"], flight["from name"] )
    if airport1 not in airports:
        airports.append(airport1)
        pnt = kml.newpoint(name=airport1[0], coords=[(airport1[1],airport1[2])], description= airport1[3]) 
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal2/icon56.png'
    if airport2 not in airports:
        airports.append(airport2)
        pnt = kml.newpoint(name=airport2[0], coords=[(airport2[1],airport2[2])], description= airport2[3]  ) 
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal2/icon56.png'

#print(airports)

#write a JSON of the data.... to be used at a later time... or another program
file = 'logbookdata'
file= file +datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.json'

print(file)
with open(file, 'w', encoding='utf-8') as f:
    json.dump(flights, f, ensure_ascii=False, indent=4)

file2 = 'consolidated_Flights'
file2= file2 +datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.json'
with open(file2, 'w', encoding='utf-8') as f:
    json.dump(plotflights, f, ensure_ascii=False, indent=4)



kml.save(os.path.splitext(__file__)[0] + ".kml")
# to do 
# test from a list of common airports first to narrow down (matbe) 
#collect the locations of the to/from so I can plot pins 

