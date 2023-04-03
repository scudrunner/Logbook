#found a blog where somone pulled KMZs and parsed the data manually. his code found the components 
from lxml import html
import json
import os

#path = "C:\Users\624445\OneDrive - BOOZ ALLEN HAMILTON\Documents\python work\flights"

# Change the directory
#os.chdir(path)

flightroutes=[]




def ingestflights(file_path):
    data = open(file_path, 'r')
    kml = data.read().encode()

    doc = html.fromstring(kml)


    thisflight={}
    position=[]
    Lat=[]
    Lon=[]
    Alt=[]
    timeinfo=[]
    date=[]
    time=[]
    airport=[]
    title=[]

    for pm in doc.cssselect('Document name'): 
        title.append(pm.cssselect('name')[0].text_content())
        #print(title)

    for pm in doc.cssselect('Document Placemark'):  #this depends on the format - the example had FOLDER but my data did no 
        tmp = pm.cssselect('track')
        name = pm.cssselect('name')[0].text_content()
        if len(tmp):
            # Track Placemark
            tmp = tmp[0]  # always one element by definition
            for desc in tmp.iterdescendants():
                content = desc.text_content()
                if desc.tag == 'when':
                    #do_timestamp_stuff(content)
                    timeinfo.append(content)
                    posdata = content.split('T')
                    date.append(posdata[0])
                    time.append(posdata[1])
                elif desc.tag == 'coord':
                    #do_coordinate_stuff(content)
                    posdata = content.split(' ')
                    Lat.append(posdata[0])
                    Lon.append(posdata[1])
                    Alt.append(posdata[2])
                    position.append(content) 
                    #print(content)
                #else:
                    #print("Skipping empty tag %s" % desc.tag)
        else:
            # Reference point Placemark
            #coord = pm.cssselect('Point coordinates')[0].text_content()
            location = pm.cssselect('name')[0].text_content()
            locdata = location.split(' ')
            airport.append(locdata[0])
            #print(coord)
            #do_reference_stuff(coord)

    Position = []
    #print(len(Lat))
    for index in range(len(Lat)):
        location = Lat[index] + ',' + Lon[index] + ',' + Alt[index] + ',' + date[index] + ',' + time[index]
        Position.append(location)
        #print(location)



    #print(Lat)
    #print(date[0])
    #print('from', airport[1] )
    #print('to', airport[0] )
    thisflight['Callsign'] = title[3]
    thisflight['Date']=date[0]
    thisflight['Departure']=airport[0]
    thisflight['Arrival']=airport[1]
    thisflight['Track'] = Position
    #thisflight['LatPath']=Lat 
    #thisflight['LonPath']=Lon 
    #thisflight['AltPath']=Alt 
    #thisflight['TimeStamps']=timeinfo
    return thisflight

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".kml"):
        #file_path = f"{path}\{file}"
        file_path = f"{file}"
  
        # call read text file function
        newflight = ingestflights(file_path)
        flightroutes.append(newflight)


#write a JSON of the data.... to be used at a later time... or another program readable 
with open('flightdata.json', 'w', encoding='utf-8') as f:
    json.dump(flightroutes, f, ensure_ascii=False, indent=4)

#write a JSON of the data.... to be used at a later time... or another program ugly
with open('flightdata2.json', 'w', encoding='utf-8') as f:
    json.dump(flightroutes, f)    

#print(thisflight)
