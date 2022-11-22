# from dash import html, dcc
# import plotly.express as px
# import pandas as pd
# from sklearn.decomposition import PCA
# import dash_bootstrap_components as dbc
# from util.styles import BORDER_STYLE
# from util.components import row
# from util.styles import FIGURE_STYLE,border_style
# from database.database import Database
# from util.styles import BORDER_STYLE, FIGURE_STYLE, padding_border_style,width_style,BORDER_STYLE_NO_WIDTH


from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
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
analysis_layout = html.Div(children=[
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
                            id="graph-pca", 
                            # figure=None,
                            style={'width': '70vh', 'height': '70vh'}
                        )
                    , style=padding_border_style(20)),
                    
                    html.Div(
                        dcc.Graph(
                            id="graph-pca-histogram", 
                            # figure=None,
                            style=FIGURE_STYLE
                        )
                    , style=padding_border_style(20)),
                    
                    
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
            
                    
                    
                    dbc.Col([
                        html.Div([
                            html.H6(children=f'PCA Band',
                                        style={'color': 'white','textAlign': 'center',}),

                            dcc.Slider(
                                0, 
                                len(tiff_data[0, 0, :])-1, 1,
                                value=0,
                                id='pca-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),

                            html.Hr(),                 
                            
                        ], style={"margin":30,'textAlign':'center'})
                
                    ],style=BORDER_STYLE),
                    
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
    
    
    html.Div(
        [
            dbc.Col(
                [
                    
                    
                    html.Div(
                        dcc.Graph(
                            id="graph-kmeans", 
                            # figure=None,
                            style={'width': '70vh', 'height': '70vh'}
                        )
                    , style=padding_border_style(10)),
                    
                    
                ], # style=padding_border_style(10)
            ),

            dbc.Col(
                [
                    
                    dbc.Col([
                        html.Div([
                            html.H6(children=f'Clusters',
                                        style={'color': 'white','textAlign': 'center',}),

                            dcc.Slider(
                                3, 5, 1,
                                value=2,
                                id='cluster-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),

                            html.Hr(),                 
                            
                        ], style={"margin":30,'textAlign':'center'})
                
                    ],style=BORDER_STYLE),
                    
            ]),
            
        ],
        className='row'
    ),
    
    
    
    
], #style = {'textAlign': 'center'},

className='row')




@app.callback(
    Output("graph-pca", "figure"),
    [Input('rgb-name-dropdown', 'value'),Input('pca-slider', 'value')])
def figure_pca(rgb_name_dropdown,pca_slider):
    
    from sklearn.decomposition import PCA
    
    rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

    # PCA implementatio    
    original_size = spim_np_data.shape[0]
    
    spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
    # print(spim_np_data.shape)
    n_components = spim_np_data.shape[-1]
        
    pca = PCA(n_components=n_components)
    
    pca_result = pca.fit_transform(spim_np_data)
    print("finish PCA!")
    
    # print(pca_result.shape)
    pca_result = pca_result[:,np.newaxis,:]
    pca_result = pca_result.reshape(original_size,-1,n_components)
    print(pca_result.shape)
    

    fig = px.imshow(pca_result[:,:,pca_slider])

    fig.update_layout(FIGURE_STYLE)
    fig.update_layout(title={'text': '<b>Principal Component Analysis</b>'}, title_x=0.5)

    return fig
    
    
    
@app.callback(
    Output("graph-pca-histogram", "figure"),
    [Input('rgb-name-dropdown', 'value'),Input('pca-slider', 'value')])
def figure_pca(rgb_name_dropdown,pca_slider):
    
    from sklearn.decomposition import PCA
    
    rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

    # PCA implementatio    
    original_size = spim_np_data.shape[0]
    
    spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
    # print(spim_np_data.shape)
    n_components = spim_np_data.shape[-1]
        
    pca = PCA(n_components=n_components)
    
    pca_result = pca.fit_transform(spim_np_data)
    # print("finish PCA!")
    
    # print(pca_result.shape)
    pca_result = pca_result[:,np.newaxis,:]
    pca_result = pca_result.reshape(original_size,-1,n_components)
    # print(pca_result.shape)
    

    fig = px.histogram(pca_result[:,:,pca_slider].reshape(-1))

    fig.update_layout(FIGURE_STYLE)
    fig.update_layout(title={'text': '<b>Principal Component Analysis - Histgram</b>'}, title_x=0.5)

    return fig


@app.callback(
    Output("graph-kmeans", "figure"),
    [Input('rgb-name-dropdown', 'value'),Input('cluster-slider', 'value')])
def figure_pca(rgb_name_dropdown,cluster_slider):

    
    rgb_np_data, spim_np_data, mask_np_data = database.get_all_data_by_rgb_name(rgb_name_dropdown)

    # PCA implementatio
    original_size = spim_np_data.shape[0]
    
    spim_np_data = spim_np_data.reshape(-1,spim_np_data.shape[-1])
    
    n_components = spim_np_data.shape[-1]

    # print(spim_np_data.shape)
    kmeans = KMeans(n_clusters=cluster_slider, random_state=0).fit(spim_np_data.T)
    print("finish KMeans!")
    
    print("kmeans.shape : ",kmeans.labels_.shape)
    # print("df.shape : ",df.shape)
        
    pca = PCA(n_components=3)
    print("PCA calc...")
    pca_result = pca.fit_transform(spim_np_data.T)

    print("pca_result.shape : ",pca_result.shape)
    
    df = pd.DataFrame(pca_result, columns=["PC1","PC2","PC3"])
    
    df['cluster_group'] = kmeans.labels_
    
    print("df.shape : ",df.shape)
    
    df['band_name'] = [f"{i}" for i in range(df.shape[0])]
    
    
    fig = px.scatter_3d(df,x='PC1', y='PC2', z='PC3', color='cluster_group', text="band_name")

    fig.update_layout(FIGURE_STYLE)
    fig.update_layout(title={'text': '<b>K-Means and PCA</b>'}, title_x=0.5)
    fig.update_layout(showlegend=False)
    
    return fig


