
from dash import html, dcc
import plotly.express as px
import numpy as np
from PIL import Image


img = np.array(Image.open(
    f"/Users/yusukemikami/Repos/IDP_2022_Project/data/Set 1, blue dye.tiff"))
fig = px.imshow(img, color_continuous_scale="gray")

tiff_layout = html.Div(children=[
    html.H2(children='This is one of the given Tiff Images'),

    dcc.Graph(
        figure=fig
    ),

])