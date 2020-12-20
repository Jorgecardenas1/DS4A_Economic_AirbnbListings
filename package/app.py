# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import flask
import dash
import base64
import datetime
import io
import pandas as pd



ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)

app = dash.Dash(__name__,server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_csv('base_dataframe.csv')
fig = px.bar(df, x="state", y="count", barmode="group")
regression_coefficients = {'intercept':0.0551,'gdp_coeff':-43.3776,'ur_coeff':-0.7716,'income_coeff':54.4809}


app.layout = html.Div(children=[

    html.Div(
    [
        dbc.Row(
            dbc.Col([
                html.H1(children='Listings Framework'),
                html.Div(children='''
                    DS4A / Team7.
                '''),
            ],
             width="auto"
            ),
            style={
                'margin-left' : '0px',
                'background' : '#FF5A5F',
                'color' : '#FFFFFF',
            },
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Graph(
                        id='example-graph',
                        figure=fig
                    ),
                    ],
                    md=6,
                    style={
                        'margin-left' : '1px',
                    },
                ),
                dbc.Col([
                    dbc.CardGroup([
                        
                        dbc.Card([
                            dbc.Label("GDP (% change)",
                                style={
                                    "margin-left": "5px",
                                    "margin-right": "5px",
                                    'font-weight': 'bold'

                                }
                                
                            ),

                            dcc.Input(
                                placeholder='(%)',
                                type='number',
                                value='',
                                size="md", 
                                className="mb-3",
                                id="GDP",
                                style={
                                    "margin-left": "5px",
                                    "margin-right": "5px"

                                }
                            ),
                            html.Br(),
                            dbc.Label("Personal Income (% change)",
                                style={
                                        "margin-left": "5px",
                                        "margin-right": "5px",
                                        'font-weight': 'bold'

                                }),

                            dcc.Input(
                                placeholder='(%)',
                                type='number',
                                value='',
                                size="md",
                                id="PI",
                                className="mb-3",
                                style={
                                    "margin-left": "5px",
                                    "margin-right": "5px"

                                }

                            ),
                            html.Br(),
                            dbc.Label("Unemployment Rate (% change)",
                                style={
                                        "margin-left": "5px",
                                        "margin-right": "5px",
                                        'font-weight': 'bold'

                                }
                            ),

                            dcc.Input(
                                placeholder='(%)',
                                type='number',
                                value='',
                                size="md", 
                                id="UR",
                                className="mb-3",
                                style={
                                    "margin-left": "5px",
                                    "margin-right": "5px"

                                }
                            ),
                            html.Br(),
                        ],
                        style={"width": "15rem",'padding_all':'10px'},

                    ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4("Listings Variations", className="card-title"),
                                html.H2(children='',id="Listings",
                            
                                ),
                                
                            ],                            
                        ),
                        color="info", inverse=True,

                    ),
                ]),
            ],
                style={"width": "10rem",'padding_all':'10px'},
                className="md-4",
                align="center",
            ),
        ]),

    ])
])
@app.callback(
    Output("Listings", "children"),
    Input("GDP", "value"),
    Input("PI", "value"),
    Input("UR", "value"),

)
#def cb_render(*vals):
#    return " | ".join((str(val) for val in vals if val))

def update_Listings(GDP, PI, UR):
    personal_income = 0
    personal_income = (regression_coefficients['intercept'] + regression_coefficients['gdp_coeff'] * GDP + regression_coefficients['ur_coeff'] * UR + regression_coefficients['income_coeff'] * PI)
    
    #return u'Input 1 {} and Input 2 {}'.format(GDP, PI)
    return u'{} '.format(personal_income)



if __name__ == '__main__':
   #app.run_server(debug=True)
    
    app.run_server(host='0.0.0.0',port=8080, debug=False)