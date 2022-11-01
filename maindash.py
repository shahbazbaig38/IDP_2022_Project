import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from flask import Flask
# from flask_restful import Resource, Api


server = Flask(__name__)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,server=server)

@server.route('/get_api', methods=['GET'])
def get_api_example():
        return {'hello': 'world'}