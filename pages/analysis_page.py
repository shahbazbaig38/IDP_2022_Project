from dash import html, dcc
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

analysis_layout = html.Div(children=[
    html.H1(children='This is Analysis Example from Official Page'),

    html.Div(children='''
        Dash is so cool 
    '''),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )

])
