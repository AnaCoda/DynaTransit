# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# pip install shapely

import pandas as pd
import numpy as np
from sodapy import Socrata
import json

from scipy.spatial.distance import cdist
from shapely.geometry import Point

def connectToBusAPI():
    # No authentication needed
    client = Socrata("data.calgary.ca", None)
    return client


def getAllActiveStopsAsDF():
    cClient = connectToBusAPI()
    # There are less than 8000 stops so this will get them all
    results = cClient.get("muzh-c9qc", where="STATUS='ACTIVE'", limit=8000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results, columns=["teleride_number", "stop_name", "point"])
    return results_df

def getActiveStopPoints():
    results_df = getAllActiveStopsAsDF()
    print(results_df)
    # Create a latitude, longitude point and change the dataset
    results_df['point'] = results_df['point'].apply(lambda point : Point(point['coordinates'][1],point['coordinates'][0]))
    return results_df

# Types: Point, DF (getActiveStopPoints return)
def closestStop(locationPoint, stopPointsDF):
    # Transform into a list of tuples ofr each point
    stopPointsList = list((p.x, p.y) for p in stopPointsDF['point'])
    tuplePoint = (locationPoint.x, locationPoint.y)
    # Get the index of the nearest
    min_idx = cdist([tuplePoint], stopPointsList).argmin()
    return stopPointsDF[min_idx:min_idx+1]


print(closestStop(Point(51.150250, -114.156370), getActiveStopPoints()))