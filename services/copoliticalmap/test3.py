# Learn about API authentication here: https://plotly.com/python/getting-started
# Find your api_key here: https://plotly.com/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('username', 'api_key')
trace1 = {
  "type": "scattergeo", 
  "lat": [40.7305991, 34.053717, 41.8755546, 29.7589382], 
  "lon": [-73.9865812, -118.2427266, -87.6244212, -95.3676974], 
  "marker": {"size": [29.7875632869474, 20.5612448479129, 17.4487902290716, 15.5937794967582]}, 
  "inherit": True, 
  "text": ["New York<br>Population: 8287238", "Los Angeles<br>Population: 3826423", "Chicago<br>Population: 2705627", "Houston<br>Population: 2129784"]
}
trace2 = {
  "type": "choropleth", 
  "z": [19746227, 38802500, 12880580, 26956958], 
  "lat": [40.7305991, 34.053717, 41.8755546, 29.7589382], 
  "lon": [-73.9865812, -118.2427266, -87.6244212, -95.3676974], 
  "marker": {"size": [29.7875632869474, 20.5612448479129, 17.4487902290716, 15.5937794967582]}, 
  "inherit": True, 
  "text": ["NY<br>Population: 19746227", "CA<br>Population: 38802500", "IL<br>Population: 12880580", "TX<br>Population: 26956958"], 
  "colorbar": {"title": ["$", "df_states", "pop"]}, 
  "colorscale": [
    [0, "#FCFBFD"], [0.111111111111111, "#F0EFF6"], [0.222222222222222, "#DFDEED"], [0.333333333333333, "#C6C7E1"], [0.444444444444445, "#ABA9D1"], [0.555555555555556, "#918DC2"], [0.666666666666667, "#796EB2"], [0.777777777777778, "#65489F"], [0.888888888888889, "#52248D"], [1, "#3F007D], 
  "locationmode": "USA-states", 
  "locations": ["NY", "CA", "IL", "TX"]
}
data = Data([trace1, trace2])
layout = {
  "geo": {"scope": "usa"}, 
  "enclos": }
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)