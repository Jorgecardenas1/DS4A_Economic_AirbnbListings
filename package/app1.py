from package import app
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import flask
import base64
import datetime
import io

#app = dash.Dash(__name__)
#server = flask.Flask(__name__)
#app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
#app.title = 'AirBLocuras- DS4A/Team7'

regression_coefficients = {'intercept':0.0551,'gdp_coeff':-43.3776,'ur_coeff':-0.7716,'income_coeff':54.4809}

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
base_df = pd.read_csv('/root/ds4a/ds4a/base_dataframe.csv')
base_df = base_df.drop('Unnamed: 0',axis=1)
#base_df = base_df.groupby(['quarter', 'state']).sum()
quarters = base_df['quarter'].unique()
states = base_df['state'].unique()
states_dict = [
    {"label": 'All states', "value": 'All states'},
    {'label': 'CA - California', 'value': 'CA'}, 
    {'label': 'CO - Colorado', 'value': 'CO'}, 
    {'label': 'DC - District of Columbia', 'value': 'DC'}, 
    {'label': 'IL - Illinois', 'value': 'IL'}, 
    {'label': 'LA - Louisiana', 'value': 'LA'}, 
    {'label': 'MA - Massachusetts', 'value': 'MA'}, 
    {'label': 'MN - Minnesota', 'value': 'MN'}, 
    {'label': 'NC - North Carolina', 'value': 'NC'}, 
    {'label': 'NY - New York', 'value': 'NY'}, 
    {'label': 'OR - Oregon', 'value': 'OR'}, 
    {'label': 'TN - Tennessee', 'value': 'TN'}, 
    {'label': 'TX - Texas', 'value': 'TX'} 
]
#[states_dict.append({"label": state, "value": state}) for state in states]
quarters_dict = []
[quarters_dict.append({"label": quarter, "value": quarter}) for quarter in quarters]
quarters_dict_slider = {
    0: {'label': '2018Q2'},
    1: {'label': '2018Q3'},
    2: {'label': '2018Q4'},
    3: {'label': '2019Q1'},
    4: {'label': '2019Q2'},
    5: {'label': '2019Q3'},
    6: {'label': '2019Q4'},
    7: {'label': '2020Q1'},
    8: {'label': '2020Q2'}
}
logo_filename = '/root/ds4a/ds4a/logo.png' # replace with your own image
logo_encoded = base64.b64encode(open(logo_filename, 'rb').read())
correlationOne_filename = '/root/ds4a/ds4a/correlationOne.jpeg' # replace with your own image
correlationOne_encoded = base64.b64encode(open(correlationOne_filename, 'rb').read())
ds4a_filename = '/root/ds4a/ds4a/ds4a.jpg' # replace with your own image
ds4a_encoded = base64.b64encode(open(ds4a_filename, 'rb').read())
mintic_filename = '/root/ds4a/ds4a/mintic.jpeg' # replace with your own image
mintic_encoded = base64.b64encode(open(mintic_filename, 'rb').read())

#print(states_dict)
#print(quarters_dict)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dbc.Row([
        # dbc.Col([
        #     html.Div(id='title_container', children=[
        #         #html.H1("Listings in Airbnb", style={'text-align': 'center', 'font-family': 'verdana', 'color': 'rgb(42, 63, 95)'}),
        #     ]),
        # ],
        #     width="auto"
        # ),
        dbc.Col([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(logo_encoded.decode()), height=50)
            ]),
        ],
            width=3,
            align='center'
        ),
        dbc.Col([
            html.Div(children='''
                DS4A / Team7.
            '''),
        ],
            width=3,
            align='center',
            style={'font-weight': 'bold'}
        ),
        dbc.Col([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(correlationOne_encoded.decode()), height=50)
            ]),
        ],
            width=2,
            align='center'
        ),
        dbc.Col([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(ds4a_encoded.decode()), height=50)
            ]),
        ],
            width=1,
            align='center'
        ),
        dbc.Col([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(mintic_encoded.decode()), height=50)
            ]),
        ],
            width=2,
            align='center'
        )],
        style={
            'margin-left' : '0px',
            'margin-right' : '0px',
            'background' : '#FFFFFF',
            'color' : '#FF5A5F',
            'padding-left': '100px',
            'padding-right': '100px'
        },
        justify='start',
    ),
    
    html.Hr(),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("State", style={'text-align': 'center', 'font-weight': 'bold', 'color': 'rgb(42, 63, 95)'}),
                    dcc.Dropdown(
                        id="slct_states",
                        options=states_dict,
                        multi=False,
                        value='All states',
                        #style={'width': "40%"}
                    ),
                ])
            ], width=3),
            dbc.Col([
                html.Div([
                    html.Div("Quarter", style={'text-align': 'center', 'font-weight': 'bold', 'color': 'rgb(42, 63, 95)'}),
                    dcc.Slider(
                        id='quarter_slider',
                        min=0,
                        max=8,
                        value=0,
                        marks=quarters_dict_slider
                    ),
                ])
            ], width=7),
        ], justify='center')
    ]),
        
    html.Br(),
    
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='first_graph', figure={})
            ], width=5),
            dbc.Col([
                #html.Div("Selected state", style={'text-align': 'center', 'font-family': 'verdana', 'color': 'rgb(42, 63, 95)'}),
                dcc.Graph(id='second_graph', figure={}),
                dcc.Graph(id='third_graph', figure={})
            ], width=5)
        ], no_gutters=True, justify='center')
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label("GDP (% change)",
                style={
                    "margin-left": "5px",
                    "margin-right": "5px",
                    'font-weight': 'bold'
                }
            ),

            dcc.Input(
                placeholder='(0.1)',
                type='number',
                value=1,
                size="md", 
                className="mb-3",
                id="GDP",
                min=-100,
                max=100,
                step=0.1,
                style={
                    "margin-left": "5px",
                    "margin-right": "5px"
                }
            ),
        ],
            width=2
        ),

        dbc.Col([
            dbc.Label(
                "Personal Income (% change)",
                style={
                    "margin-left": "5px",
                    "margin-right": "5px",
                    'font-weight': 'bold'
                }
            ),

            dcc.Input(
                placeholder='(0.1)',
                type='number',
                value=1,
                size="md",
                id="PI",
                className="mb-3",
                min=-100,
                max=100,
                step=0.1,
                style={
                    "margin-left": "5px",
                    "margin-right": "5px"
                }
            ),
        ],
            width=3,
        ),

        dbc.Col([
            dbc.Label(
                "Unemployment Rate (% change)",
                style={
                    "margin-left": "5px",
                    "margin-right": "5px",
                    'font-weight': 'bold'
                }
            ),

            dcc.Input(
                placeholder='(0.1)',
                type='number',
                value=1,
                size="md", 
                min=-100,
                max=100,
                id="UR",
                step=0.1,
                className="mb-3",
                style={
                    "margin-left": "5px",
                    "margin-right": "5px"
                }
            ),
        ],
            width=3,
        ),

        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Listings Variations", className="card-title"),
                        html.H2(children='',id="Listings",),
                    ],                            
                ),
                color="info", inverse=True,
            ),
        ],
            width=4,
        )],
        style={
            'margin-left' : '0px',
            'background' : '#FF5A5F',
            'color' : '#FFFFFF',
            'padding-left': '100px',
        },
        align='center',
        justify='center'
    ),
], style={'background-color': '#FCFCFC'})

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        # Output(component_id='title_container', component_property='children'),
    Output(component_id='first_graph', component_property='figure'),
    Output(component_id='second_graph', component_property='figure'),
    Output(component_id='third_graph', component_property='figure'),
    Output("Listings", "children")],
    [Input(component_id='slct_states', component_property='value'),
    Input(component_id='quarter_slider', component_property='value'),
    Input("GDP", "value"),
    Input("PI", "value"),
    Input("UR", "value"),]
)
def update_graph(state_slctd, quarter_slider_slctd, GDP, PI, UR):
    quarter_slctd = quarters_dict_slider[quarter_slider_slctd]['label']
    state_slctd_label = [state for state in states_dict if state['value'] == state_slctd][0]['label']
    #print(quarter_slctd)
    #print(type(quarter_slctd))

    first_df = base_df.copy()
    first_df = first_df[first_df["quarter"] == quarter_slctd]
    
    second_df = base_df.copy()
    #second_df = second_df[second_df["quarter"] == quarter_slctd]
    
    third_df = base_df.copy()
    #

    # title_string = "Airbnb listings"
    if(state_slctd != 'All states'):
        first_df = first_df[first_df["state"] == state_slctd]
        second_df = second_df[second_df["state"] == state_slctd]
        third_df = third_df[third_df["state"] == state_slctd]
        title_string = "{}'s Airbnb listings in {}".format(state_slctd_label[5:], quarter_slctd)
    else:
        #third_df = third_df[third_df["state"] == 'CA']
        third_df = third_df[third_df["quarter"] == quarter_slctd]

    # title = html.H1(title_string, style={
    #         'margin-left' : '0px',
    #         'background' : '#FF5A5F',
    #         'color' : '#FFFFFF',
    #     })
       
    # Plotly Express
    second_fig = px.choropleth(
        data_frame=first_df,
        locationmode='USA-states',
        locations='state',
        scope="usa",
        color='count',
        hover_data=['state', 'count'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        #labels={'state': 'count'},
        #template='seaborn',
        height=180,
        basemap_visible=True,
        title='Map',
        #projection='equirectangular',
    )

    first_fig = px.line(second_df, x="quarter", y="count", color='state', title='Listings per state')
    first_fig['layout']['xaxis']['tickangle'] = -45
    first_fig.update_layout(title='Listings per state by quarter', paper_bgcolor="#FCFCFC", title_x=0.5)
    
    second_fig.update_geos(showcountries = True)
    second_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text='Maps', plot_bgcolor='#FCFCFC')
    
    if(state_slctd != 'All states'):
        third_fig = px.bar(third_df, x='quarter', y=['income',"gdp"], color='unemployment', height=300, barmode='relative', labels={'value':'Income | GDP'})
    else:
        #third_fig = px.bar(third_df, x="quarter", y=['income',"gdp"], color='unemployment', height=300, barmode='overlay')
        
        #third_fig.update_traces(texttemplate=['%{text:.2s}', '%{text:.2s}'], textposition='inside')
        #texts = [third_df['income'].tolist(), third_df['gdp'].tolist()]
        third_fig = px.bar(third_df, x="state", y=['income',"gdp"], color='unemployment', height=300, barmode='relative', labels={'value':'Income | GDP'})
        # for i, t in enumerate(texts):
        #     third_fig.data[i].text = t
        #     third_fig.data[i].textposition = 'outside'
        #print(third_fig.data)
    third_fig.update_layout(title='Income, GDP and unemployment rate per state', paper_bgcolor="#FCFCFC", title_x=0.5)
    
    GDP = GDP/100
    UR = UR/100
    PI = PI/100
    personal_income = 0
    prediction = ''
    personal_income = (regression_coefficients['intercept'] + regression_coefficients['gdp_coeff'] * GDP + regression_coefficients['ur_coeff'] * UR + regression_coefficients['income_coeff'] * PI)
    prediction = u'{:.5f} %'.format(personal_income)
    

    # return title, first_fig, second_fig, third_fig, prediction
    return first_fig, second_fig, third_fig, prediction

# -------------------------------------------------------------------------------------------------------
#if __name__ == '__main__':
#    app.run_server(host='0.0.0.0',port=8080, debug=False)
