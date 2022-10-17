
from ast import Pass
import io
from dash import html, dcc, Dash
from database.database import Database
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE, border_style, FIGURE_STYLE
import sqlite3
from dash import dcc, html, Input, Output

from maindash import app
import dash_daq

# connect to sqlite
db = Database()

# load data
tiff_data = db.get_tiff()
mask_data = db.get_mask()
id = db.get_id()

# main layouts of the View page
tiff_layout = html.Div(children=[

    dbc.Row(
        [

            dbc.Col(
                [
                    dcc.Graph(
                        id='band-tiff-fig'
                    ),

                    html.H4(children=f'Select Bands',
                            style={'color': 'white'}),
                    dcc.Slider(0, len(tiff_data[0, 0, :]-1), 1,
                               value=0,
                               id='band-slider'
                               ),
                    html.Hr(),
                    html.H4(children=f'Select Masks',
                            style={'color': 'white'}),
                    dcc.Slider(0, len(mask_data[:, 0, 0]-1), 1,
                               value=0,
                               id='mask-slider'
                               ),
                    dash_daq.ToggleSwitch(
                        vertical=False,
                        value=False,
                        id="is-masked"
                    ),
                ],),
            dbc.Col(
                [
                    # html.H2(children='Metadata',
                    #         style={'color': 'white'}),
                    html.H4(children=f'Image ID : {id}',
                            style={'color': 'white'}),
                    html.Div(id='slider-output-container',
                             style={'color': 'white'})

                ],),
        ]
    ),

], className='row')

# function to test slider works fine
@app.callback(
    Output('slider-output-container', 'children'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value')])
def update_output(band_index, mask_index):
    print(band_index)
    return 'You have selected Band : {} Mask : {}'.format(band_index, mask_index)


# function to write figure
@app.callback(
    Output('band-tiff-fig', 'figure'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value'), Input('is-masked', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask):
    print("Band : ", band_index)
    print("Mask : ", mask_index)
    # print(tiff_data[:, :, value].shape)

    # if mask or not
    if isMask == False:
        pltdata = tiff_data[:, :, band_index]
    else:
        pltdata = tiff_data[:, :, band_index] * mask_data[mask_index]

    fig = px.imshow(pltdata)

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(FIGURE_STYLE)

    return fig
