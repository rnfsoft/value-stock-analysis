from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import settings
import stock_info
from dash.dependencies import Input, Output
from future_value import get_future_value
from pandas_datareader import data as web
from stock_evaluation import get_stock_evaluation
from stock_list import combine_stock_list

BULL_LOGO = "static/img/bull.png"
BEAR_LOGO = "static/img/bear.png"

start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()
stocks = combine_stock_list()

navbar = dbc.Navbar(
   [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=BULL_LOGO, height="40px")),
                    dbc.Col(dbc.NavbarBrand("VALUE STOCK ANALYSIS", className="ml-2")),
                    dbc.Col(html.Img(src=BEAR_LOGO, height="40px")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="#",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5('Choose a Stock'),
                        dcc.Dropdown(
                            id='stock-list',
                            options= stocks,
                            value='GOOG'
                        ),
                        html.Br(),
                        html.H5('Select a Date Range'),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=datetime(start_date.year,start_date.month,start_date.day),
                            end_date=datetime(end_date.year,end_date.month,end_date.day),
                            calendar_orientation='vertical',
                        ),
                        dcc.Graph(id='stock-graph'),
         
                        html.Div(id='financial-reports'),
                        html.H5('Stock Evaluation'),
                        html.Div(id='stock-evaluation'),
                        html.Br(),
                        
                        html.H5('Future/Current Value and Recommendation'),
                        html.Div(id='future-value'),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    static_folder='static',
    csrf_protect=False
    )

server = app.server

app.title = 'Value Stock Analysis'
app.layout = html.Div([navbar, body])

@app.callback(Output('stock-graph', 'figure'), 
                [
                    Input('stock-list', 'value'), 
                    Input('date-picker-range', 'start_date'), 
                    Input('date-picker-range', 'end_date')
                ])

def update_graph(symbol, start_date, end_date):
    stock_prices = web.DataReader(symbol, data_source='yahoo', start=start_date, end=end_date)

    adj_close = go.Scatter(
        x = stock_prices.index,
        y = stock_prices['Adj Close'],
        name = 'Adj Close'
    )
    exp_20_days = go.Scatter(
        x = stock_prices.index,
        y = stock_prices['Adj Close'].ewm(span=20, adjust=False).mean(),
        name = '20 Days EMA'
    )
    exp_50_days = go.Scatter(
        x = stock_prices.index,
        y = stock_prices['Adj Close'].ewm(span=50, adjust=False).mean(),
        name = '50 Days EMA'
    )
    

    data = [adj_close, exp_20_days, exp_50_days]
    
    layout = go.Layout(
        yaxis=dict(
            title='Adj Close'
        ),
    )
    return{
        'data': data,
        'layout': layout
    }

@app.callback(Output('financial-reports', 'children'), [Input('stock-list', 'value')])
def update_table(symbol):
    stock_info.get_stock_info(symbol)
    df_financial_reports = stock_info.combine_financial_reports()
    df_financial_reports = df_financial_reports.loc[:, ~df_financial_reports.columns.str.contains('^Unnamed')]
    return dbc.Table.from_dataframe(df_financial_reports, striped=True, bordered=True, hover=False, index=True)

@app.callback(Output('stock-evaluation', 'children'), [Input('financial-reports', 'children')])
def update_table(symbol):
    evaluations = get_stock_evaluation()

    if(any(evaluations)): # if any reason exists
        return html.Span(
            html.H5(
                [
                    dbc.Badge(evaluation, pill=True, color="danger", className="mr-1") for evaluation in evaluations
                ]
            )
        )
    else:
        return html.H5(dbc.Badge("GOOD", pill=True, color="success", className="mr-1"))

@app.callback(Output('future-value', 'children'), [Input('financial-reports', 'children')])
def update_table(symbol):
    future_value = get_future_value()
    return dbc.Table.from_dataframe(future_value, striped=True, bordered=True, hover=False, index=True)

if __name__ == '__main__':
    app.run_server(debug=True)
