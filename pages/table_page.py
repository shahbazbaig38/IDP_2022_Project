from dash import Dash, dash_table, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = Dash()


@app.callback(
    Output('datatable-paging', 'data'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"))
def update_table(page_current, page_size):
    return df.iloc[
        page_current*page_size:(page_current + 1)*page_size
    ].to_dict('records')


table_fig = dash_table.DataTable(df.to_dict('records'), [
    {"name": i, "id": i} for i in df.columns],
    style_data={
        'color': 'white',
        'backgroundColor': 'transparent',
        'width': '50%'
},
    style_header={
        'color': 'white',
        'backgroundColor': 'transparent'
},
    page_current=0,
    page_size=5,
    page_action='custom',
    id='datatable-paging',
    style={
        'width': '50%'
},
)

table_layout = html.Div(children=[
    html.H2(children='This is a Table from Dash Official Turtorial',
            style={'color': 'white'}),

    # html.Div(children='''
    #     Dash is so cool
    # ''', ),

    html.Hr(),

    # table_fig, table_fig, table_fig,

    dbc.Row([

        dbc.Col(table_fig),
        dbc.Col(table_fig)

    ])

])
