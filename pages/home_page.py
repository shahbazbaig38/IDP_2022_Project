
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from util.styles import BORDER_STYLE


def bar_chart():
    wide_df = px.data.medals_wide()

    fig = px.bar(wide_df, x="nation", y=[
                 "gold", "silver", "bronze"], title="Wide-Form Input")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

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

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

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

    dbc.Row(
        [
            dbc.Col(overview_component(838, "Total Patient Number")),
            dbc.Col(overview_component(345, "Total Dataset Size")),
            dbc.Col(overview_component(8433, "Total Image Number")),
            dbc.Col(overview_component(936, "Total Table Size")),
        ]
    ),

    dbc.Row(
        [
            html.Div(pychart(), style={"border": "2px white transparent",
                                       'margin': 25, 'border-radius': 10, 'background': '#181240',
                                       'width': '50%'}),
            html.Div(bar_chart(), style={"border": "2px white transparent",
                                         'margin': 25, 'border-radius': 10, 'background': '#181240',
                                         'width': '40%'}),
        ]
    ),

    dbc.Row(
        [
            html.Div(bar_chart(), style={"border": "2px white transparent",
                                         'margin': 25, 'border-radius': 10, 'background': '#181240',
                                         'width': '40%'}),
            html.Div(pychart(), style={"border": "2px white transparent",
                                       'margin': 25, 'border-radius': 10, 'background': '#181240',
                                       'width': '50%'}),

        ]
    ),

], className='row', style={})
