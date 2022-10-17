
from ast import Pass
import io
from dash import html, dcc, Dash
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE, border_style
import sqlite3
from dash import dcc, html, Input, Output

from maindash import app

# connect to sqlite
con = sqlite3.connect("database/hsi_database")
cur = con.cursor()

# read dataset
cur.execute("select id, spim from tiff_table")
id = cur.fetchone()[0]

cur.execute("select id, spim from tiff_table")
tiff_data = cur.fetchone()[1]

out = io.BytesIO(tiff_data)
out.seek(0)
tiff_data = np.load(out)


tiff_layout = html.Div(children=[
    html.H2(children='View Image Page',
            style={'color': 'white'}),

    html.Hr(),
    # dcc.Graph(
    #     # figure=fig,
    #     # style=border_style(89),
    #     id='band-tiff-fig'
    # ),
    dbc.Row(
        [

            dbc.Col(
                [
                    dcc.Graph(
                        # figure=fig,
                        # style=border_style(89),
                        id='band-tiff-fig'
                    ),
                    html.H4(children=f'Please Select Bands',
                            style={'color': 'white'}),
                    html.Hr(),
                    dcc.Slider(0, len(tiff_data[0, 0, :]), 1,
                               value=0,
                               id='band-slider'
                               ),
                ],),
            dbc.Col(
                [
                    html.H2(children='Metadata Here',
                            style={'color': 'white'}),
                    html.H4(children=f'Image ID : {id}',
                            style={'color': 'white'}),
                    html.Div(id='slider-output-container',
                             style={'color': 'white'})

                ],),
        ]
    ),

], className='row')


@app.callback(
    Output('slider-output-container', 'children'),
    Input('band-slider', 'value'))
def update_output(value):
    print(value)
    return 'You have selected Band : {}'.format(value)


@app.callback(
    Output('band-tiff-fig', 'figure'),
    Input('band-slider', 'value'))
def tiff_figure_slide_band(value):
    print(value)
    print(tiff_data[:, :, value].shape)
    fig = px.imshow(tiff_data[:, :, value], color_continuous_scale="gray")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig
