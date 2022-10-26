import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output





app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
