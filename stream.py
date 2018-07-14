import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from scipy.stats import rayleigh
import numpy as np
import pandas as pd
import os
import datetime as dt
import twitterAPI

app = dash.Dash()
server = app.server
app.layout = html.Div([

    html.Div([
           html.Div(id='text'),
    dcc.Interval(id='tweet-update', interval=1000, n_intervals=0),
    ], className='row'),
])

@app.callback(Output('text', 'children'), [Input('tweet-update', 'n_intervals')])
def gen_tweet(interval):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    # twitterAPI.stream(twitterAPI.apple,10000)
    return  twitterAPI.stream(twitterAPI.apple,10000)


if __name__ == '__main__':
    app.run_server()