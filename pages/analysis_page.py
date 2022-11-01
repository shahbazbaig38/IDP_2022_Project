from dash import html, dcc
import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE
from util.components import row
from util.styles import FIGURE_STYLE,border_style
from database.database import Database
from util.styles import BORDER_STYLE, FIGURE_STYLE, padding_border_style,width_style,BORDER_STYLE_NO_WIDTH

# connect to sqlite
db = Database()
rgb_data = db.get_rgb()
fig = px.imshow(rgb_data)
fig.update_layout(FIGURE_STYLE)

image = dcc.Graph(figure=fig,
                  style={'width': '40vh', 'height': '40vh'})

analysis_layout = html.Div(children=[
    
    # html.Hr(),
    html.H2(children='Two Columns Test', style={'color': 'white',"padding":20}),
    
    dbc.Row([
        dbc.Col([
            
            dbc.Row([
                image,
                image,
            ]) for i in range(5)
            
        ],style=BORDER_STYLE_NO_WIDTH,width={"size":8}),
        
        dbc.Col([
            html.Div([
                
                html.Div(
                    [
                        html.Hr(),
                        html.H5('Example : example',
                            style={'color': 'white'})
                    ]) for i in range(100)
                                 
            ], style={"margin":30})

        ],style=BORDER_STYLE_NO_WIDTH,width={"size": 3})
    ])
    
    
])
