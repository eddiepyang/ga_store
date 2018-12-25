import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go


final = pd.read_hdf('../../data/out/final.h5', 
                    parse_dates = ['date', 'visitStartTime'], 
                    dtype = {'fullvisitorId':int, 'transactionRevenue':int}
            )

# data variables
channel_x = final.channelGrouping.value_counts(normalize=True).index
channel_y = final.channelGrouping.value_counts(normalize=True)


app = dash.Dash(__name__)  # the name of the folder containing your code and static folder.
# app.css.append_css({'external_url': '/static/reset.css'})
# app.server.static_folder = 'static'
#@app.serve_route('') 
#app = dash.Dash()

# start of app
app.layout = html.Div( 
children = [html.Div([
                    html.Span('Google store charts', style={'textAlign': 'center'}, 
                        className='app-title')], 
                    className = 'row header'), 
html.Div(#style = {'backgroundColor':'#D3D3D3'},
    children = [html.Div([
            #html.H3('Google store charts'),
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
                                    width=1),
                            ),
                            opacity=0.6
                            )],
                    # 'layout': {
                    #     'title': 'Dash Data Visualization1',
                    #     #'height': 800,
                    #     #'width': 1200
                    #     #'margin': dict(l=10, r=10, t=0, b=0)
                    #             }
                    }, 
                style={"height": "95%", 
                "width": "95%", 
                'display': 'inline-block', 
                'text-align': 'center', 
                'padding': 1},
                config={'displayModeBar': False}
                )
    ], className="five columns offset-by-halfed chart_div"),
   
        html.Div(#style = {'backgroundColor':'#D3D3D3'}, 
        children = [
            #html.H3('Column 2'),
            # dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]}),
            dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    
                    go.Histogram( x = final.transactionRevenue.dropna(), 
                    xbins=dict(start=0, end=10**9, size = 10000000), 
                    opacity = 0.7, marker={'color':'red'} 
                    )
                    ],
                    'layout': go.Layout(bargap=0.1)
            #'layout': f1
        }, style={#"height": "95%", "width": "95%", 
                'display': 'inline-block', 
                'text-align': 'center',
                'padding':1},
           config={'displayModeBar': False} 
           
    )
        ], className="five columns chart_div"),
    ], className="row"),
    
        html.Div([html.H4('Line chart'), dcc.Graph(id='g3', 
        figure={'data': [{'y': [1, 2, 3]}]},
        style={"height": "95%", "width": "95%", 
            'display': 'inline-block', 
            'text-align': 'center',
            'padding':1},
        config={'displayModeBar': False}
                )], 
        className="five columns offset-by-halfed chart_div ")
        
])

if __name__ == '__main__':
    app.run_server(debug=True)