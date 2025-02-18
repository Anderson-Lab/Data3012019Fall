# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 12.2 Dot Maps
#
# A **dot map** is a way to visualize the locations of events in space. In a dot map, points are added to a map to represent the geographic location of some event.
#
# The most important dot map ever made is perhaps John Snow's map of the cholera cases during the 1854 London cholera outbreak. At the time, the cause of cholera was unknown. Snow's dot map showed that the cholera cases centered around a particular water pump, the Broad Street pump. (In the days before running water, residents had to fetch water from the local water pump.) Snow's dot map is shown below; each "dot" is a thin black box. Snow stacked the boxes when there were multiple people in one residence that contracted cholera. At this resolution, the data appear as black bars of different heights, but if you zoom in, you will see the individual "dots".
#
# ![](cholera.jpg)
#
# Snow followed up on his insight by interviewing residents near the Broad Street pump. He found that everyone who had contracted cholera had consumed water from the Broad Street pump; those who lived near the pump but did not contract cholera got their water from a different pump. Thus, one dot map gave John Snow the key insight he needed to identify the cause of cholera.

# Let's look at how to make dot maps in Python. We will make a map of all earthquakes in the world on June 4, 2018. First, we read in the data.

# +
import pandas as pd
pd.options.display.max_rows = 15

quakes = pd.read_csv("https://raw.githubusercontent.com/dlsun/data-science-book/"
                     "master/data/earthquakes.csv")
quakes
# -

# Now, we set up the basic map, just as we did in the previous section. To add the points to the map, we make a scatterplot, just like we learned in Chapter 3, but we have to specify the coordinate system we are using. (Longitude and latitude are not the only way to specify a geographic location.) If the coordinates are specified in latitude and longitude, it is best to use the `Geodetic` transform.

# +
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
# %matplotlib inline

ax = plt.axes(projection=ccrs.Robinson())
ax.stock_img()

quakes.plot.scatter(ax=ax,
                    x="longitude", y="latitude",
                    c="red",
                    transform=ccrs.Geodetic())
# -

# Just as before, we can use size to represent another dimension of the data. In the graphic below, we use size to represent the magnitude of each earthquake.

# +
import numpy as np

ax = plt.axes(projection=ccrs.Robinson())
ax.stock_img()

ax.scatter(quakes["longitude"], quakes["latitude"],
           c="red", s=2 ** quakes["mag"],
           transform=ccrs.Geodetic())
# -

# # Exercises

# **Exercise 1.** The file `https://raw.githubusercontent.com/dlsun/data-science-book/master/data/ncaa-football-stadiums.csv` contains information about the locations and capacity of NCAA football stadiums. Make a dot map that represents this data.

# +
# TYPE YOUR CODE HERE
