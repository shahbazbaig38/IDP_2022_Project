
from dash import html, dcc, no_update
from database.database import Database
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE, FIGURE_STYLE, padding_border_style
from dash import dcc, html, Input, Output
from skimage import data, draw
import scipy
from maindash import app
import dash_daq
from util.analytical_tool import apply_brightness_contrast

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
fig = px.imshow(rgb_data, binary_string=True)
fig.update_layout(FIGURE_STYLE,dragmode="drawclosedpath")

fig_hist = px.histogram(img.ravel())
fig_hist.update_layout(FIGURE_STYLE)


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
                ],style={'width': '80%','textAlign': 'center'}),

        ],
        style=BORDER_STYLE
    ),
                
    html.Div(
        [
            dbc.Col(
                [
                    html.Div(
                        dcc.Graph(
                        id='band-tiff-fig',
                        style={'width': '88vh', 'height': '70vh'}
                    ), style=padding_border_style(0)),
                    
                    html.Div(
                        dcc.Graph(
                            id="graph-histogram", 
                            figure=fig_hist,
                            style=FIGURE_STYLE
                        )
                    , style=padding_border_style(10)),

                ], # style=padding_border_style(10)
            ),

            dbc.Col(
                [
                
                    # html.Div(
                    #     dcc.Graph(
                    #         id="graph-histogram", 
                    #         figure=fig_hist,
                    #         # showlegend=False,
                    #         style={'width': '32vh', 'height': '40vh'}
                    #     )
                    # , #style=padding_border_style(0)
                    # ),


                    dbc.Col([
                        html.Div([
                            
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
                                value=True,
                                id="is-rgb",
                                style={'color': 'white'}
                            ),                  
                            
                        ], style={"margin":20})
                
                    ],style=BORDER_STYLE),
                    
                    html.Div(
                        [
                            
                            
                            
                            # html.Hr(),
                            html.H6(children=f'Bands',
                                        style={'color': 'white','textAlign': 'center',}),
                            # html.Hr(),  
                            dcc.Slider(
                                0, 
                                len(tiff_data[0, 0, :])-1, 1,
                                value=0,
                                id='band-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            
                            
                            html.Hr(),
                            html.H6(children=f'Masks',
                                    style={'color': 'white','textAlign': 'center'}),
                            # html.Hr(),  
                            dcc.Slider(
                                0, 
                                len(mask_data[:, 0, 0])-1, 1,
                                value=0,
                                id='mask-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Hr(),

                            html.H6(children=f'Brightness',
                                        style={'color': 'white','textAlign': 'center',}),
                            dcc.Slider(
                                -255, 
                                255, 1,
                                value=0,
                                id='bright-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),

                            html.Hr(),  
                            html.H6(children=f'Contrast',
                                        style={'color': 'white','textAlign': 'center',}),
                            dcc.Slider(
                                -127, 
                                127, 1,
                                value=0,
                                id='contrast-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),


                        ], 
                        style=BORDER_STYLE

                    ),
                    
                    dbc.Col([
                        html.Div([
                            
                            dbc.Button(
                                "RESET", id="reset-button", className="me-2", n_clicks=0
                            ),                  
                            
                        ], style={"margin":30,'textAlign':'center'})
                
                    ],style=BORDER_STYLE),
                    
                    dbc.Col([
                        html.Div([
                            
                                    html.Hr(),

                                    html.H2(children='Metadata',
                                            style={'color': 'white' }),
                                    html.Hr(),

                                    html.H5(children=f'Image ID : {id}',
                                            style={'color': 'white'}),
                                    html.Hr(),

                                    html.Div(id='slider-output-container',
                                            style={'color': 'white' }),

                                    html.Hr(),                    
                            
                        ], style={"margin":30})
                
                    ],style=BORDER_STYLE)
                    
            ]),
            
        ],
        className='row'
    ),
], #style = {'textAlign': 'center'},

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
    Input('is-masked', 'value'), Input('is-rgb', 'value'),
    Input('bright-slider', 'value'), Input('contrast-slider', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask, isRGB,brightness,contrast):
    
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
            
    # apply_brightness_contrast
    pltdata = apply_brightness_contrast(pltdata, brightness, contrast)    

    fig = px.imshow(pltdata)

    fig.update_layout(FIGURE_STYLE,dragmode="drawclosedpath")
    # fig.update_layout(width=600,autosize=False)

    return fig

# function to write figure


@app.callback(
    Output("graph-histogram", "figure"),
    [Input("band-tiff-fig", "relayoutData"),Input('band-slider', 'value'), 
    Input('mask-slider', 'value'), Input('is-masked', 'value'), Input('is-rgb', 'value'),
    Input('bright-slider', 'value'), Input('contrast-slider', 'value')])
def html_figure_tiff_image(relayout_data,band_index, mask_index, isMask, isRGB,brightness,contrast):

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
            
    pltdata = apply_brightness_contrast(pltdata, brightness, contrast)    


    if relayout_data != None and "shapes" in relayout_data:
        last_shape = relayout_data["shapes"][-1]
        mask = path_to_mask(last_shape["path"], pltdata.shape)
        fig = px.histogram(pltdata[mask])
        fig.update_layout(FIGURE_STYLE)
        # fig.update_yaxes(visible=False, showticklabels=False)
        # fig.update_xaxes(visible=False, showticklabels=False)
        fig.update_traces(showlegend=False)

        return fig
    else:
        # return no_update
        fig = px.histogram(pltdata.reshape(-1))
        fig.update_layout(FIGURE_STYLE)
        # fig.update_yaxes(visible=False, showticklabels=False)
        # fig.update_xaxes(visible=False, showticklabels=False)
        fig.update_traces(showlegend=False)

        return fig


# reset button and slidebar 

# reset mask button
@app.callback(
    Output('is-masked', 'value'),
    Output('is-rgb', 'value'),
    Output('band-slider', 'value'),
    [Input('reset-button', 'value')])
def reset_mask_button(reset_button):
    # print("reset")
    
    return False, True, 0 