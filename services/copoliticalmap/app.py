import dash
#import dash_html_components as html
#import dash_html_components as dbc
#import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html
from dash import dash_table
import dash_leaflet as dl
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import base64
import datetime
import io
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map():
    global fig # make fig global so it can be updated
    global counties_gdf # make global so it can be used in clean_data
    filename = './co_counties_voters.geojson'
    #filename = '/Users/arbetter/Coding/Streamlit/coloradovoters/co_counties_voters.geojson'
    file=open(filename)
    counties_gdf = gpd.read_file(file)

    print(counties_gdf.head(10))

    point = [-105, 40]

#   fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
#       mapbox={
#           "style":"open-street-map",
#           "zoom":7,
#           "layers":[
#               {
#                   "source": json.loads(counties_gdf.geometry.to_json()),
#                   "below":"traces",
#                   "type":"line",
#                   "color":"purple",
#                   "line":{"width": 1.5}
#               }
#           ],
#       },
#       margin={"l":0,"r":0,"t":0,"b":0},
#   )

    fig = go.Figure(data=go.scattermapbox(lat=[point[1]], lon=[point[0]]).update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom":7,
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
    ) )

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

    print ('parsing contents')

### update fig here
    print ('df',type(df))
    print (df.head(10))

### clean data
    df_clean = clean_data(df)

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
#           df_clean.to_dict('records'),
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def clean_data(df):
    global fig
### use dff because counties_df is global
    global counties_df # make global so it can be used in clean_data
    dff = counties_gdf.copy()
    df_clean = df.copy()

    print('cleaning data')

# fill missing with 0
    df_clean =df_clean.fillna(value='0',axis=1)

    for col in df_clean.columns:
        if (col != 'County'):
#remove commas from numbers
            df_clean[col] = df_clean[col].astype(str)
            df_clean[col] = df_clean[col].str.replace(',','')
            df_clean[col] = df_clean[col].astype(float)
            df_clean[col] = df_clean[col].astype(np.int64)

    for i in range(len(dff)):
        df_clean.at[i,'%Active']=100.*df_clean.at[i,'Total-Active']/df_clean.at[i,'Total']

#now updating df
    dff['Republicans']=0
    dff['Democrats']=0
    dff['Unaffiliated']=0
    dff['Max']=None
    dff['Total']=0


#    figure.update_traces(locations=dff,selector=dict(type='choropleth'))
#    figure.add_trace(go.Scatter,data=dff)

    partial = 0.75

    for c in dff['LABEL']:
        county_index = dff[dff['LABEL']==c].index[0]
        print('LABEL',county_index)
        voter_index = df_clean[df_clean['County']==c].index[0]
        print('Voter',voter_index)
        gop_total = df_clean.at[voter_index,'REP-Active']+df_clean.at[voter_index,'REP-Inactive']
        dff.at[county_index,'Republicans'] = gop_total
        dem_total = df_clean.at[voter_index,'DEM-Active']+df_clean.at[voter_index,'DEM-Inactive']
        dff.at[county_index,'Democrats'] = dem_total
        uaf_total = df_clean.at[voter_index,'UAF-Active']+df_clean.at[voter_index,'UAF-Inactive']
        dff.at[county_index,'Unaffiliated'] = uaf_total
        dff.at[county_index,'Total']=(gop_total + dem_total + uaf_total)/1000.

        if ((dff.at[county_index,'Unaffiliated'] > dff.at[county_index,'Democrats']) and \
            (dff.at[county_index,'Unaffiliated'] > dff.at[county_index,'Republicans'])):
            if (dff.at[county_index,'Democrats']/dff.at[county_index,'Unaffiliated'] > partial):
                dff.at[county_index,'Max']=1
            elif (dff.at[county_index,'Republicans']/dff.at[county_index,'Unaffiliated'] > partial):
                dff.at[county_index,'Max']=3
            else:
                dff.at[county_index,'Max']= 2
        elif ((dff.at[county_index,'Republicans'] > dff.at[county_index,'Democrats']) and \
            (dff.at[county_index,'Republicans'] > dff.at[county_index,'Unaffiliated'])):
            dff.at[county_index,'Max']= 4  
        elif ((dff.at[county_index,'Democrats'] > dff.at[county_index,'Unaffiliated']) and \
            (dff.at[county_index,'Democrats'] > dff.at[county_index,'Republicans'])):
            dff.at[county_index,'Max']= 0
        else:
            print('Error, no max found')
            exit()

    print(dff.columns)

# prepare data for plot
    lats = dff['CENT_LAT']
    lons = dff['CENT_LONG']
    sizes = dff['Total']
    for i in range(0,len(sizes)):
        sizes[i] = min(sizes[i],150)
        sizes[i] = max(10,sizes[i])
        print('s=',sizes[i])

    colors = []
    color_key = ["blue","lightblue","grey","pink","red"]
    for i in range(0,len(dff['Max'])):
        m = int(dff['Max'][i])
        print('i=',i,' m=',m,color_key[m])
        colors.append(color_key[m])

    labels = []
    reps = dff['Republicans'].astype(int).astype(str)
    uafs = dff['Unaffiliated'].astype(int).astype(str)
    dems = dff['Democrats'].astype(int).astype(str)
    for i in range(0,len(dff['LABEL'])):
        labels.append(dff['LABEL'][i] + '\nRep: '+reps[i] + '\nUAF: '+uafs[i]+'\nDems: '+dems[i])

    print('lat',type(lats),'lon',type(lons))

    fig.add_scattermapbox(lat=lats,lon=lons,mode='markers+text',text=labels,
                      marker_size=sizes,marker_color=colors, below='')

    fig.update_traces(line=dict(width=3, color='black'))

    df = dff.copy()
    return df_clean


### the Decorator that updates the output when a file is dragged onto the web page
### (also from https://dash.plotly.com/dash-core-components/upload)

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


figure = plot_map()
app.layout = html.Div(children=[html.H1(children='Colorado Counties'),
    dcc.Graph(id='map', figure=figure),
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
    html.Div(id='output-data-upload'),
  ]
 )

if __name__ == '__main__':
    app.run_server()

