import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
from numpy import random
import colorlover as cl
import datetime as dt
import flask
import os
from pandas_datareader.data import DataReader
from keras.models import load_model
import time

import predict
import twitterAPI
from twitterAPI import stream
from twitterAPI import get_influence



################################################################################
# HELPERS
################################################################################



################################################################################
# PLOTS
################################################################################
#HR
def update_hr(showlegend=False):

    return   { 'data': [
                        { 'x': [1,2,3,4,5,6], 'y': np.random.uniform(low=150, high=250, size=(6,)),'type': 'line','name':'off campus'},
                        { 'x': [1,2,3,4,5,6], 'y': np.random.uniform(low=150, high=250, size=(6,)),'type': 'line','name':'on campus'}],
                'layout': {'title':'Half-Year Recruiting Cost','showlegend':showlegend},}

def update_op(showlegend=False):
    return  { 'data': [
                        { 'x': [1,2,3,4,5,6], 'y': np.random.uniform(low=1000, high=2250, size=(6,)),'type': 'bar','name':'network'},
                        { 'x': [1,2,3,4,5,6], 'y': np.random.uniform(low=1000, high=2250, size=(6,)),'type': 'bar','name':'resources'}],
                'layout': {'title':'Monthly Operation Cost','showlegend':showlegend}}

def update_fin(showlegend=False):
    df = pd.read_csv('DASH_datasets/GOOGfinancials.csv')
    x = df.year
    y1,y2,y3 = df['marketcap'],df['netdebt'],df['totalcapital']
    return { 'data': [
                           { 'x': x, 'y': y1,'type': 'line','name':'marketcap'},
                           { 'x': x, 'y': y2,'type': 'line','name':'netdebt'},
                           { 'x': x, 'y': y3,'type': 'line','name':'totalcapital'}],
                   'layout': {'title':'Past Financials','showlegend':showlegend}}



def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band


################################################################################
# APP INITIALIZATION
################################################################################


app = dash.Dash()

app.config['suppress_callback_exceptions']=True
app.css.append_css({ 'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

df_symbol = pd.read_csv('tickers.csv')

colorscale = cl.scales['9']['qual']['Paired']

external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

model = load_model('model.h5')
model.load_weights("weights.h5")    

################################################################################
# LAYOUT
################################################################################
app.layout = html.Div([
    html.Div(id='top-row',
        className='row',
        children = [dcc.Graph(id='hr',className='three columns',
                            figure= update_hr()),
                    dcc.Graph(id='go',className='three columns',
                                figure=update_op()),
                    dcc.Graph(id='fin',className='three columns',
                                figure= update_fin()) ,
                    html.Div(id='box',className='three columns',
                        children=[       
                                html.Img(src="http://s21644.pcdn.co/wp-content/uploads/2014/08/Twitter.png",height=25,width=25),
                                html.Div(id='t-container',children=['Twitter Live Feed'],style={'color': 'black', 'fontSize': 18}),
                                html.Div(id='twitter',style={'color': 'darkgrey', 'fontSize': 18})]
                                ),],
                    style={'marginBottom': 0, 'marginTop': 10,'marginLeft':0}),

    html.Div(id='second-row',
        className="row",
        children=[
            html.Div(id='second-row-first-col',
                className="four columns",
                children=html.Div([
                                html.Div([
                                    html.H6('Stock Ticker',
                                            style={'display': 'inline',
                                                   'float': 'left',
                                                   'margin-left': '7px',
                                                   'font-weight': 'bolder',
                                                   'font-family': 'Product Sans',
                                                   'color': "rgba(117, 117, 117, 0.95)",
                                                   }),
                                ]),
                                dcc.Dropdown(
                                    id='stock-ticker-input',
                                    options=[{'label': s[0], 'value': str(s[1])}
                                             for s in zip(df_symbol.Company, df_symbol.Symbol)],
                                    value=['GOOGL'],
                                    multi=True,
                                ),
                                html.Div(id='graphs')
                            ], className="container")
            ),
            html.Div(id='second-row-second-col',
                className="eight columns",
                children=[
                    html.Div(
                        children=[dcc.Graph(
                            id='center',
                            figure={
                                'data': [{
                                    'x': [1, 2, 3],
                                    'y': [3, 1, 2],
                                    'type': 'bar'
                                }],
                                'layout': {
                                    'height': 500,
                                    # 'margin': {
                                        # 'l': 10, 'b': 20, 't': 0, 'r': 0
                                    # }
                                }
                            }
                        ), html.Div(id= 'pred')]
                    ),
                dcc.Dropdown(
                        id='selector',
                        options=[
                            {'label': 'Human Resources', 'value': 'hr'},
                            {'label': 'Operation', 'value': 'op'},
                            {'label': 'Financials', 'value': 'fin'},
                        ],
                        value='fin'
                    ),
                dcc.Interval(id='tweet-update', interval=25000, n_intervals=0),
                dcc.Dropdown(
                        id='company-dropdown',
                        options=[
                            {'label': 'Apple', 'value': 'apple'},
                            {'label': 'Google', 'value': 'google'},
                            {'label': 'Facebook', 'value': 'facebook'},
                            {'label': 'Amazon', 'value': 'amazon'},
                            {'label': 'Motorola', 'value': 'motorola'},
                        ],
                        value='google'
                    ),
                html.Div(id = 'tweet-info',style={'display':'none'}),
                ]
            ),
        ]
    ),
])


################################################################################
# INTERACTION CALLBACKS
################################################################################

@app.callback(Output('center','figure'),
    [Input('selector','value')])
def update_center(value):
    fcns = {'hr':update_hr,'op':update_op,'fin':update_fin}
    return fcns[value](showlegend=True)

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value'),
    Input('company-dropdown','value')])
def update_graph(tickers,company):

    companies = {'apple':'AAPL','facebook':'FB','amazon':'AMZN',
    'google':'GOOGL','motorola':'MSI'}
    tickers = list(set([companies[company]]).union(set(tickers)) )

    graphs = []
    for i, ticker in enumerate(tickers):
        try:
            df = DataReader(str(ticker), 'morningstar',
                            dt.datetime(2017, 1, 1),
                            dt.datetime.now(),
                            retry_count=0).reset_index()
        except:
            graphs.append(html.H3(
                'Data is not available for {}, please retry later.'.format(ticker),
                style={'marginTop': 20, 'marginBottom': 20}
            ))
            continue

        candlestick = {
            'x': df['Date'],
            'open': df['Open'],
            'high': df['High'],
            'low': df['Low'],
            'close': df['Close'],
            'type': 'candlestick',
            'name': ticker,
            'legendgroup': ticker,
            'increasing': {'line': {'color': colorscale[0]}},
            'decreasing': {'line': {'color': colorscale[1]}}
        }
        bb_bands = bbands(df.Close)
        bollinger_traces = [{
            'x': df['Date'], 'y': y,
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
            'hoverinfo': 'none',
            'legendgroup': ticker,
            'showlegend': True if i == 0 else False,
            'name': '{} - bollinger bands'.format(ticker)
        } for i, y in enumerate(bb_bands)]
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data': [candlestick] + bollinger_traces,
                'layout': {
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))

    return graphs

@app.callback(Output('twitter', 'children'), 
    [Input('tweet-update', 'n_intervals'),
    Input('company-dropdown','value')])
def gen_tweet(interval,company):
    companies = {'apple':twitterAPI.apple,'facebook':twitterAPI.facebook,'amazon':twitterAPI.amazon,
    'google':twitterAPI.google,'motorola':twitterAPI.motorola}
    texts,tweets = twitterAPI.stream(companies[company],5)
    return [text+'\n' for text in texts]

@app.callback(Output('t-container', 'children'), 
    [Input('tweet-update', 'n_intervals'),
    Input('company-dropdown','value')],)
def gen_tweet(interval,company):
    return 'Twitter Live Feed'+' for ' + company.title()

@app.callback(Output('tweet-info', 'children'), 
    [Input('tweet-update', 'n_intervals'),
    Input('company-dropdown','value')],
    [State('tweet-info','children')])
def gen_tweet(interval,company,tweets_dict):
    if tweets_dict is None:
        tweets_dict = {'sentiment': 0,'count':0}
    else:
        tweets_dict = json.loads(tweets)
    companies = {'apple':twitterAPI.apple,'facebook':twitterAPI.facebook,'amazon':twitterAPI.amazon,
    'google':twitterAPI.google,'motorola':twitterAPI.motorola}
    texts,tweets = twitterAPI.stream(companies[company],5)

    influences = [get_influence(tweet) for tweet in tweets]
    influences = influences / np.linalg.norm(influences)
    tweets_dict['sentiment'] += np.multiply(influences,(predict.predict(model,texts)))
    tweets_dict['count'] += 5
    return json.dumps(tweets_dict)


@app.callback(Output('pred','children'),
    [Input('tweet-update','n_intervals'),
    Input('company-dropdown','value')],
    [State('tweet-info','children')])
def update_pred(interval,company,tweets_dict):
    if tweets_dict is None:
        tweets_dict = {'sentiment': 0,'count':0}
    else:
        tweets_dict = json.loads(tweets_dict)
    companies = {'apple':'AAPL','facebook':'FB' ,'amazon':'AMZN',
    'google':'GOOG','motorola':'MSI'} 
    df = pd.read_csv('STOCK/datasets/'+companies[company]+"_yearly.csv")
    for i,row in df.iterrows():
        if (row['stock_year_change']!= float(0) and row['close_on_up']!= float(0)):
            break
    stock_year_change  = row['stock_year_change']
    close_on_up = row['close_on_up']
    stock_change = "+{:.2%}".format(stock_year_change) if stock_year_change>=0 else "-{:.2%}".format(stock_year_change)
    close_on = "+{:.2%}".format(close_on_up) if close_on_up>=0 else "-{:.2%}".format(close_on_up)

    pred = "The company stock has changed by {} last year, and {} of the time \
    the stock closed higher than opened that day. Based on sentiment analysis from twitter feeds.\
    We believe the performance will likely change in this way:{}. ".format(stock_change,close_on,
        tweets_dict['sentiment'])


    return pred

if __name__ == '__main__':
    app.run_server(debug=True)
