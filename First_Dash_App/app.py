#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is my first dash app."""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from datetime import datetime as dt

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

# load data for an interactive plot
df3 = pd.read_csv('gap.csv')

# define a css stylesheet to use
external_stylesheets = ['./dash_default.css']

# define markdown text
markdown_text = '''
## Dash and Markdown

#### Brief Notes
- Plot sizes are dynamically scaled to the window automatically.
- Tables are not: a constant font size/spacing is maintained.
- Traditional HTML tags like <ul> are rendered as text.

You can specify your headers using '\#'.\n
Insert a double return using '\\n'.\n
The escape character is '\\'.
'''

# initialize the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# define a dictionary of css styles for repeatedly used inline styles
colors = {
    'background': '#7FDBFF',
    #'text': '#7FDBFF'
}

# define the layout
app.layout = html.Div(style={'background': colors['background']}, children=[
    html.H1(children='Dash is Extremely Dynamic',
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
        }),
    
    # block of markdown
    html.Div([
        dcc.Markdown(children=markdown_text, style={'background': '#FFFFFF'})
    ]),
    
    # single datepicker
    html.Div(style={'background': '#FFFFFF'}, children=[
        html.Div(children='Please pick a date'),
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=dt.today()
        )
    ]),
    
    # div to break up the spacing
    html.Div([
        html.Br()
    ]),
    
    # interactive plot
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df3['year'].min(),
            max=df3['year'].max(),
            value=df3['year'].min(),
            marks={str(year): str(year) for year in df3['year'].unique()},
            step=None
        )
        
    ],
    style={'background': 'white'},
    )
])

# callbacks for interactivity

# GDP and life expectancy
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    filtered_df = df3[df3.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity='0.7',
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
        
    return {
        'data': traces,
        'layout': dict(
            title='Life Expectancy by GDP for {}'.format(selected_year),
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                  'range': [2.3, 4.8]},
            yaxis={'title': 'Life Expectancy',
                  'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 500},
        )
    }

# run the app if app.py is the main file
if __name__ == '__main__':
    app.run_server(debug=True)