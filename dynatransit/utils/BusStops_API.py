# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# pip install shapely
# pip install geopy

from re import X
import pandas as pd
import numpy as np
from sodapy import Socrata
import json

from scipy.spatial.distance import cdist, pdist, euclidean
from shapely.geometry import Point
import geopy.distance
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from . import HERERouting_API

import itertools

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
    return stopPointsDF.iloc[[min_idx]]

# Types: Point, DF (getActiveStopPoints return)
def closestStops(locationPoint, stopPointsDF, amount=3):
    # Transform into a list of tuples ofr each point
    stopPointsList = list((p.x, p.y) for p in stopPointsDF['point'])
    tuplePoint = (locationPoint.x, locationPoint.y)
    # Get the index of the nearest
    min_idxs = np.argsort(cdist([tuplePoint], stopPointsList))[0][:amount]
    closests = stopPointsDF[stopPointsDF.index.isin(min_idxs)]
    return closests

def kmBetweenPoints(Point1, Point2):
    return geopy.distance.vincenty((Point1.x, Point1.y), (Point2.x, Point2.y))


# Turn a list of points into a pandas dataframe of x and y
def pointsListToDF(pointsList):
    pointsData = {'x':[p.x for p in pointsList], 'y':[p.y for p in pointsList]}
    df = pd.DataFrame(pointsData)
    return df

# Get the centroid from a numpy array of locations
def get_centroid(cluster):
    cluster_ary = np.asarray(cluster)
    centroid = cluster_ary.mean(axis=0)
    return centroid

# Given locations, cluster them if they are within a certain distance of each other (unsupervised, without number of clusters)
def clusterLocations(locationPointsList):
    LocationsNP = np.array(pointsListToDF(locationPointsList))
    clustered = DBSCAN(eps=0.025,metric='haversine', min_samples=1).fit(LocationsNP)
    cluster_labels = clustered.labels_
    print(cluster_labels)
    # get the number of clusters
    num_clusters = len(set(clustered.labels_))
    # turn the clusters into a pandas series,where each element is a cluster of points
    dbsc_clusters = pd.Series([LocationsNP[cluster_labels == n] for n in range(num_clusters)])
    return dbsc_clusters

# Given clusters, get their centroids and find the closest stops
def closestStopsToCentroids(clusters):
    # Get the centroids
    centroids = clusters.map(get_centroid)
    print(centroids)
    stops = getActiveStopPoints()
    closeStops = pd.DataFrame()
    for location in centroids:
        locPoint = Point(location)
        print(locPoint)
        print(closestStop(locPoint, stops))
        closeStops = closeStops.append(closestStop(locPoint, stops))
    stopCoords = list(zip(closeStops.stop_name, closeStops.point))
    return stopCoords

def calculateStops(pointsList):
    LocationsNP = np.array(pointsListToDF(pointsList))
    clusters = clusterLocations(pointsList)
    stops = closestStopsToCentroids(clusters)
    print(stops)
    return stops

def farthestStops(stopPoints):
    Npoints = 2 # or 4 or 5...
    print(stopPoints)
    # making up some data:
    data = [[sp[1].x,sp[1].y] for sp in stopPoints]
    # finding row indices of all combinations:
    c = [list(x) for x in itertools.combinations(range(len(data)), Npoints )]

    distances = []
    for i in c:    
        print(i)
        distances.append(euclidean(data[i[0]], data[i[1]])) # pdist: a method of computing all pairwise Euclidean distances in a condensed way.

    ind = distances.index(max(distances)) # finding the index of the max mean distance
    rows = c[ind] # these are the points in question
    print(rows)
    return rows

# Two points in hamptons, two points in sandstone
departures = [Point(51.150250, -114.156370), Point(51.145810, -114.152068), Point(51.142220, -114.109543), Point(51.141654, -114.108165)]
# Central library, city hall
arrivals = [Point(51.047310, -114.057970), Point(51.0460, 114.0574), Point(51.1592957666, -114.066441361), Point(51.1084, 114.0416)]
allPoints = departures + arrivals
# Simply an example
def example():
    return HERERouting_API.findSequence(calculateStops(allPoints))

def findStops(points):
    for point in points:
        print(f'{point.x},{point.y}')
    stops = calculateStops(points)
    print(stops)
    far = farthestStops(stops)
    newStops = [stops[far[0]]]
    for k in range(len(stops)):
        if k != far[1]:
            newStops.append(stops[k])
    newStops.append(stops[far[1]])
    print(newStops)
    return HERERouting_API.findSequence(newStops)