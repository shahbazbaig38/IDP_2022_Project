from tkinter.tix import ROW
from dash import Dash, dash_table, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from database.database import Database
from util.styles import FIGURE_STYLE, BORDER_STYLE, border_style
from util.components import row

# connect to sqlite
db = Database()

# load data
tiff_data = db.get_tiff()
mask_data = db.get_mask()
rgb_data = db.get_rgb()

id = db.get_id()

fig = px.imshow(rgb_data)
fig.update_layout(FIGURE_STYLE)
image = dcc.Graph(figure=fig,
                  style={'width': '40vh', 'height': '40vh'})
imageLabel = html.H5(children=f'Image ID : {id}',
                                style={'color': 'white', 'margin-left': 90})
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = Dash()

# main layouts of the Delete/Modify page
delete_modify_layout = html.Div(children=[
    dbc.Row([
            dbc.Col([
                dbc.Row([
                    image,
                    image,
                ]) for i in range(5)
                ], style={"border": "2px white transparent",
                      'margin': 10, 'border-radius': 10, 'background': '#181240',
                      'width': 6}),

            dbc.Col(
                [
                    image,
                    imageLabel,
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H4(children=f'Metadata',
                            style={'color': 'white', 'margin-left': 90, 'margin-bottom': 10 }),
                    html.H6(children=f'Image ID : {id}',
                            style={'color': 'white', 'margin-left': 90, 'margin-bottom': 10}),
                    dcc.Input(id="input1", type="text", placeholder="", style={'margin-left': 90, 'margin-bottom': 10}),
                    html.Button('Update', style={'margin-left': 20}),
                    html.H6(children=f'Patient ID : {id}',
                            style={'color': 'white', 'margin-left': 90, 'margin-bottom': 10 }),
                    dcc.Input(id="input1", type="text", placeholder="", style={'margin-left': 90, 'margin-bottom': 10}),
                    html.Button('Update', style={'margin-left': 20}),
                    html.Br(),
                    html.Br(),
                    html.Button('Delete', style={'margin-left': 90, 'margin-bottom': 10})
                ], style={"border": "2px white transparent",
                          'margin': 10, 'border-radius': 10, 'background': '#181240',
                          'width': 3}, align='top'),
        ], # align='center'
    ),

], className='row')

