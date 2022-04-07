import dash
from dash import dcc 
from dash import html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({'place_no': [1, 1, 1, 2, 2, 2],
                   'lat': [50.941357, 50.941357, 50.941357, 50.932171, 50.932171, 50.932171],
                   'lon': [6.957768, 6.957768, 6.957768, 6.964412, 6.964412, 6.964412],
                   'year': [2017, 2018, 2019, 2017, 2018, 2019],
                   'value': [20, 40, 60, 80, 60, 40]})


def get_map(df_map):
    fig = go.Figure(go.Scattermapbox(
        lat=df_map['lat'],
        lon=df_map['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=df_map['value']
        ),
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox={'center': go.layout.mapbox.Center(lat=50.936600, lon=6.961497), 'zoom': 11}
    )
    return fig


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='map',
              figure=get_map(df[df['year'] == 2017])),
    dcc.Slider(id='year-picker',
               min=2017,
               max=2019,
               marks={2017: {'label': 2017}, 2018: {'label': 2018}, 2019: {'label': 2019}}
               ),
    html.Div(id='shown-week', style={'textAlign': 'center'})
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