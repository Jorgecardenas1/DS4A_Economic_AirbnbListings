import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = 'AirBLocuras - DS4A/Team7'
from package import app1


