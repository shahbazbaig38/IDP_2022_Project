
from dash import html, dcc
import plotly.express as px
import numpy as np
from PIL import Image


img = np.array(Image.open(
    f"/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, blue dye.tiff"))
fig = px.imshow(img, color_continuous_scale="gray")

tiff_layout = html.Div(children=[
    html.H1(children='This is one of the given Tiff Images'),

    html.Div(children='''
        This is depicted by Dash 
    '''),

    dcc.Graph(
        figure=fig
    ),

])