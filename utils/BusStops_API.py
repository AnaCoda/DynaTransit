# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

def connectToBusAPI():
    # No authentication needed
    client = Socrata("data.calgary.ca", None)
    return client


def getAllActiveStopsAsDF():
    cClient = connectToBusAPI()
    # There are less than 8000 stops so this will get them all
    results = cClient.get("muzh-c9qc", where="STATUS='ACTIVE'", limit=8000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return results_df

print(getAllActiveStopsAsDF())