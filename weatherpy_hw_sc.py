#shaheda choudhury weatherpy hw with weather apis 

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import requests 
import time
import json
import csv

from api_keys import api_key 
from citipy import citipy 

lat_range = (-90, 90)
long_range = (-180, 180)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

#api url for pull and a list to collect the data of the list. 
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key
city_data = []

#making the retrival look pretty
print("Beginning Data Retrieval:")


# Loop through all the cities in our list
counter = 1
for city in cities:
    city_url = url + "&q=" + city
    print(f"Processing Record {counter} | {city}")
    counter = counter + 1

    
# run the Api request to gety the cities we are evaluating 
    try:
        city_weather = requests.get(city_url).json()
        
#parsing the data and creating a data fram with the data
        city_lat = city_weather["coord"]["lat"]
        city_lng = city_weather["coord"]["lon"]
        city_max_temp = city_weather["main"]["temp_max"]
        city_humidity = city_weather["main"]["humidity"]
        city_clouds = city_weather["clouds"]["all"]
        city_wind = city_weather["wind"]["speed"]
        city_country = city_weather["sys"]["country"]
        city_date = city_weather["dt"]
        
#create dictionary 
        city_data.append({"City": city,
                         "Lat": city_lat,
                         "lng": city_lng,
                         "Max Temp": city_max_temp,
                         "Humidity": city_humidity,
                         "Cloudiness": city_clouds,
                         "Wind Speed": city_wind,
                         "Country": city_country,
                         "Date": city_date})
    except:
        print(f"City {city} not found. Skipping to next city.")
    pass
    
#making the retrival look pretty
print("Data Retrieval Complete!!!")

city_pd = pd.DataFrame(city_data)

#creating columns for the csv with the df values
lats = city_pd["Lat"]
max_temps = city_pd["Max Temp"]
humidity = city_pd["Humidity"]
cloudiness = city_pd["Cloudiness"]
wind_speed = city_pd["Wind Speed"]

city_pd.count()

#ploting the data

#graph 1: lat vs temp

date = time.strftime("%m/%d/%Y")

plt.scatter(lats, max_temps)
plt.title(f"City Latitude vs. Max Temperature {date}")
plt.xlabel("Latitude")
plt.ylabel("Temperature (F)")
plt.grid()
plt.savefig("Temperature.png")
plt.show()


# graph 2 lat vs humididty

date = time.strftime("%m/%d/%Y")

plt.scatter(lats, humidity)
plt.title(f"City Latitude vs. Humidity {date}")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid()
plt.show()


#graph 3 lat vs cloudiness

date = time.strftime("%m/%d/%Y")

plt.scatter(lats, cloudiness)
plt.title(f"City Latitude vs. Cloudiness {date}")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid()
plt.show()

#lat vs wind speed

date = time.strftime("%m/%d/%Y")

plt.scatter(lats, cloudiness)
plt.title(f"City Latitude vs. Cloudiness {date}")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid() 
plt.show()

#Export the city data frame into a csv
output_csv = 'cities_info.csv'
city_pd.to_csv(output_csv, index_label='City_ID') 

