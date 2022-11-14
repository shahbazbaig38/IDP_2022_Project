import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "mysql://mysql:root1234@localhost:3306/hsi"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config['MYSQL_USER'] = 'root'
server.config['MYSQL_PASSOWRD'] = 'root1234'


print("before SQLAlchemy")
db:SQLAlchemy = SQLAlchemy(server)
print("SQLAlchemy")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,server=server)
