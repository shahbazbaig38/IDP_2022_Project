
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
rgb_data = db.get_rgb()

id = db.get_id()

# main layouts of the View page
tiff_layout = html.Div(children=[
    html.H4(children=f'Select Image Here by filtering',
            style={"border": "2px white transparent",
                   'margin': 20, 'border-radius': 20, 'background': '#181240',
                   'width': '90%', 'color': 'white', 'padding': 30}),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(dcc.Graph(
                        id='band-tiff-fig'
                    )),

                    dbc.Row(
                        [
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
                            html.Hr(),

                            dash_daq.ToggleSwitch(
                                vertical=False,
                                value=False,
                                id="is-masked"
                            ),
                            html.Hr(),
                        ], style={
                            'margin': 20,
                        }, align='center'

                    ),

                ], style={"border": "2px white transparent",
                          'margin': 20, 'border-radius': 20, 'background': '#181240',
                          'width': "100%"}),
            dbc.Col(
                [

                    dcc.Graph(
                        id='rgb-tiff-fig'
                    ),
                    html.Hr(),

                    # html.H2(children='Metadata',
                    #         style={'color': 'white'}),
                    html.H4(children=f'Image ID : {id}',
                            style={'color': 'white', 'margin': 20, }),
                    html.Div(id='slider-output-container',
                             style={'color': 'white', 'margin': 20, })

                ], style={"border": "2px white transparent",
                          'margin': 20, 'border-radius': 20, 'background': '#181240',
                          'width': 3}, align='top'),
        ],  # align='center'
    ),

], className='row')

# function to test slider works fine


@app.callback(
    Output('slider-output-container', 'children'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value')])
def update_output(band_index, mask_index):
    # print(band_index)
    return 'You have selected Band : {} Mask : {}'.format(band_index, mask_index)


# function to write figure
@app.callback(
    Output('band-tiff-fig', 'figure'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value'), Input('is-masked', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask):

    # if mask or not
    if isMask == False:
        pltdata = tiff_data[:, :, band_index]
    else:
        pltdata = tiff_data[:, :, band_index] * mask_data[mask_index]

    fig = px.imshow(pltdata)

    fig.update_layout(FIGURE_STYLE)

    return fig

# function to write figure


@app.callback(
    Output('rgb-tiff-fig', 'figure'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value'), Input('is-masked', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask):
    print("Band : ", band_index)
    print("Mask : ", mask_index)

    print(mask_data[mask_index].shape)

    if isMask == False:
        pltdata = rgb_data
    else:

        mask_ = mask_data[:,:,:,np.newaxis]
        print(mask_.shape)
        pltdata = rgb_data * np.repeat(mask_[mask_index], 3, axis=2)

    # print(np.repeat(mask_data[mask_index], 3, axis=2).shape)
    fig = px.imshow(pltdata)

    fig.update_layout(FIGURE_STYLE)

    return fig
