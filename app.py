# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from maindash import app

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from pages.image_page import tiff_layout
from pages.analysis_page import analysis_layout
from pages.table_page import table_layout
from pages.home_page import home_layout

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#080124",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    # "padding": "2rem 1rem",
    # 'background': '#111111'
}

NAVLINK_STILE = {
    'color': 'white', 'fontSize': 20
}

sidebar = html.Div(
    [
        html.H3("HSIDash", style={'color': 'white', 'fontSize': 40}),
        # html.Hr(),
        html.P(
            "Manage and Analize HSI Database", style={'color': 'white', 'fontSize': 15}
        ),
        html.Hr(style={'color': 'white', 'fontSize': 30}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/",
                            active="exact", style=NAVLINK_STILE),
                dbc.NavLink("View", href="/image",
                            active="exact", style=NAVLINK_STILE),
                dbc.NavLink("Delete/Modify", href="/table",
                            active="exact", style=NAVLINK_STILE),
                dbc.NavLink("Analysis", href="/analysis",
                            active="exact", style=NAVLINK_STILE),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content], style={'background': '#060030'})


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/table":
        return table_layout
    elif pathname == "/image":
        return tiff_layout
    elif pathname == "/analysis":
        return analysis_layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
    app.run_server(debug=True)
