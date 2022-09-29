
from dash import html, dcc
import plotly.express as px
import numpy as np
from PIL import Image
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE,border_style


img = np.array(Image.open(
    f"/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, blue dye.tiff"))
fig = px.imshow(img, color_continuous_scale="gray")

fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

tiff_layout = html.Div(children=[
    html.H2(children='This is one of the given Tiff Images',
            style={'color': 'white'}),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(
                        figure=fig,
                        style=border_style(89)
                    ),
                    dcc.Graph(
                        figure=fig,
                        style=border_style(89)
                    ),
                ],),
            dbc.Col(
                [
                    dcc.Graph(
                        figure=fig,
                        style=border_style(89)
                    ),
                    dcc.Graph(
                        figure=fig,
                        style=border_style(89)
                    ),
                ],),
        ]
    ),

], className='row')
