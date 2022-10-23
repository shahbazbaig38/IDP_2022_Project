from dash import html, dcc
import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA
import dash_bootstrap_components as dbc
from util.styles import BORDER_STYLE
from util.components import row
from util.styles import FIGURE_STYLE,border_style

# PCA
df_iris = px.data.iris()
X = df_iris[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

pca = PCA(n_components=3)
components = pca.fit_transform(X)
total_var = pca.explained_variance_ratio_.sum() * 100

fig_iris = px.scatter_3d(
    components, x=0, y=1, z=2, color=df_iris['species'],
    # title=f'Total Explained Variance: {total_var:.2f}%',
    labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
)

fig_iris.update_layout(FIGURE_STYLE)

fig_scatter = px.scatter(df_iris, x="sepal_width",
                         y="sepal_length", color="species", symbol="species")

fig_scatter.update_layout(FIGURE_STYLE)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

fig.update_layout(FIGURE_STYLE)

analysis_layout = html.Div(children=[

    html.H2(children='Iris Data PCA 3D', style={'color': 'white'}),


    row([
        dcc.Graph(
            id='iris-exp-vs-gdp',
            figure=fig_iris,
            style=BORDER_STYLE
        ),
        dcc.Graph(
            id='iris-exp-vs-gdp',
            figure=fig_iris,
            style=BORDER_STYLE
        ),
    ]),



    html.H2(children='''
        Iris Data PCA 2D
    ''', style={'color': 'white'}),

    dcc.Graph(
        id='iris-2d-vs-gdp',
        figure=fig_scatter,
        style=BORDER_STYLE
    ),


    html.H2(children='''
            Official Dash example
        ''', style={'color': 'white', 'margin-top': 30}),

    html.Div([

        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=fig,
            style=BORDER_STYLE
        ),

    ], style=BORDER_STYLE),



])
