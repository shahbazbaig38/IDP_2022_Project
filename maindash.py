import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost:3306/hsi"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# server.config['MYSQL_USER'] = 'root'
# server.config['MYSQL_PASSOWRD'] = 'root1234'


print("before SQLAlchemy")
db:SQLAlchemy = SQLAlchemy(server)
print("SQLAlchemy")


from database.database import Database

database = Database()


@server.route('/spims/<int:id>', methods=['GET'])
def get_spims(id:int):
        numpy_spim = database.get_spim_by_id(id)
        return numpy_spim.tostring()

@server.route('/hello', methods=['GET'])
def test():
        return "hello"

@server.route('/tissueclass', methods=['GET'])
def get_tissueclass():
        return {'hello': 'world'}

@server.route('/classfeature', methods=['GET'])
def get_classfeature():
        return {'hello': 'world'}



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,server=server)
