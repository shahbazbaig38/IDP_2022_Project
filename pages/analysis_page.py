from dash import html, dcc
import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA

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

fig_scatter = px.scatter(df_iris, x="sepal_width",
                         y="sepal_length", color="species", symbol="species")


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

analysis_layout = html.Div(children=[
    # html.H1(children='Analysis'),

    html.H2(children='''
        Iris Data PCA 3D
    '''),

    html.Div(
        dcc.Graph(
            id='iris-exp-vs-gdp',
            figure=fig_iris,
            style={
                "width": "100%",
                "height": "100%"
            }),
        style={
            "width": "100%",
            "height": "100%",
        },
    ),

    html.H2(children='''
        Iris Data PCA 2D
    '''),

    dcc.Graph(
        id='iris-2d-vs-gdp',
        figure=fig_scatter,
        style={
            "width": "100%",
            "height": "100%"
        }),

    html.H2(children='''
        Official Dash example
    '''),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    ),

])
