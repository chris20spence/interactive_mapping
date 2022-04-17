import pandas as pd
import sys
from opencage.geocoder import OpenCageGeocode

key = "7ceff722918946faa1fe35b9f4e9f204"
geocoder = OpenCageGeocode(key)

df = pd.read_csv("Holiday_data.csv")

#print(df)

df["Combined city/country"] = df["City"].str.strip() + ", " + df["Country"].str.strip() #combines city & country 

df = df.reset_index() #makes sure indexes match with number of rows

for index, row in df.iterrows(): 
    
    address = df.loc[index, "Combined city/country"]
    results = geocoder.geocode(address, no_annotations="1")

    if results and len(results):
        longitude = results[0]["geometry"]["lng"]
        latitude = results[0]["geometry"]["lat"]
        df.loc[index, "lon"] = longitude
        df.loc[index, "lat"] = latitude
    else: print(f"{address} not found")

#print(df)

def get_crds(city):
    return df.loc[df["City"] == city, "Crds"].iloc[0]

#print(get_crds("Rome"))

