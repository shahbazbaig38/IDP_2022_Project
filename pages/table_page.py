from tkinter.tix import ROW
from dash import Dash, dash_table, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from util.styles import FIGURE_STYLE, border_style
from util.components import row
from database.database import Database
from dash import html, dcc, no_update

# connect to sqlite
database = Database()

# load data
tiff_data = database.get_spim_by_id(id=4444)
mask_data = database.get_mask_cubic_by_name(name="Set_1_lower_10_icg")
rgb_data = database.get_rgb_by_id(id=2222)

id = 2222

fig = px.imshow(rgb_data)
fig.update_layout(FIGURE_STYLE)
image = dcc.Graph(figure=fig,
                  style={'width': '40vh', 'height': '40vh'})
imageButton = dbc.Button(id='btn', children=f'Image ID : {id}', className='me-2',
                                style={'margin-left': 100, 'width': 150, 'margin-right': 10000})

imageLabel = html.H5(f'Image ID : {id}',
                                style={'margin-left': 100, 'color': 'white'})

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
                    imageButton,
                    imageButton
                ]) for i in range(5)
                ], style={"border": "2px white transparent",
                      'margin': 10, 'border-radius': 10, 'background': '#181240',
                      'width': 6, 'vertical-align': 'top'}),

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
                    dcc.Input(id="inputImageId", type="text", value='', style={'margin-left': 90, 'margin-bottom': 10}),
                    dbc.Button('Update', id='btnUpdateImageId', style={'margin-left': 20}),
                    html.H6(children=f'Patient ID : {id}',
                            style={'color': 'white', 'margin-left': 90, 'margin-bottom': 10 }),
                    dcc.Input(id="inputPatientId", type="text", placeholder="", style={'margin-left': 90, 'margin-bottom': 10}),
                    dbc.Button('Update', id='btnUpdatePatientId', style={'margin-left': 20}),
                    html.Br(),
                    html.Br(),
                    dbc.Button('Delete', id='btnDelete', style={'margin-left': 90, 'margin-bottom': 10})
                ], style={"border": "2px white transparent",
                          'margin': 10, 'border-radius': 10, 'background': '#181240',
                          'width': 3}, align='top'),
        ],
    ),

], className='row')