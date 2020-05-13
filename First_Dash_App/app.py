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

# load data for country indicators plot
ctry_ind = pd.read_csv('country_indicators.csv')

# set available indicators for interactive plots
available_indicators = ctry_ind['Indicator Name'].unique()

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
    'background': '#e6ffff',
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
    ), 
    
    # div to break up the spacing
    html.Div([
        html.Br()
    ]),
    
    # interactive series of plots (crossfilter plots)
    html.Div([
    
        # interactive plot options
        html.Div([
        
            # left side plot options
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Fertility rate, total (births per woman)'
                ),
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            # style for the left side options
            style={'width': '49%', 'display': 'inline-block'}),
        
            # right side plot options
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Life expectancy at birth, total (years)'
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            # style for the right side options
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
            )
        ],
        # style for the interactive plot options div
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        
        # left side of interactive figure (scatter plot)
        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Japan'}]}  # set initial hoverData value
            )
        ], 
        # style for left side of figure (scatter plot)
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        
        # right side of interactive figure (two time-series line plots)
        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ], style={'display': 'inline-block', 'width': '49%'}),
        
        # bottom slider
        html.Div(dcc.Slider(
            id='crossfilter-year--slider',
            min=ctry_ind['Year'].min(),
            max=ctry_ind['Year'].max(),
            value=ctry_ind['Year'].max(),
            marks={str(year): str(year) for year in ctry_ind['Year'].unique()},
            step=None
            ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}
        )
        
    ]) # close interactive series of plots
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
            transition={'duration': 500},   # this creates smooth transitions when updating the figure
        )
    }

# interactive series of plots (crossfilter plots series)
@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value')])
def update_scatter_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    
    # filter the dataframe by selected year
    dff = ctry_ind[ctry_ind['Year'] == year_value]
    
    # return the figure for dcc.Graph of crossfilter-indicator-scatter
    return {
        'data': [dict(
            x=ctry_ind[ctry_ind['Indicator Name'] == xaxis_column_name]['Value'],  # return the 'Value' df column
            y=ctry_ind[ctry_ind['Indicator Name'] == yaxis_column_name]['Value'],  # reutrn the 'Value' df column
            text=ctry_ind[ctry_ind['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=ctry_ind[ctry_ind['Indicator Name'] == yaxis_column_name]['Country Name'],  # generate customdata for hover tool
            mode='markers',  # scatter plot
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

# not tied to a callback because not immediately following a decorator '@'
# must call this function in the following callback function
# could have included this in each of the callbacks below, but that would be redundant since using twice
def create_time_series(dff, axis_type, title):
    return{
        'data': [dict(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 255,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

# callbacks to create the time-series plots
@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value')])
def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']   # see above Input for the id where this was defined in the layout
    dff = ctry_ind[ctry_ind['Country Name'] == country_name]   # filter dataframe by country from hoverdata
    dff = dff[dff['Indicator Name'] == xaxis_column_name]   # filter dataframe to specified x data
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)  # mix of HTML in to format graph title
    return create_time_series(dff, axis_type, title)    # call the function above to generate the plot

@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value')])
def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = ctry_ind[ctry_ind['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
    

# run the app if app.py is the main file
if __name__ == '__main__':
    app.run_server(debug=True)