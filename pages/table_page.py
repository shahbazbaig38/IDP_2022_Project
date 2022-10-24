from tkinter.tix import ROW
from dash import Dash, dash_table, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from database.database import Database
from util.styles import FIGURE_STYLE, border_style
from util.components import row

# connect to sqlite
db = Database()

# load data
tiff_data = db.get_tiff()
mask_data = db.get_mask()
rgb_data = db.get_rgb()

id = db.get_id()

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
        'width': '30%'
},
    style_header={
        'color': 'white',
        'backgroundColor': 'transparent'
},
    page_current=0,
    page_size=5,
    page_action='custom',
    id='datatable-paging',
    # filter_action='native',
)

# table_fig.update_layout(FIGURE_STYLE)

table_layout = row([

    # dbc.RadioItems(
    #     id="radios",
    #     # className="btn-group",
    #     inputClassName="btn-check",
    #     labelClassName="btn btn-outline-primary",
    #     labelCheckedClassName="active",
    #     options=[
    #         {"label": "CREATE", "value": 1},
    #         {"label": "DELETE", "value": 2},
    #         {"label": "UPDATE", "value": 3},
    #         {"label": "SELECT", "value": 4},
    #     ],
    #     value=1,
    #     style={"overflow": "scroll", 'width': 60}
    # ),



    html.Div([
        html.H2(children='Manage Table',
                style={'color': 'white'}),

        html.Hr(),

    row([

        dbc.Button("CREATE", outline=True, color="light", className="me-1"),
        dbc.Button("DELETE", outline=True, color="light", className="me-1"),
        dbc.Button("UPDATE", outline=True, color="light", className="me-1"),
        dbc.Button("SELECT", outline=True, color="light", className="me-1"),
    ]),        

        html.Hr(),

        dbc.Row([

            dbc.Col(table_fig),
            dbc.Col(table_fig),
            dbc.Col(table_fig),
            dbc.Col(table_fig),

        ])

    ])
])
