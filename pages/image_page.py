
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
database = Database()

# load data
# database.get_all_rgb_name()
tiff_data = database.get_spim_by_id(id=4444)
mask_data = database.get_mask_cubic_by_name(name="Set_1_lower_10_icg")
rgb_data = database.get_rgb_by_id(id=2222)

all_files = database.get_all_rgb_name()

all_mask_names = ["Specular reflection","Artery","Vein","Stroma, ICG"]

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
                        all_files,
                        value=all_files[0], 
                        id='rgb-name-dropdown'
                        ,style={'width': '70%',}
                    ),
                    # dcc.Dropdown(
                    #     all_files,
                    #     placeholder="Filter",style={'width': '50%',}
                    # ),
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
                    
                    # html.Div(
                    #     dcc.Graph(
                    #         id="graph-pca", 
                    #         # figure=None,
                    #         style={'width': '70vh', 'height': '70vh'}
                    #     )
                    # , style=padding_border_style(10)),
                    
                    # html.Div(
                    #     dcc.Graph(
                    #         id="graph-pca-histogram", 
                    #         # figure=None,
                    #         style=FIGURE_STYLE
                    #     )
                    # , style=padding_border_style(10)),
                    
                    
                    # html.Div(
                    #     dcc.Graph(
                    #         id="graph-kmeans", 
                    #         # figure=None,
                    #         style=FIGURE_STYLE
                    #     )
                    # , style=padding_border_style(10)),
                    
                    
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
                                # marks={
                                #     0: all_mask_names[0],
                                #     1: all_mask_names[1],
                                #     2: all_mask_names[2],
                                #     3: all_mask_names[3],
                                # },
                                id='mask-slider',
                                # marks=None,
                                tooltip={"placement": "bottom", "always_visible": False},
                                # style={"color": "blue", "fontSize": 14,"writing-mode": "vertical-rl","text-orientation": "upright"}
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
                
                    ],style=BORDER_STYLE),
                    
                    
                    # dbc.Col([
                    #     html.Div([
                    #         html.H6(children=f'PCA Band',
                    #                     style={'color': 'white','textAlign': 'center',}),

                    #         dcc.Slider(
                    #             0, 
                    #             len(tiff_data[0, 0, :])-1, 1,
                    #             value=0,
                    #             id='pca-slider',
                    #             marks=None,
                    #             tooltip={"placement": "bottom", "always_visible": True}
                    #         ),

                    #         html.Hr(),                 
                            
                    #     ], style={"margin":30,'textAlign':'center'})
                
                    # ],style=BORDER_STYLE),
                    
                    # dbc.Col([
                    #     html.Div([
                    #         html.H6(children=f'Clusters',
                    #                     style={'color': 'white','textAlign': 'center',}),

                    #         dcc.Slider(
                    #             2, 5, 1,
                    #             value=2,
                    #             id='cluster-slider',
                    #             marks=None,
                    #             tooltip={"placement": "bottom", "always_visible": True}
                    #         ),

                    #         html.Hr(),                 
                            
                    #     ], style={"margin":30,'textAlign':'center'})
                
                    # ],style=BORDER_STYLE),
                    
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
    Input('bright-slider', 'value'), Input('contrast-slider', 'value'),
    Input('rgb-name-dropdown', 'value')])
def tiff_figure_slide_band(band_index, mask_index, isMask, isRGB,brightness,contrast, rgb_name_dropdown):
    
    print(rgb_name_dropdown)
    rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)
    
    if isRGB:
        # if mask or not
        if isMask == False:
            pltdata = rgb_np_data
        else:
            # pltdata = rgb_data

            # print(mask_data.shape)
            mask_ = mask_np_data[:,:,:,np.newaxis]
            mask__ = np.repeat(mask_[mask_index], 3, axis=2)
            print(not np.any(mask__) )

            pltdata = rgb_np_data * mask__ #* np.stack([mask_data[mask_index]*3], 2)

            # print(mask_)
            # print(mask_data.shape)
            # print(np.stack([mask_data[mask_index]*3], 2).shape)
            # print(np.count_nonzero(np.stack([mask_data[mask_index]*3], 2))==1)

            # pltdata = rgb_data * np.repeat(mask_[mask_index], 3, axis=2)
            # pltdata = rgb_data #* np.stack([mask_data[mask_index]*3], 2) *rgb_data

    else:
        # if mask or not
        if isMask == False:
            pltdata = spim_np_data[:, :, band_index]
        else:
            print(mask_np_data.shape)
            print(spim_np_data.shape)
            pltdata = spim_np_data[:, :, band_index] * mask_np_data[mask_index]
            
    # apply_brightness_contrast
    pltdata = apply_brightness_contrast(pltdata, brightness, contrast)    

    fig = px.imshow(pltdata)

    fig.update_layout(FIGURE_STYLE,dragmode="drawclosedpath")
    # fig.update_layout(width=600,autosize=False)
    # fig.update_layout(title={'text': '<b>Image</b>'}, title_x=0.5)

    return fig

# function to write figure


@app.callback(
    Output("graph-histogram", "figure"),
    [Input("band-tiff-fig", "relayoutData"),Input('band-slider', 'value'), 
    Input('mask-slider', 'value'), Input('is-masked', 'value'), Input('is-rgb', 'value'),
    Input('bright-slider', 'value'), Input('contrast-slider', 'value')],
    Input('rgb-name-dropdown', 'value'))
def html_figure_tiff_image(relayout_data,band_index, mask_index, isMask, isRGB,brightness,contrast, rgb_name_dropdown):

    rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)


    if isRGB:
        # if mask or not
        if isMask == False:
            pltdata = rgb_np_data
        else:
            mask_ = mask_np_data[:,:,:,np.newaxis]
            # print(mask_.shape)
            pltdata = rgb_np_data * np.repeat(mask_[mask_index], 3, axis=2)
    else:
        # if mask or not
        if isMask == False:
            pltdata = spim_np_data[:, :, band_index]
        else:
            
            pltdata = spim_np_data[:, :, band_index] * mask_np_data[mask_index]
            
    pltdata = apply_brightness_contrast(pltdata, brightness, contrast)    


    if relayout_data != None and "shapes" in relayout_data:
        last_shape = relayout_data["shapes"][-1]
        mask = path_to_mask(last_shape["path"], pltdata.shape)
        fig = px.histogram(pltdata[mask])
        fig.update_layout(FIGURE_STYLE)
        fig.update_layout(title={'text': '<b>Histgram</b>'}, title_x=0.5)

        return fig
    else:
        # return no_update
        fig = px.histogram(pltdata.reshape(-1))
        fig.update_layout(FIGURE_STYLE)
        fig.update_layout(title={'text': '<b>Histgram</b>'}, title_x=0.5)

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



# @app.callback(
#     Output("graph-pca", "figure"),
#     [Input('rgb-name-dropdown', 'value'),Input('pca-slider', 'value')])
# def figure_pca(rgb_name_dropdown,pca_slider):
    
#     from sklearn.decomposition import PCA
    
#     rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

#     # PCA implementatio    
#     original_size = spim_np_data.shape[0]
    
#     spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
#     # print(spim_np_data.shape)
#     n_components = spim_np_data.shape[-1]
        
#     pca = PCA(n_components=n_components)
    
#     pca_result = pca.fit_transform(spim_np_data)
#     print("finish PCA!")
    
#     # print(pca_result.shape)
#     pca_result = pca_result[:,np.newaxis,:]
#     pca_result = pca_result.reshape(original_size,-1,n_components)
#     print(pca_result.shape)
    

#     fig = px.imshow(pca_result[:,:,pca_slider])

#     fig.update_layout(FIGURE_STYLE)
#     fig.update_layout(title={'text': '<b>Principal Component Analysis</b>'}, title_x=0.5)

#     return fig
    
    
    
# @app.callback(
#     Output("graph-pca-histogram", "figure"),
#     [Input('rgb-name-dropdown', 'value'),Input('pca-slider', 'value')])
# def figure_pca(rgb_name_dropdown,pca_slider):
    
#     from sklearn.decomposition import PCA
    
#     rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

#     # PCA implementatio    
#     original_size = spim_np_data.shape[0]
    
#     spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
#     # print(spim_np_data.shape)
#     n_components = spim_np_data.shape[-1]
        
#     pca = PCA(n_components=n_components)
    
#     pca_result = pca.fit_transform(spim_np_data)
#     # print("finish PCA!")
    
#     # print(pca_result.shape)
#     pca_result = pca_result[:,np.newaxis,:]
#     pca_result = pca_result.reshape(original_size,-1,n_components)
#     # print(pca_result.shape)
    

#     fig = px.histogram(pca_result[:,:,pca_slider].reshape(-1))

#     fig.update_layout(FIGURE_STYLE)
#     fig.update_layout(title={'text': '<b>Principal Component Analysis - Histgram</b>'}, title_x=0.5)

#     return fig


# @app.callback(
#     Output("graph-kmeans", "figure"),
#     [Input('rgb-name-dropdown', 'value'),Input('cluster-slider', 'value')])
# def figure_pca(rgb_name_dropdown,cluster_slider):
    
#     from sklearn.cluster import KMeans
#     import pandas as pd
    
#     rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

#     # PCA implementatio
#     original_size = spim_np_data.shape[0]
    
#     spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
    
#     n_components = spim_np_data.shape[-1]

#     # print(spim_np_data.shape)
#     kmeans = KMeans(n_clusters=cluster_slider, random_state=0).fit(spim_np_data.T)
#     print("finish KMeans!")
    
#     print("kmeans.shape : ",kmeans.labels_.shape)
#     # print("df.shape : ",df.shape)
    
#     from sklearn.decomposition import PCA
    
#     pca = PCA(n_components=3)
#     print("PCA calc...")
#     pca_result = pca.fit_transform(spim_np_data.T)

#     print("pca_result.shape : ",pca_result.shape)
    
#     df = pd.DataFrame(pca_result, columns=["PC1","PC2","PC3"])
    
#     df['cluster_group'] = kmeans.labels_
    
#     print("df.shape : ",df.shape)
    
    
#     fig = px.scatter_3d(df,x='PC1', y='PC2', z='PC3', color='cluster_group')

#     fig.update_layout(FIGURE_STYLE)
#     fig.update_layout(title={'text': '<b>K-Means and PCA</b>'}, title_x=0.5)

#     return fig