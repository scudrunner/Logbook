# Logbook
 Plot flight paths from a logbook 

Step 1 - use Spreadsheet Logbbok - I use Google Sheets and the heading are important
Step -2 - export to CSV
Step 3 - Process with Python - exporting JSON file 

Step 4 - Consolidate the flightaware files into one file 
        bulkreadflightradar.py  exporting to flightdata.json  

Step 5 - Run Python code to match up flightdata.json to data
    addtrack.py reads Logbook_with_routes2023.json and  flightdata.json
        it looks to see if a route is already there and ignores the flightdata if one is there

Step 6- View with Map 
    currently testmap3.html reading Logbook_with_routes2023.json

Still to do - 

figure out updates to core JSON file.....  how to add a flight to main database. Just need to write it... 
Add filters for the map - select which flight to view on altitude...        




 to view a webpage locally - 
 http://localhost:8000/Leaflet.html#close
 python3 -m http.server
