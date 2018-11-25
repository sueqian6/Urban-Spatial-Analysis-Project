
# coding: utf-8

# In[2]:


import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library


# In[3]:


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium

print('Folium installed and imported!')


# In[4]:


latitude = 40.730610
longitude = -73.935242


# In[5]:


# create map and display it
newyork_map = folium.Map(location=[latitude, longitude], zoom_start=12)

newyork_map


# In[6]:


from __future__  import print_function, division
import pylab as pl
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt


# In[7]:



#I am starting with a single month of data: reading data from citibike csv file from jan 2018
def getCitiBikeCSV(datestring):
    print ("Downloading", datestring)
    ### First I will heck that it is not already there
    if not os.path.isfile("./" + datestring + "-citibike-tripdata.csv"):
        if os.path.isfile(datestring + "-citibike-tripdata.csv"):
            # if in the current dir just move it
            if os.system("mv " + datestring + "-citibike-tripdata.csv " + "./"):
                print ("Error moving file!, Please check!")
        #otherwise start looking for the zip file
        else:
            if not os.path.isfile("./" + datestring + "-citibike-tripdata.zip"):
                if not os.path.isfile(datestring + "-citibike-tripdata.zip"):
                    os.system("curl -O https://s3.amazonaws.com/tripdata/" + datestring + "-citibike-tripdata.csv.zip")
                    #https://s3.amazonaws.com/tripdata/JC-201808-citibike-tripdata.csv.zip
                ###  To move it I use the os.system() functions to run bash commands with arguments
                os.system("mv " + datestring + "-citibike-tripdata.csv.zip " + "./")
            ### unzip the csv 
            os.system("unzip " + "./" + datestring + "-citibike-tripdata.csv.zip")
            ## NOTE: old csv citibike data had a different name structure. 
            if '2014' in datestring:
                os.system("mv " + datestring[:4] + '-' +  datestring[4:] + 
                          "\ -\ Citi\ Bike\ trip\ data.csv " + datestring + "-citibike-tripdata.csv")
            os.system("mv " + datestring + "-citibike-tripdata.csv " + "./")
    ### One final check:
    if not os.path.isfile("./" + datestring + "-citibike-tripdata.csv"):
        print ("WARNING!!! something is wrong: the file is not there!")

    else:
        print ("file in place, you can continue")


# In[8]:


df_list = []
for i in range(1):
    
    m = str(i+1).zfill(2)
    datestring = '2018'+m
    getCitiBikeCSV(datestring)
    df = pd.read_csv(  "./" + datestring + '-citibike-tripdata.csv')
    df_list.append(df)


# In[9]:


df = pd.concat(df_list)
df['date'] = pd.to_datetime(df['starttime'])
df.head()


# In[10]:


f = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f')
df['starttime'] = df['starttime'].apply(f)
df['stoptime'] = df['stoptime'].apply(f)


# In[11]:


filter_night = lambda x: x.hour > 17
df['is_night'] = df['starttime'].apply(filter_night)


# In[12]:


df = df[df['is_night'] == True]


# In[16]:


filter_isdayone = lambda x:x.day<2
df['is11']=df['starttime'].apply(filter_isdayone)
df=df[df['is11']==True]


# In[18]:


df.tail()


# In[19]:


longitude = list(df['start station longitude']) + list(df['end station longitude'])
latitude = list(df['start station latitude']) + list(df['end station latitude'])
plt.figure(figsize = (10,10))
plt.plot(longitude,latitude,'.', alpha = 1, markersize = 5)
plt.show()


# In[20]:


unique_longitude = list(df['start station longitude'].unique()) + list(df['end station longitude'].unique())
unique_latitude = list(df['start station latitude'].unique()) + list(df['end station latitude'].unique())


# In[21]:


# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through and add each to the incidents feature group
for lat, lng, in zip(latitude, longitude):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add incidents to map
newyork_map.add_child(incidents)


# In[22]:


def birth_year_filter(yr):
    age = 2018 - yr
    if age <= 18:
        return "Adolescence"
    elif age <= 30:
        return "Adult"
    elif age <= 60:
        return "Middle-Aged"
    else:  # > 60
        return "Senior Adult"
df['agegroup'] = df['birth year'].apply(birth_year_filter)


# In[27]:


# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through and add each to the incidents feature group
for lat, lng, in zip(latitude, longitude):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add pop-up text to each marker on the map
latitudes = list(latitude)
longitudes = list(longitude)
labels = list(df.agegroup)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(newyork_map)    
    
# add incidents to map
newyork_map.add_child(incidents)


# In[24]:


# create map and display it
newyork_map = folium.Map(location=[40.730610, -73.935242], zoom_start=12)

# loop through and add each to the map
for lat, lng, label in zip(latitude, longitude, df.agegroup):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5, # define how big you want the circle markers to be
        color='yellow',
        fill=True,
        popup=label,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(newyork_map)

# show map
newyork_map


# In[25]:


from folium import plugins

# let's start again with a clean copy of the map of San Francisco
newyork_map = folium.Map(location = [40.730610, -73.935242], zoom_start = 12)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(newyork_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(latitude, longitude, df.agegroup):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# display map
newyork_map

