import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# layout = go.Layout(
#     xaxis=dict(
#         showgrid=True,
#         zeroline=True,
#         showline=True,
#         mirror='ticks',
#         gridcolor='#bdbdbd',
#         gridwidth=2,
#         zerolinecolor='#969696',
#         zerolinewidth=4,
#         linecolor='#636363',
#         linewidth=6
#     ),
#     yaxis=dict(
#         showgrid=True,
#         zeroline=True,
#         showline=True,
#         mirror='ticks',
#         gridcolor='#bdbdbd',
#         gridwidth=2,
#         zerolinecolor='#969696',
#         zerolinewidth=4,
#         linecolor='#636363',
#         linewidth=6
#     )
# )

final = pd.read_hdf('../../data/out/final.h5', 
                    parse_dates = ['date', 'visitStartTime'], 
                    dtype = {'fullvisitorId':int, 'transactionRevenue':int}
            )

# data variables
channel_x = final.channelGrouping.value_counts(normalize=True).index
channel_y = final.channelGrouping.value_counts(normalize=True)

# chart layout dict

f1 = {
                'title': 'Dash Data Visualization',
                'height': 800,
                'width': 1200,
                'xaxis': dict(
                                showgrid=False,
                                zeroline=True,
                                showline=True,
                                mirror='ticks',
                                gridcolor='#bdbdbd',
                                gridwidth=1,
                                zerolinecolor='#969696',
                                zerolinewidth=2,
                                #linecolor='#636363',
                                #linecolor='#ADD8E6',
                                linecolor = '#B0B0B0',
                                linewidth=2
                             ),
                'yaxis': dict(
                                showgrid=True,
                                zeroline=True,
                                showline=True,
                                mirror='ticks',
                                gridcolor='#bdbdbd',
                                gridwidth=1,
                                zerolinecolor='#969696',
                                zerolinewidth=2,
                                #linecolor='#636363',
                                #linecolor= '#ADD8E6',
                                linecolor = '#B0B0B0',
                                linewidth=2)
            }

app.layout = html.Div(style={'padding':10}, 
children=[
    html.H1(children='Google store analytics',
            style = {'textAlign': 'center'}),

    
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    go.Histogram( x = final.transactionRevenue.dropna(), 
                    xbins=dict(start=0, end=10**9, size = 10000000), 
                    opacity = 0.7)
                     
                    
            ],
            'layout': f1
        }
    ),


    dcc.Graph(
        id='example-graph1',
        figure={
            'data': [go.Bar(
                    x=channel_x,
                    y=channel_y,
                    text=channel_y,
                    textposition = 'auto',
                    marker=dict(
                        color='rgb(158,202,225)',
                        line=dict(
                            color='rgb(8,48,107)',
                            width=1.5),
                    ),
                    opacity=0.6
                    )],
            'layout': {
                'title': 'Dash Data Visualization1',
                'height': 800,
                'width': 1200
                #'margin': dict(l=10, r=10, t=0, b=0)
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)