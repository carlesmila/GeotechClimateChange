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
df2 = pd.read_sql_query("SELECT * from FIXEDTAB", con)
con.close()

# Creating the layout
pretty_container={'border-radius': '5px', 'background-color': '#f9f9f9', 'margin': '10px', 'padding': '15px',
                  'position': 'relative', 'box-shadow': '2px 2px 2px lightgrey'}

app = dash.Dash(__name__,  assets_folder='Assets')

##Configuring Server
server=app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3(['Climate change explorer'])
        ], style={'text-align': 'center'})
    ], className='row'),
    dcc.Tabs([
        # Creating the layout for "Temperature"
        dcc.Tab(label='Temperature', children=[
            html.Div([
                html.Div([
                html.H5(['Select here the location and the year'])
                ], style={'text-align': 'center'}),
                html.Div([
                    html.Div([html.H6(' ')], className='row', style={'text-align': 'center'}),
                    dcc.Slider(
                        min=1948,
                        max=2019,
                        marks={i: '{}'.format(i) for i in range(1948, 2020, 5)},
                        value=2019,
                        step=1,
                        included=True,
                        id='year_slider'
                    )
                ], className='row', style={'margin': '35px'}),
                html.Div([
                    dcc.RadioItems(
                        id='temp_radio',
                        options=[
                            {'label': 'Temperature (°C)', 'value': 'temp'},
                            {'label': 'Difference from the baseline (°C)', 'value': 'tempanom'},
                        ],
                        value='temp',
                        labelStyle={'display': 'inline-block'},
                    )
                ], style={'text-align': 'center'}, className='six columns'),
                html.Div([
                    html.Div([
                    dcc.Graph(id='raster')],className='row')
                ], className='six columns'),

                html.Div([
                    html.Div([html.H3(id='location_temp')], style={'text-align': 'center'}),
                        dcc.Graph(id='line')
                ], className='five columns')
            ],className='row',style=pretty_container)
        ]),
        # Creating the layout for "Precipitable water"
        dcc.Tab(label='Precipitable water', children=[
            html.Div([
                html.Div([
                    html.H5(['Select here the location and the year'])
                ], style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.H5(' ')], className='row',
                    style={'text-align': 'center'}),
                    dcc.Slider(
                        min=1948,
                        max=2019,
                        marks={i: '{}'.format(i) for i in range(1948, 2020, 5)},
                        value=2019,
                        step=1,
                        included=True,
                        id='precip_year_slider'
                    )
                ], className='row', style={'margin': '15px'}),
                html.Div([
                    html.Div([
                        dcc.RadioItems(
                            id='precip_radio',
                            options=[
                            {'label': 'Precipitable water (kg/m^2)', 'value': 'precip'},
                            {'label': 'Difference from the baseline (kg/m^2)', 'value': 'precipanom'},
                            ],
                            value='precip',
                            labelStyle={'display': 'inline-block'}
                        )
                    ],style={'text-align': 'center'}),
                    html.Div([
                        dcc.Graph(id='precip_raster')],
                    className='row')
                ], className='six columns'),
                html.Div([
                    html.Div([
                        html.H3(id='location_precip')],
                    style={'text-align': 'center'}),
                        dcc.Graph(id='precip_line')
                ], className='five columns')
            ], className='row', style=pretty_container)
        ]),
        # Creating the layout for "About"
        dcc.Tab(label='About', children=[
            html.Div([
                 html.H4([dcc.Markdown('''
## **Implementing a GIS web app for climate change awareness**

According to the United Nations Intergovernmental Panel on Climate Change (IPCC), human-induced climate warming is estimated to be between 0.8°C and 1.2°C compared to pre-industrial levels (Allen et al, 2018). In spite of the severe consequences of climate change and its overwhelmingly scientific consensus, parts of the society still do not acknowledge its importance (Lee et al, 2015). We hypothesise that part of this issue is because a majority of the worldwide population do not have access to climate change reports, and so we think it is necessary to develop engaging solutions and tools to raise social awareness about climate change.


To answer this need, the objective of this project is to develop a webGIS portal to raise climate change awareness with the following capabilities:


* Spatiotemporal visualization of global temperature and precipitation data.
* Time series temperature and precipitation visualization of a user-selected location.



### App functionality
The Climate Change explorer app is structured in 3 tabs: temperature, precipitable water, and about. The temperature and precipitable water tabs consist of two side by side panels. In the left panel, the user can visualize the spatial distribution of the variable for a given year, or can otherwise select to visualize the difference with respect to the baseline level (mean values between 1948-1952). When clicking on a specific location on the map, the time series plot on the right is updated to the selected location, showing the country, climate area, temperature profile and moving average (7 years).



### Disclaimer

This project was done within the GPS group project class of the Master in Geospatial Technologies (Winter term 2019/2020) of the NOVA Information Management School of Lisbon by the students Carles Milà, Giulia Molisse and Pablo Cruz. This is therefore an educational exercise that would need further proofing in case the app were to be launched into the general public.

For more detailed information and documentation, check our [GitHub Repository](https://github.com/carlesmila/GeotechClimateChange).
''' )                    ])
            ])
        ]),
    ])
], style = {'background-color': '#f9f9f9'})



# Callback 1: temperature and variations from the baseline map
@app.callback(Output('raster','figure'),
            [Input('year_slider', 'value'), Input('temp_radio','value')])
# defining the function that takes an year and creates a figure
def raster_plot(chosen_year,mode):
    raster = df[df.year == chosen_year].sort_values(by=['lat', 'lon'], ascending=True)[mode].to_numpy()
    raster = np.reshape(raster, (-1, 144))
    lon = df[df.year == chosen_year].lon.to_numpy()
    lon = np.unique(lon)
    lat = df[df.year == chosen_year].lat.to_numpy()
    lat = np.unique(lat)
    if mode=='temp':
        cap = 50
    else:
        cap = 4
    data = [go.Contour(
        z=raster,
        x=lon,
        y=lat,
        colorscale="RdBu",
        reversescale=True,
        zauto=False,
        zmin=-cap,
        zmax=cap
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


# Callback 2: temperature line-graph
@app.callback([Output('line','figure'),Output('location_temp','children')],
              [Input('raster', 'clickData'), Input('year_slider', 'value')])
# Defining the function that takes location and year and outputs temperature line-graph, country and climate
def update_lines(clickData, chosen_year):
    if not clickData:
        chosen_lon, chosen_lat = -2.5, 37.5
    else:
        chosen_lon, chosen_lat = clickData['points'][0]['x'], clickData['points'][0]['y']
    plot_data = df[(df['lon'] == chosen_lon) & (df['lat'] == chosen_lat)]
    baseline = np.mean(plot_data['temp'][:5])*np.ones(len(plot_data['year']))
    data = [go.Scatter(x=plot_data['year'],
                       y=plot_data['temp'],
                       line=dict(color='royalblue',width=4),
                       legendgroup = "group",
                       name = "yearly average temperature (°C)",
                       mode = "lines",
                       ),
            go.Scatter(x=plot_data['year'],
                       y=plot_data['temp'].rolling(7,center=True).mean(),#rolling average (trende line for non linear data)
                       line=dict(color='firebrick',width=4),
                       legendgroup = "group",
                       name = "rolling average temperature (°C)",
                       mode = "lines",
                       ),
            go.Scatter(x=plot_data['year'],
                       y=baseline,
                       line=dict(color='black',dash='dash'),
                       legendgroup = "group",
                       name = "baseline temperature (°C)",
                       mode = "lines",
                       )] #baseline
    # adding x and y-axis
    layout = go.Layout(
        xaxis=dict(title='Years'),
        yaxis=dict(title=' '),
        template="plotly_white",
        margin = dict(l=0, b=50, r=0,t=50),
        showlegend=True)
    fig = go.Figure(data=data,layout=layout)
    fig.update_layout(legend_orientation="h")


    names = df2[(df2['lon'] == chosen_lon) & (df2['lat'] == chosen_lat)]
    query = f'{names.countryname.values[0]}, {names.climate.values[0]}'

    return fig, query


# Callback 3: moisture and variation from the baseline map
@app.callback(Output('precip_raster','figure'),
            [Input('precip_year_slider', 'value'),Input('precip_radio','value')])
# Defining the function that takes an year and creates a figure
def raster_plot(chosen_year,mode):
    raster = df[df.year == chosen_year].sort_values(by=['lat', 'lon'], ascending=True)[mode].to_numpy()
    raster = np.reshape(raster, (-1, 144))
    lon = df[df.year == chosen_year].lon.to_numpy()
    lon = np.unique(lon)
    lat = df[df.year == chosen_year].lat.to_numpy()
    lat = np.unique(lat)
    if mode=='precip':
        capmax = 700
        capmin = 0
    else:
        capmax = 150
        capmin = - 150
    data = [go.Contour(
        z=raster,
        x=lon,
        y=lat,
        colorscale="haline",
        reversescale=True,
        #zauto=False,  # Eventually we need to change this
        zmin=capmin,  # WE NEED TO CHECK THIS!!
        zmax=capmax  # WE NEED TO CHECK THIS!!
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


# Callback 4: moisture line-graph
@app.callback([Output('precip_line','figure'),Output('location_precip','children')],
              [Input('precip_raster', 'clickData'), Input('precip_year_slider', 'value')])
# Defining the function that takes location and year and outputs precipitable water line-graph, country and climate
def update_lines(clickData, chosen_year):
    if not clickData:
        chosen_lon, chosen_lat = -2.5, 37.5
    else:
        chosen_lon, chosen_lat = clickData['points'][0]['x'], clickData['points'][0]['y']
    plot_data = df[(df['lon'] == chosen_lon) & (df['lat'] == chosen_lat)]
    baseline = np.mean(plot_data['precip'][:5]) * np.ones(len(plot_data['year']))
    data = [go.Scatter(x=plot_data['year'],
                       y=plot_data['precip'],
                       line=dict(color='royalblue', width=4),
                       legendgroup = "group",
                       name = "yearly sum precipitable water (kg/m^2)",
                       mode = "lines"
            ),
            go.Scatter(x=plot_data['year'],
                       y=plot_data['precip'].rolling(7, center=True).mean(),
                       # rolling average (trend line for non linear data)
                       line=dict(color='#F96D15', width=4),
                       legendgroup = "group",
                       name = "rolling average precipitable water (kg/m^2)",
                       mode = "lines"),
            go.Scatter(x=plot_data['year'],
                       y=baseline,
                       line=dict(color='black', dash='dash'),
                       legendgroup = "group",
                       name = "baseline precipitable water (kg/m^2)",
                       mode = "lines")]  # baseline
    # adding x and y-axis
    layout = go.Layout(xaxis=dict(title='Years'), yaxis=dict(title='Average Yearly Precipitable (mm)'),
                       template="plotly_white", margin=dict(l=0, b=50, r=0, t=50), showlegend=True)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(legend_orientation="h")

    names = df2[(df2['lon'] == chosen_lon) & (df2['lat'] == chosen_lat)]
    query = f'{names.countryname.values[0]}, {names.climate.values[0]}'

    return fig, query



print('App ready to be run!')
