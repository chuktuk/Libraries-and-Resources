#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is my first dash app."""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# import data for a table
df = pd.read_csv('states.csv')

# create a function to create a table layout using a pandas df
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
        children=html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# load data for a scatterplot
df2 = pd.read_csv('scatter.csv')

# define a css stylesheet to use
external_stylesheets = ['./dash_default.css']

# initialize the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# define a dictionary of css styles for repeatedly used inline styles
colors = {
    'background': '#7FDBFF',
    #'text': '#7FDBFF'
}

# define the layout
app.layout = html.Div(style={'background': colors['background']}, children=[
    html.H1(children='Hello Dash',
           style={
               'textAlign': 'center'
               #, 'color': colors['text']
           }),
    
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center'
        #, 'color': colors['text']
    }),
    
    # simple bar graph with fabricated data
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background']
                #,'font': {
                #    'color': colors['text']
                #}
            }
        }),
    
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df),
    
    # scatter plot using a pandas dataframe
    dcc.Graph(
        id='life_exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df2[df2['continent'] == i]['gdp per capita'],
                    y=df2[df2['continent'] == i]['life expectancy'],
                    text=df2[df2['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df2.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest')
        })
])

# run the app if app.py is the main file
if __name__ == '__main__':
    app.run_server(debug=True)