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
    results_df['point'] = results_df['point'].apply(lambda point : Point(point['coordinates'][0],point['coordinates'][1]))
    return results_df


print(getActiveStopPoints())