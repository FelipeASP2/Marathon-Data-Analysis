import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

#Read and curate the data.
df = pd.read_csv("data/ff_race_50.csv", sep = ";")
curated_df = df.dropna(axis = 1)
#print(curated_df.head())

# Merge First and Last name columns into one.
curated_df["Name"] = curated_df["First"] + " " + curated_df["Last"]


#Change time column metrics and create new column in minutes.
curated_df["Time"] = pd.to_timedelta(curated_df["Time"])
curated_df["Total_Minutes"] = curated_df["Time"].dt.total_seconds() / 60
curated_df["Total_Minutes"] = curated_df["Total_Minutes"].round().astype(int)


#Latitude and Longitude
def get_latitude_longitude(city, state):
    address = f"{city}, {state}"
    try:
        geolocator = Nominatim(user_agent = "running", timeout = 10)
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

curated_df["Latidute"], curated_df["Longitude"] = zip(*curated_df.apply(lambda x: get_latitude_longitude(x["City"], x["State"]), axis = 1))
curated_df["LatLong"] = curated_df["Latidute"].astype(str) + ", " + curated_df["Longitude"].astype(str)


#New df
curated_df.to_csv("data/cleaned_up_data.csv")