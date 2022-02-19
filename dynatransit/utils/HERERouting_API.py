import requests


api_key = 'rdE07wGvlGAMwAOwQ52_gRcyKvm9uqsCC8agWPbgkqY' # Acquire from developer.here.com
PARAMS = {'apikey':api_key,'q':location} 

def findSequence(pointsList):
    URL = "https://https://wse.ls.hereapi.com/2/findsequence.json"
    PARAMS = {'apikey':api_key,'start':location}
    
    print(locationList)

def loc_to_waypoint(self, location):
        return str(location[1][0]) + ',' + str(location[1][1])

def findSequence(pointsList):
    locationList = []
    for point in pointsList:
        locationList.append((point[0], [point[1].x, point[1].y]))
    app_data = {}
    app_data['start'] = loc_to_waypoint(locationList[0])
    for i, cl in enumerate(locationList):
        if i == 0:
            continue
        app_data['destination' + str(i)] = self.loc_to_waypoint(cl)
        if i == 10:
            break

    app_data['end'] = self.loc_to_waypoint(self.container_locations[-1])
    app_data['mode'] = 'truck;fastest'

    s = Session()
    req = Request('GET', url=self.sequence_url, params=app_data).prepare()

    # This URL can be copy/pasted into a browser and returns an optimized sequence
    print (req.url)

    # this call blocks
    r = s.send(req)

    # this call also blocks
    # r = requests.get(self.sequence_url, app_data)

    print (r.json())

# sending get request and saving the response as response object 
'''r = requests.get(url = URL, params = PARAMS) 
data = r.json()'''