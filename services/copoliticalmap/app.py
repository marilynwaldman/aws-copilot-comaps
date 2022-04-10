import dash
from dash import dcc 
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import base64
import io
import numpy as np
from processdata import process_data, get_map_attributes

#initialize county polygons
filename = './co_counties_voters.geojson'
file=open(filename)
counties_gdf = gpd.read_file(file)

#create df that contains counties and lat/long for them
df_counties = counties_gdf[['LABEL', 'CENT_LAT', 'CENT_LONG']]

# create empty df to initialize map
df = pd.DataFrame()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,prevent_initial_callbacks=True)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map(df, counties_gdf):
    
    fig = go.Figure(go.Scattermapbox())
        
    if  not df.empty:
        lats, lons, labels, sizes, colors = get_map_attributes(df)

        fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = lons,
        lat = lats,
        text = labels,
        marker = {'size': sizes, 'color': colors},
        
        ))
    
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

    fig.update_traces(line=dict(width=3, color='black'))
    
    return fig

### The code that parses the file (from https://dash.plotly.com/dash-core-components/upload)
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


### clean data
    df_clean = process_data(df, df_counties)
    return df_clean
    



### the Decorator that updates the output when a file is dragged onto the web page
### (also from https://dash.plotly.com/dash-core-components/upload)

@app.callback(Output('map', 'figure'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),prevent_initial_call=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df_cleaned = [parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]    
        fig = plot_map(df_cleaned[0],counties_gdf)  
        return fig  
        


#figure = plot_map(df, counties_gdf)
app.layout = html.Div([
    dcc.Graph(id='map',
              figure=plot_map(df,counties_gdf)),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    #html.Div(id='output-data-upload'),
  ]
 )

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',port=port)
    app.run_server(debug=True, host="0.0.0.0", port=8050, use_reloader=False)
    

