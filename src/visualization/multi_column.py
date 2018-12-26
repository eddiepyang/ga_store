import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff

final = pd.read_hdf('../../data/out/final.h5', 
                    parse_dates = ['date', 'visitStartTime'], 
                    dtype = {'fullvisitorId':int, 'transactionRevenue':int}
            )
#final.to_csv('../../data/out/final.csv')
final['log_transaction'] = np.log1p(final.transactionRevenue.astype(float))
final['transactionRevenue'] = final.transactionRevenue.astype(float)

# data variables
channel_x = final.channelGrouping.value_counts(normalize=True).index
channel_y = final.channelGrouping.value_counts(normalize=True)

# line chart
summary_time = final.groupby('date').transactionRevenue.sum()
summary_n = final.groupby('date').transactionRevenue.count()

def create_lines(x=pd.to_datetime(summary_time.index, format='%Y%m%d'), y=summary_time, 
                 x1=pd.to_datetime(summary_n.index, format='%Y%m%d'), y1=summary_n):
    
    data = go.Scatter(x=x , y=y, name='revenue')
    data1 = go.Scatter(x=x1 , y=y1, yaxis='y2', name='count')

    layout = go.Layout(
        title='Purchasing over time',
        yaxis=dict(
            title='revenues'
        ),
        yaxis2=dict(
            title='number of customers',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ))

    fig = go.Figure(data=[data, data1], layout=layout)
    return fig

# with __name__ app will read from assets folder 
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
                id='g1',
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
                    'layout': {
                        'title': 'Customer Sources'}
                        #'height': 800,
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
    ], className="five columns offset-by-part chart_div"),
   
        html.Div(#style = {'backgroundColor':'#D3D3D3'}, 
        children = [
            #html.H3('Column 2'),
            # dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]}),
            dcc.Graph(
        id='g2',
        figure={
            'data': [
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    
                    go.Histogram( x = final.transactionRevenue.dropna(), 
                    xbins=dict(start=0, end=10**9, size = 10000000), 
                    opacity = 0.7, marker={'color':'red'} 
                    )
                    ],
                    'layout': go.Layout(bargap=0.1, title= 'Revenue Distribution')
            #'layout': f1
        }, style={#"height": "95%", "width": "95%", 
                'display': 'inline-block', 
                'text-align': 'center',
                'padding':1},
           config={'displayModeBar': False} 
           
    )
        ], className="five columns chart_div"),
    ], className="row"),
    html.Div([

        html.Div(#[html.H4('Line chart'), 
        [dcc.Graph(id='g3', 
        figure=create_lines(),
        style={"height": "95%", "width": "95%", 
            'display': 'inline-block', 
            'text-align': 'center',
            'padding':1},
        config={'displayModeBar': False}
                )], 
        className="five columns offset-by-part chart_div"),

        html.Div(#[html.H4('Line chart'), 
        [dcc.Graph(id='g4', 
        figure = {'data': [go.Scatter(
    x = final.visitNumber.dropna(0).sample(1000, replace=True),
    y = final.log_transaction.dropna(0).sample(1000, replace=True),
    mode = 'markers'
        )],
        'layout': go.Layout(
            title = "Visit Count at Transaction",
            xaxis=dict(
                    range = [0,30]
                    )
        )},
                style={"height": "95%", "width": "95%", 
                    'padding':1,
                    'display': 'inline-block'},
                config={'displayModeBar': False}
                        )], 
                className="five columns chart_div"),
            ], className='row')

           
])

if __name__ == '__main__':
    app.run_server(debug=True)