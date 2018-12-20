import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

final = pd.read_hdf('../../data/out/final.h5', 
                    parse_dates = ['date', 'visitStartTime'], 
                    dtype = {'fullvisitorId':int, 'transactionRevenue':int}
            )


app.layout = html.Div(children=[
    html.H1(children='Google store analytics',
            style = {'textAlign': 'center'}),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    go.Histogram( x = final.transactionRevenue.dropna(), 
                    marker=dict(color='green'), opacity=0.75), 
                    
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)