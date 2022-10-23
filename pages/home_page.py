
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from util.styles import FIGURE_STYLE,border_style
import pandas as pd
from util.components import row

def ts_plot():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    fig = px.line(df, x='Date', y='AAPL.High',
                  title='Time Series with Range Slider and Selectors')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(FIGURE_STYLE)

    return dcc.Graph(
        figure=fig,
    )


def bar_chart():
    wide_df = px.data.medals_wide()

    fig = px.bar(wide_df, x="nation", y=[
                 "gold", "silver", "bronze"], title="Wide-Form Input")

    fig.update_layout(FIGURE_STYLE)

    return dcc.Graph(
        figure=fig,
    )


def pychart():
    labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
    values = [4500, 2500, 1053, 500]

    df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
    # Represent only large countries
    df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries'
    fig = px.pie(df, values='pop', names='country',
                 title='Population of European continent')

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])

    fig.update_layout(template='plotly_dark')
    fig.update_layout(FIGURE_STYLE)

    return dcc.Graph(
        id='iris-exp-vs-gdp',
        figure=fig,
    )


def overview_component(number, text):
    return html.Div([
        dbc.Row([
                    html.H1(number, style={'color': 'white', 'margin': 15}),
                    html.H5(text, style={'color': 'white', 'margin': 15})
                    ])
    ], style={"border": "2px white transparent", 'margin': 10, 'border-radius': 10, 'background': '#181240'})


home_layout = html.Div([

    row([
        overview_component(838, "Total Patients"),
        overview_component(345, "Total Dataset Size"),
        overview_component(8433, "Total Images"),
        overview_component(936, "Total Table Size")
    ]),

    dbc.Row(
        [
            html.Div(ts_plot(), style=border_style(50)),
            html.Div(bar_chart(), style=border_style(40)),
        ]
    ),

    dbc.Row(
        [
            html.Div(bar_chart(), style=border_style(40)),
            html.Div(pychart(), style=border_style(50)),

        ]
    ),

], className='row', style={})
