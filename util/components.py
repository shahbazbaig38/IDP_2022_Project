import dash_bootstrap_components as dbc


def row(components: list):
    return dbc.Row([dbc.Col(component) for component in components])
