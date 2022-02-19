# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# pip install shapely
# pip install geopy

import pandas as pd
import numpy as np
from sodapy import Socrata
import json

from scipy.spatial.distance import cdist
from shapely.geometry import Point
import geopy.distance
from sklearn.cluster import KMeans

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
    return stopPointsDF[min_idx:min_idx+1].first

# Types: Point, DF (getActiveStopPoints return)
def closestStops(locationPoint, stopPointsDF, amount=3):
    # Transform into a list of tuples ofr each point
    stopPointsList = list((p.x, p.y) for p in stopPointsDF['point'])
    tuplePoint = (locationPoint.x, locationPoint.y)
    # Get the index of the nearest
    min_idxs = np.argsort(cdist([tuplePoint], stopPointsList))[0][:amount]
    closests = stopPointsDF[stopPointsDF.index.isin(min_idxs)]
    print(closests)

def kmBetweenPoints(Point1, Point2):
    return geopy.distance.vincenty((Point1.x, Point1.y), (Point2.x, Point2.y))

departures = [Point(51.150250, -114.156370), Point(51.145810, -114.152068), Point(51.142220, -114.109543), Point(51.141654, -114.108165)]

def pointsListToDF(pointsList):
    pointsData = {'x':[p.x for p in pointsList], 'y':[p.y for p in pointsList]}
    df = pd.DataFrame(pointsData)
    return df

print(closestStops(Point(51.150250, -114.156370), getActiveStopPoints()))

DeparturesNP = np.array(pointsListToDF(departures))
print(DeparturesNP)
