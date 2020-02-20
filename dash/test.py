import pandas as pd
import numpy as np

import plotly.express as px
import cufflinks as cf

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

############################################################

listings = pd.read_pickle('../data/listings.pckl')
nei_stats = listings.groupby(['neighborhood','room_type']).describe()['price'].reset_index()
choice = ['Radius','Theta','Color']
col_options = [dict(label=x, value=x) for x in nei_stats.columns]

############################################################

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("Paris Airbnb analysis"),
        html.Div(
            [
                html.P(['Price statistics to show :', dcc.Dropdown(id = 'Radius', options = col_options[2:])]),
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%",'height' : '75%', "display": "inline-block"}),
    ]
)

@app.callback(Output("graph", "figure"), [Input('Radius', "value")])
def make_figure(Radius):
    return px.line_polar(
        nei_stats,
        r = Radius,
        theta = 'neighborhood',
        color = 'room_type',
        line_close = True,
        title = 'Price statistics per neighborhood for each room type'
    )

app.run_server(debug=True)
