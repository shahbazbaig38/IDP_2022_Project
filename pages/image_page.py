
from ast import Pass
import io
from tkinter.ttk import Style
from dash import html, dcc, Dash, no_update
from database.database import Database
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE, border_style, FIGURE_STYLE
import sqlite3
from dash import dcc, html, Input, Output
from skimage import data, draw
import scipy
from maindash import app
import dash_daq

# connect to sqlite
db = Database()

# load data
tiff_data = db.get_tiff()
mask_data = db.get_mask()
rgb_data = db.get_rgb()

id = db.get_id()


def path_to_indices(path):
    """From SVG path to numpy array of coordinates, each row being a (row, col) point
    """
    indices_str = [
        el.replace("M", "").replace("Z", "").split(",") for el in path.split("L")
    ]
    return np.rint(np.array(indices_str, dtype=float)).astype(np.int)

def path_to_mask(path, shape):
    """From SVG path to a boolean array where all pixels enclosed by the path
    are True, and the other pixels are False.
    """
    cols, rows = path_to_indices(path).T
    rr, cc = draw.polygon(rows, cols)
    mask = np.zeros(shape, dtype=np.bool)
    mask[rr, cc] = True
    mask = scipy.ndimage.binary_fill_holes(mask)
    return mask

img = data.camera()
fig = px.imshow(img, binary_string=True)
fig.update_layout(FIGURE_STYLE,dragmode="drawclosedpath")

fig_hist = px.histogram(img.ravel())


# main layouts of the View page
tiff_layout = html.Div(children=[
    html.Div(
        [
            dbc.Row(
                [
                    dcc.Dropdown(
                        ['Set 1, lower 10, icg', 'Set 1, lower 10, icg', 'Set 1, lower 10, icg'],
                        placeholder="Select Image",style={'width': '50%',}
                    ),
                    dcc.Dropdown(
                        ['Set 1, lower 10, icg', 'Set 1, lower 10, icg', 'Set 1, lower 10, icg'],
                        placeholder="Filter",style={'width': '50%',}
                    ),
                ]),
            # html.H4(children=f'Select Image Here by filtering'),
            # dcc.Dropdown(
            #     ['Set 1, lower 10, icg', 'Set 1, lower 10, icg', 'Set 1, lower 10, icg'],
            #     placeholder="Select Image",
            # )
        ],
        style={"border": "2px white transparent",
                   'margin': 10, 'border-radius': 20, 'background': '#181240',
                   'width': '100%', 'color': 'white', 'padding': 30}
    ),
                
    html.Div(
        [
            dbc.Col(
                [
                    html.Div(
                        dcc.Graph(
                        id='band-tiff-fig'
                    )),

                    dbc.Row(
                        [
                            html.H4(children=f'Bands',
                                    style={'color': 'white'}),
                            dcc.Slider(
                                0, 
                                len(tiff_data[0, 0, :])-1, 1,
                                value=0,
                                id='band-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Hr(),
                            html.H4(children=f'Masks',
                                    style={'color': 'white'}),
                            dcc.Slider(
                                0, 
                                len(mask_data[:, 0, 0])-1, 1,
                                value=0,
                                id='mask-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}

                                       
                                       ),
                            html.Hr(),

                            dbc.Row(
                            [ 
                                dash_daq.ToggleSwitch(
                                    labelPosition='bottom',
                                    label='Mask',
                                    value=False,
                                    id="is-masked",
                                    style={'color': 'white'}
                                ),       
                                html.Hr(),                     
                                dash_daq.ToggleSwitch(
                                    labelPosition='bottom',
                                    label='RGB',
                                    value=False,
                                    id="is-rgb",
                                    style={'color': 'white'}
                                ), 
                            ]),

                            
                            html.Hr(),
                        ], style={
                            'margin': 20,
                        }, align='center'

                    ),

                ], style={"border": "2px white transparent",
                          'margin': 20,
                          'border-radius': 20,
                           'background': '#181240',
                          'width': "80%"
                          }
            ),

            dbc.Col(
                [


                    html.Hr(),

                    # html.H2(children='Metadata',
                    #         style={'color': 'white'}),
                    html.H4(children=f'Image ID : {id}',
                            style={'color': 'white', 'margin': 20, }),
                    html.Div(id='slider-output-container',
                             style={'color': 'white', 'margin': 20, }),
                    dcc.Graph(
                        id="graph-histogram", 
                        # figure=fig_hist
                        style=FIGURE_STYLE
                    ),
                ], style={"border": "2px white transparent",
                          'margin': 20,
                           'border-radius': 20, 
                           'background': '#181240',
                          'width': "20%"
                          }),
        ],
        style={'width': '100%'},
        className='row'
    ),
], 

className='row')

# function to test slider works fine


@app.callback(
    Output('slider-output-container', 'children'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value')])
def update_output(band_index, mask_index):
    # print(band_index)
    return 'You selected Band : {} Mask : {}'.format(band_index, mask_index)


# function to write figure
@app.callback(
    Output('band-tiff-fig', 'figure'),
    [Input('band-slider', 'value'), Input('mask-slider', 'value'), 
    Input('is-masked', 'value'), Input('is-rgb', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask, isRGB):

    if isRGB:
        # if mask or not
        if isMask == False:
            pltdata = rgb_data
        else:
            mask_ = mask_data[:,:,:,np.newaxis]
            pltdata = rgb_data * np.repeat(mask_[mask_index], 3, axis=2)
    else:
        # if mask or not
        if isMask == False:
            pltdata = tiff_data[:, :, band_index]
        else:
            pltdata = tiff_data[:, :, band_index] * mask_data[mask_index]

    fig = px.imshow(pltdata)

    fig.update_layout(FIGURE_STYLE,dragmode="drawclosedpath")

    return fig

# function to write figure


@app.callback(
    Output("graph-histogram", "figure"),
    [Input("band-tiff-fig", "relayoutData"),Input('band-slider', 'value'), 
    Input('mask-slider', 'value'), Input('is-masked', 'value'), Input('is-rgb', 'value')])
def tiff_figure_slide_band(relayout_data,band_index, mask_index, isMask, isRGB):

    if isRGB:
        # if mask or not
        if isMask == False:
            pltdata = rgb_data
        else:
            mask_ = mask_data[:,:,:,np.newaxis]
            pltdata = rgb_data * np.repeat(mask_[mask_index], 3, axis=2)
    else:
        # if mask or not
        if isMask == False:
            pltdata = tiff_data[:, :, band_index]
        else:
            pltdata = tiff_data[:, :, band_index] * mask_data[mask_index]

    if relayout_data != None and "shapes" in relayout_data:
        last_shape = relayout_data["shapes"][-1]
        mask = path_to_mask(last_shape["path"], pltdata.shape)
        fig = px.histogram(pltdata[mask])
        fig.update_layout(FIGURE_STYLE)
        return fig
    else:
        return no_update

    # print("Band : ", band_index)
    # print("Mask : ", mask_index)

    # print(mask_data[mask_index].shape)

    # if isMask == False:
    #     pltdata = rgb_data
    # else:

    #     mask_ = mask_data[:,:,:,np.newaxis]
    #     print(mask_.shape)
    #     pltdata = rgb_data * np.repeat(mask_[mask_index], 3, axis=2)

    # # print(np.repeat(mask_data[mask_index], 3, axis=2).shape)
    # fig = px.imshow(pltdata)

    # fig.update_layout(FIGURE_STYLE)

    # return fig
