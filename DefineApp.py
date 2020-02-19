#####################################################
#                    Define app                     #
#####################################################
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
import sqlite3

# Read input data for app
basemap = np.load('Data/basemap.npy', allow_pickle = True)
countries_data = [go.Scatter( x = poly[0], y = poly[1], mode = 'lines',
                            marker = dict (color='black')) for poly in basemap]

# Query database
con = sqlite3.connect("Database/database.sqlite")
df = pd.read_sql_query("SELECT * from TEMPTAB", con)
con.close()

# this is a pretty container for the layout
pretty_container={'border-radius': '5px', 'background-color': '#f9f9f9', 'margin': '10px', 'padding': '15px',
                  'position': 'relative', 'box-shadow': '2px 2px 2px lightgrey'}

app = dash.Dash(__name__,  assets_folder='Assets')

# Now we do html.Div (list of things) to setup the layout's elements
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(['this is the function that makes the title']),
            html.H2(['this is the title little brother'])
        ], style={'text-align': 'center'})
    ], className='row'),
    dcc.Tabs([
        dcc.Tab(label='Temperature', children=[
            html.Div([
            html.Div([
            html.Div([html.H3(['this is the title of a pretty graph'])],
                     className='row', style={'text-align': 'center'}),
            # html.Div for showing the map
            html.Div([dcc.Graph(id='raster')],className='row'),
        ], className='six columns'),
        # html.Div for showing the line-graph
        html.Div([
            html.Div([html.H3(['this is a tiny tiny little title for a raster'])], style={'text-align': 'center'}),
            dcc.Graph(id='line')
        ], className='five columns'),
        html.Div([
            html.Div([html.H5('Select the year')], className='row', style={'text-align': 'center'}),
            dcc.Slider(
                min=1948,
                max=2019,
                marks={i: '{}'.format(i) for i in range(1948, 2020, 5)},
                # we set the default value for the selected year in the slider
                value=2019,
                step=1,
                included=True,
                id='year_slider'
                )
            ],className='row', style={'margin': '15px'})
     ],className='row',style=pretty_container)
        ]),
        dcc.Tab(label='Precipitation', children=[
            html.Div([
                html.Div([
                    html.Div([html.H3(['this is the title of a pretty graph'])],
                             className='row', style={'text-align': 'center'}),
                    # html.Div for showing the map
                    html.Div([dcc.Graph(id='precip_raster')], className='row'),
                ], className='six columns'),
                # html.Div for showing the line-graph
                html.Div([
                    html.Div([html.H3(['this is a tiny tiny little title for a raster'])],
                             style={'text-align': 'center'}),
                    dcc.Graph(id='precip_line')
                ], className='five columns'),
                html.Div([
                    html.Div([html.H5('Select the year')], className='row', style={'text-align': 'center'}),
                    dcc.Slider(
                        min=1948,
                        max=2019,
                        marks={i: '{}'.format(i) for i in range(1948, 2020, 5)},
                        # we set the default value for the selected year in the slider
                        value=2019,
                        step=1,
                        included=True,
                        id='precip_year_slider'
                    )
                ], className='row', style={'margin': '15px'})
            ], className='row', style=pretty_container)
        ]),
        dcc.Tab(label='About', children=[
            html.Div([
                html.H1(['HERE WE CAN WRITE ABOUT US'])
            ])
        ]),
    ])
])


# first callback: temp map
@app.callback(Output('raster','figure'),
            [Input('year_slider', 'value')])
# defining the function that takes an year and creates a figure
def raster_plot(chosen_year):
    raster = df[df.year == chosen_year].sort_values(by=['lat', 'lon'], ascending=True).temp.to_numpy()
    raster = np.reshape(raster, (-1, 144))
    lon = df[df.year == chosen_year].lon.to_numpy()
    lon = np.unique(lon)
    lat = df[df.year == chosen_year].lat.to_numpy()
    lat = np.unique(lat)
    data = [go.Contour(
        z=raster,
        x=lon,
        y=lat,
        colorscale="RdBu",
        reversescale=True,
        zauto=False,  # Eventually we need to change this
        zmin=-35,  # WE NEED TO CHECK THIS!!
        zmax=35  # WE NEED TO CHECK THIS!!
    )]
    full_data = countries_data + data
    title = 'kinda hot'
    axis_style = dict(
        zeroline=False,
        showline=False,
        showgrid=False,
        ticks='',
        showticklabels=False,
    )
    layout = go.Layout(
        #title=title,
        showlegend=False,  # highlight closest point on hover
        xaxis=dict(
            axis_style,
            range=[lon[0], lon[-1]]  # restrict y-axis to range of lon
        ),
        yaxis=dict(
            axis_style,
        ),
        autosize=True,
        #width=1000,
        #height=500,
        margin = dict(l=0, b=50, r=0,t=50)
    )
    fig = go.Figure(data=full_data, layout=layout)
    return fig


# second callback: temp line-graph
@app.callback(Output('line','figure'),
              [Input('raster', 'clickData'), Input('year_slider', 'value')])
# setting a default chosen_year
def update_lines(clickData, chosen_year):
    if not clickData:
        chosen_lon, chosen_lat = -2.5, 37.5
    else:
        chosen_lon, chosen_lat = clickData['points'][0]['x'], clickData['points'][0]['y']
    plot_data = df[(df['lon'] == chosen_lon) & (df['lat'] == chosen_lat)]
    data = go.Scatter(x=plot_data['year'], y=plot_data['temp'])

    # adding x and y-axis
    layout = go.Layout(xaxis=dict(title='Years'), yaxis=dict(title='Average Yearly Air temperature ºC'),
                       template="plotly_white",margin = dict(l=0, b=50, r=0,t=50))
    fig = go.Figure(data=data,layout=layout)

    # adding layout
    fig.add_shape(
        go.layout.Shape(
            type="line",
            xref="x",
            yref="paper",
            x0=chosen_year,
            y0=0,
            x1=chosen_year,
            y1=1,
            fillcolor="tomato",
            opacity=0.5,
            layer="below",
            line_width=20
        )
    )

    return fig


@app.callback(Output('precip_raster','figure'),
            [Input('precip_year_slider', 'value')])
# defining the function that takes an year and creates a figure
def raster_plot(chosen_year):
    raster = df[df.year == chosen_year].sort_values(by=['lat', 'lon'], ascending=True).precip.to_numpy()
    raster = np.reshape(raster, (-1, 144))
    lon = df[df.year == chosen_year].lon.to_numpy()
    lon = np.unique(lon)
    lat = df[df.year == chosen_year].lat.to_numpy()
    lat = np.unique(lat)
    data = [go.Contour(
        z=raster,
        x=lon,
        y=lat,
        colorscale="haline",
        reversescale=True,
        #zauto=False,  # Eventually we need to change this
        #zmin=-35,  # WE NEED TO CHECK THIS!!
        #zmax=35  # WE NEED TO CHECK THIS!!
    )]
    full_data = countries_data + data
    title = 'kinda hot'
    axis_style = dict(
        zeroline=False,
        showline=False,
        showgrid=False,
        ticks='',
        showticklabels=False,
    )
    layout = go.Layout(
        #title=title,
        showlegend=False,  # highlight closest point on hover
        xaxis=dict(
            axis_style,
            range=[lon[0], lon[-1]]  # restrict y-axis to range of lon
        ),
        yaxis=dict(
            axis_style,
        ),
        autosize=True,
        #width=1000,
        #height=500,
        margin = dict(l=0, b=50, r=0,t=50)
    )
    fig = go.Figure(data=full_data, layout=layout)
    return fig


# second callback: temp line-graph
@app.callback(Output('precip_line','figure'),
              [Input('precip_raster', 'clickData'), Input('precip_year_slider', 'value')])
# setting a default chosen_year
def update_lines(clickData, chosen_year):
    if not clickData:
        chosen_lon, chosen_lat = -2.5, 37.5
    else:
        chosen_lon, chosen_lat = clickData['points'][0]['x'], clickData['points'][0]['y']
    plot_data = df[(df['lon'] == chosen_lon) & (df['lat'] == chosen_lat)]
    data = go.Scatter(x=plot_data['year'], y=plot_data['precip'])

    # adding x and y-axis
    layout = go.Layout(xaxis=dict(title='Years'), yaxis=dict(title='Average Yearly Precipitation'),
                       template="plotly_white",margin = dict(l=0, b=50, r=0,t=50))
    fig = go.Figure(data=data,layout=layout)

    # adding layout
    fig.add_shape(
        go.layout.Shape(
            type="line",
            xref="x",
            yref="paper",
            x0=chosen_year,
            y0=0,
            x1=chosen_year,
            y1=1,
            fillcolor="tomato",
            opacity=0.5,
            layer="below",
            line_width=20
        )
    )

    return fig



print('App ready to be run!')