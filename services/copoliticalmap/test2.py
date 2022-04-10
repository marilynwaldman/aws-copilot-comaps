#https://stackoverflow.com/questions/62558312/get-current-zoom-and-center-from-mapbox-in-dash

import dash
from dash import dcc 
from dash import html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import json

df2 = pd.DataFrame({'place_no': [1, 1, 1, 2, 2, 2],
                   'lat': [50.941357, 50.941357, 50.941357, 50.932171, 50.932171, 50.932171],
                   'lon': [6.957768, 6.957768, 6.957768, 6.964412, 6.964412, 6.964412],
                   'year': [2017, 2018, 2019, 2017, 2018, 2019],
                   'value': [20, 40, 60, 80, 60, 40]})
# initialize county polygons
filename = './co_counties_voters.geojson'
file=open(filename)
counties_gdf = gpd.read_file(file)
print(counties_gdf.head(10))

# create empty df to initialize map
df = pd.DataFrame()
#df['lat'] = [-105]
#df['lon'] = [40]

def get_map(df_map):

    fig = go.Figure(go.Scattermapbox())
    
    #fig = go.Figure(go.scattermapbox(lat=lat, lon=lon))
    fig.update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom": 5,
            "center" :  go.layout.mapbox.Center(lat= 38.9, lon=-106.06),
            "layers":[
                {
                    "source": json.loads(counties_gdf.geometry.to_json()),
                    "below":"traces",
                    "type":"line",
                    "color":"purple",
                    "line":{"width": 1.5}
                }
            ],
        },
        margin={"l":0,"r":0,"t":0,"b":0},
    ) 
    print(type(fig))
    return fig


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='map',
              figure=get_map(df)),
], )


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='year-picker', component_property='value')]
)
def update_map(selected_year):
    filtered_df = df[df['year'] == selected_year]
    fig = get_map(filtered_df)
    return fig


if __name__ == '__main__':
    app.run_server()