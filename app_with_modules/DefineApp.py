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

# Read input data for app
basemap = np.load('Data/basemap.npy', allow_pickle = True)
countries_data = [go.Scatter( x = poly[0], y = poly[1], mode = 'lines',
                            marker = dict (color='black')) for poly in basemap]
df = pd.read_csv("Database/database.csv")

# this is just a pretty container and its kinda html
pretty_container={'border-radius': '5px', 'background-color': '#f9f9f9', 'margin': '10px', 'padding': '15px',
                  'position': 'relative', 'box-shadow': '2px 2px 2px lightgrey'}

app = dash.Dash(__name__,  assets_folder='Assets')

app.layout = html.Div([  # this html.Div is a list of things
    html.Div([
        html.H1(['this is the function that makes the title']),
        html.H2(['this is the title little brother'])
    ], style={'text-align': 'center'}),

    html.Div([
        html.Div([html.H3(['this is the title of a pretty graph'])], style={'text-align': 'center'}),
        html.Div([dcc.Graph(id='raster')]),

        html.Div([
            html.Div([html.H5('Select the year')], style={'text-align': 'center'}),

            dcc.Slider(
                min=1948,
                max=2019,
                marks={i: '{}'.format(i) for i in range(1948, 2020, 5)},  # this must be done very carefull)
                value=1990,  # value is the default value. So it means that the ball is gonna start at 2019
                step=1,  # value is the default value. So it means that the ball is gonna start at 2019
                included=True,
                # the "included = False" just means that the only thing that appears is a little ball. try with true
                id='year_slider'
            )
        ], style={'margin': '15px'})

    ], style=pretty_container),  # here we dont put brackers because pretty_container is a dictionary already

    html.Div([
        html.Div([html.H5(['this is a tiny tiny little title for a raster'])], style={'text-align': 'center'}),
        dcc.Graph(id='line')
    ], style=pretty_container)  # here we dont put brackers because pretty_container is a dictionary already
])


#this is the callback:
# (Output("Where it is  going to(the location)", "What is going").
# we answer those questions by using the ids of the components (thats why we have been putting them and thats why they have to be unique)
# we want our raster graph to go to the dcc.Graph called "raster"
# and what is going is a figure (a.k.a that plotly thing of data+layout)
# Input( where is it coming from, what is coming from)
# we want the value from the year_slider.
#the input is inside a list this way we can have multiple inputs
@app.callback(Output('raster','figure'),
            [Input('year_slider', 'value')])
#now we define a function that takes the year and create a figure. we put just one input:the chosen_year
def raster_plot(chosen_year): #and we copy all we did on jupyter
    raster = df[df.year == chosen_year].sort_values(by=['lat', 'lon'], ascending=True).Air.to_numpy()
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
        title=title,
        showlegend=False,  # highlight closest point on hover
        xaxis=dict(
            axis_style,
            range=[lon[0], lon[-1]]  # restrict y-axis to range of lon
        ),
        yaxis=dict(
            axis_style,
        ),
        autosize=False,
        width=1000,
        height=500,
        margin = dict(l=150, b=0, r=0)
    )
    fig = go.Figure(data=full_data, layout=layout)
    return fig

# now we define the call back and fucntion for the yearly graphs

@app.callback(Output('line','figure'),
              [Input('raster', 'clickData'), Input('year_slider', 'value')])
def update_lines(clickData, chosen_year): #here I write again the inputs. they can have different names compared to the previous line. but they must keep the order! so, chosen_year is 'value'. since dash already matches them, I dont need to define chosen year
    if not clickData:
        chosen_lon, chosen_lat = -2.5, 37.5
    else:
        chosen_lon, chosen_lat = clickData['points'][0]['x'], clickData['points'][0]['y']
    # we need to do something that checks is the user clicked on some value -> I get my output.
    # if the user still hasnt clicker -> than I get a predefined value
    plot_data = df[(df['lon'] == chosen_lon) & (df['lat'] == chosen_lat)]
    data = go.Scatter(x=plot_data['year'], y=plot_data['Air'])

    # this line adds an xaxis and a yaxis. we can change it
    layout = go.Layout(xaxis=dict(title='Years'), yaxis=dict(title='Average Yearly Air temperature ºC'),
                       template="plotly_white")

    fig = go.Figure(data=data,layout=layout)

    #now we add a pretty layout
    fig.add_shape(
        # Line reference to the axes
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

# this will run the application on debug mode and so we dont have to rerun it every time we make a change
# we just have to refresh the browser page

# 12.02.20
# we place the slider for the years, we create a call back and we style it a bit

print('App ready to be run!')