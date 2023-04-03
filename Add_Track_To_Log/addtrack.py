#need to install simplekml 
#need to install polycircles for local airpots 
# 3/31/23 - I have it reading a CSV of my logbook and outputting a form of JSON - need to clean it up
#3/31 added an international airfield database - manually created it with one airport 

#to-do 
# want to export a geojson so I can use it in leaflet


import os
#import simplekml
import logging 
import json
import datetime as dt
from datetime import datetime


#if you load a json with routes already - it will check and not overwrite
file = open('Logbook_with_routes2023.json')
logbook = json.load(file)
file.close()

file2 = open('flightdata.json')
FlightTracks = json.load(file2)
file2.close()


#iterate through the data - big list first and then look for tracks in small list 

count = 0 
for flight in logbook:
    data = flight['Date']
    Fday = data.split('/')
    if (len(Fday[0]) == 1):
        Fday[0] = '0' + Fday[0]
    if (len(Fday[1]) == 1):
        Fday[1] = '0' + Fday[1]

    date1=Fday[0]+'/'+Fday[1]+'/'+Fday[2]
    Fdayobj = dt.datetime.strptime(date1, "%m/%d/%Y")  


    # format of date - month can be single "Date": "8/30/2022",

    for path in FlightTracks:
        C = False
        D = False 
        M = False 
        Y = False
        date = False
        Dep = False
        Arr = False 
        data2 = path["Date"]
        Pdate = data2.split('-')
        date2 = Pdate[1]+'/'+Pdate[2]+'/'+Pdate[0]
        Pdayobj = dt.datetime.strptime(date2, "%m/%d/%Y") 


        # format of "Date": "2023-02-17"
        if (flight['Callsign']==path['Callsign']):
            C = True 
        if (flight['Departure']==path['Departure']):
            Dep = True 
        if (flight['Arrival']==path['Arrival']):
            Arr = True 
        #track may be on next zulu day    
        if ((Pdayobj == Fdayobj) or (Pdayobj == (Fdayobj+dt.timedelta(days=1))) ): 
            date = True    
        # if ( Fday[0] == Pdate[1] ):  #looking at month
        #     M = True
        # if ( Fday[1] == Pdate[2] ): #looking at day 
        #     D = True
        # if ( Fday[2] == Pdate[0] ): #looking at year 
        #     Y = True    
        if (C and date and Dep and Arr):
            #print('found one', flight['Callsign'], '  ', path['Callsign'], '  ', data, '   ', data2, 'from ', flight['Departure'], '/', path['Departure'], 'to', flight['Arrival'],'/',path['Arrival']  )
            if (flight.get('Route') == None ) :    
                count +=1
                flight['Route']=path['Track']
       
            
file1 = 'Logbook_with_routes'
file1= file1 +datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.json'
with open(file1, 'w', encoding='utf-8') as f:
    json.dump(logbook, f, ensure_ascii=False, indent=4)


print(len(FlightTracks),' tracks input')
print(count,' tracks found')





