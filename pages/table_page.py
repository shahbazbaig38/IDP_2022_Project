from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')


table_layout = html.Div(children=[
    html.H2(children='This is a Table from Dash Official Turtorial'),

    html.Div(children='''
        Dash is so cool 
    ''', style={"margin-bottom": "30px"}),

    dash_table.DataTable(df.to_dict('records'), [
                         {"name": i, "id": i} for i in df.columns])

])
