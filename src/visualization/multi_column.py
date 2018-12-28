import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff

final = pd.read_csv('https://raw.githubusercontent.com/eddiepyang/ga_store/master/data/out/final.csv', 
                    parse_dates = ['date', 'visitStartTime'], 
                    dtype = {'fullvisitorId':int, 'transactionRevenue':int}
        )

final['log_transaction'] = np.log1p(final.transactionRevenue.astype(float))
final['transactionRevenue'] = final.transactionRevenue.astype(float)

# data variables
channel_x = final.channelGrouping.value_counts(normalize=True).index
channel_y = final.channelGrouping.value_counts(normalize=True)

# line chart
summary_time = final.groupby('date').transactionRevenue.sum()
summary_n = final.groupby('date').transactionRevenue.count()
    
s1 = {"height": "95%", "width": "95%", 
                    'display': 'inline-block', 
                    'text-align': 'center', 
                    'padding': 1}

# with __name__ app will read from assets folder 
app = dash.Dash(__name__)  

# calls flask server for deployment
server=app.server

# start of main program
app.layout = html.Div( 
    children = [html.Div([
    
    # header
    html.Span('Google store charts', style={'textAlign': 'center'}, 
    className='app-title')], 
    className = 'row header'), 

    # dropdown menu
    html.Div([
        html.Div([
            dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in final.country.unique()],
                        value='United States')], 
        style = {'display': 'inline-block', 'float': 'left'},
        className= 'five columns offset-by-part chart_div'),

        html.Div(
            dcc.RangeSlider(id ='count range',
                        min = 0,
                        max = 100,
                        step = 10,
                        marks = {i*10:f'{i*10}' for i in range(11)},
                        value = [0,60]),
        style = {'display': 'inline-block', 'float': 'bottom'},
        className = 'five columns chart_div')],

    className = 'row'),

    # row 1
    html.Div([
        
        html.Div([
        
        dcc.Graph(id='g1',
        style=s1,
        config={'displayModeBar': False}
        )], 
        className="five columns offset-by-part chart_div"),
    
    html.Div( 
        [dcc.Graph(id='g2', 
                style=s1,
                config={'displayModeBar': False}
                        )], 
                className="five columns chart_div"),
    ], className='row'),
                            
    # row 2
    html.Div(
        children = [html.Div([
                #html.H3('Google store charts'),
                dcc.Graph(
                    id='g3',
                    figure={
                        'data': [go.Bar(
                                x=channel_x,
                                y=channel_y,
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
                        }, 
                    style=s1,
                    config={'displayModeBar': False}
                    )
        ], className="five columns offset-by-part chart_div"),
    
            html.Div( 
            children = [
                dcc.Graph(
                id='g4',
                figure={
                    'data': [
                            go.Histogram( x = final.transactionRevenue.dropna(), 
                            xbins=dict(start=0, end=10**9, size = 10000000), 
                            opacity = 0.7, marker={'color':'red'} 
                            )
                    ],
                            'layout': go.Layout(bargap=0.1, title= 'Revenue Distribution')
                }, 
            style=s1,
            config={'displayModeBar': False} 
            
                )
            ], className="five columns chart_div"),
        ], className="row")
])

# callbacks
@app.callback(
    dash.dependencies.Output('g1', 'figure'),
    [dash.dependencies.Input('yaxis-column', 'value')]
)

def create_lines(country):
    
    df = final.loc[final.country == country]
    
    summary_time = df.groupby('date').transactionRevenue.sum()
    summary_n = df.groupby('date').transactionRevenue.count()
    
    x=pd.to_datetime(summary_time.index, format='%Y%m%d') 
    y=summary_time
    x1=pd.to_datetime(summary_n.index, format='%Y%m%d')
    y1=summary_n
        
    data = go.Scatter(x=x , y=y, name='revenue')
    data1 = go.Scatter(x=x1 , y=y1, yaxis='y2', name='count')

    layout = go.Layout(
        title='Purchasing over time from ' + country,
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


@app.callback(
    dash.dependencies.Output(component_id='g2', component_property='figure'),
    [dash.dependencies.Input(component_id='count range', component_property='value')]
)


def create_scatter(rng):
    
    final['transactionRevenue'] = final.transactionRevenue.astype(float)
    num_visits = final.groupby('fullVisitorId').visitNumber.max()
    user_revenue = np.log(final[['fullVisitorId', 'transactionRevenue']].dropna().groupby('fullVisitorId').transactionRevenue.sum())
    res = pd.concat([num_visits, user_revenue], axis=1).dropna()

    # Create a trace
    trace = go.Scatter(
        x = res.visitNumber,
        y = res.transactionRevenue,
        mode = 'markers'
    )

    layout = go.Layout(title = 'Revenue by Visit',
        xaxis = {'title': 'Visit Count',
                'range': rng
               },
        yaxis = {'title': 'Log Transaction'
                }
    )
    
    data = [trace]

    return go.Figure(data, layout)



if __name__ == '__main__':
    app.run_server(debug=True)
