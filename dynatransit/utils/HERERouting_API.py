import requests


api_key = 'JdR1F4vpXx_HoCgrfwrmkPQxdz9nBBVjZ9W8ypWuViA' # Acquire from developer.here.com

def loc_to_waypoint(location):
        return str(location[1][0]) + ',' + str(location[1][1])

def get_demo_route():
    url = "https://wse.ls.hereapi.com/2/calculateroute.json"
    # app_data = {"app_id": self.app_id, "app_code": self.app_code}
    app_data = {"waypoint0": "52.5,13.4", "waypoint1":"52.5,13.45", "mode": "fastest;car;traffic:disabled"}
    app_data['apiKey'] = api_key
    print (requests.get(url, app_data).json())

#get_demo_route()

def findSequence(pointsList):
    sequence_url = "https://wse.ls.hereapi.com/2/findsequence.json"
    locationList = []
    for point in pointsList:
        locationList.append((point[0], [point[1].x, point[1].y]))
    app_data = {}
    app_data['start'] = loc_to_waypoint(locationList[0])
    for i, cl in enumerate(locationList):
        if i == 0:
            continue
        app_data['destination' + str(i)] = loc_to_waypoint(cl)
        if i == 10:
            break

    app_data['apiKey'] = api_key
    app_data['end'] = loc_to_waypoint(locationList[-1])
    app_data['mode'] = 'car;fastest'

    s = requests.Session()
    req = requests.Request('GET', url=sequence_url, params=app_data).prepare()

    # this call blocks
    r = s.send(req)

    # this call also blocks
    # r = requests.get(self.sequence_url, app_data)

    waypoints = r.json()['results'][0]['waypoints']
    wayArr = {'routingMode': 'fast',
    'transportMode': 'car',
    'return': 'polyline'}
    for p in waypoints:
        wayArr[p['id']] = f"{p['lat']},{p['lng']}"
    return wayArr


# sending get request and saving the response as response object 
'''r = requests.get(url = URL, params = PARAMS) 
data = r.json()'''