#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''This is a primary layout for dash apps.

References:

https://dash.plotly.com/dash-core-components/tabs
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
https://dash.plotly.com/datatable


'''

import dash
import dash_table

# must pip install dash_bootstrap_components==0.10.7 or include in requirements.txt
import dash_bootstrap_components as dbc

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

# additional imports here
import pandas as pd

# import custom modules
# customary app design includes putting all functions in main.py and all data queries in query.py
# import main as mn
# import query as qry


# read in sample data
df = pd.read_csv('gap.csv')
df2 = pd.read_csv('states.csv')
df3 = px.data.gapminder()
#df3.columns = ['idx', 'ctry', 'cont', 'pop', 'lifeexp', 'gpdpercap']


# set additional css styling
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

# initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])





# define the controls that are needed (user inputs)
# each control gets a title and and object

# control 1
control_one_title = html.P('Control 1 Display Name', style={'textAlign': 'center'})
# using a dropdown for exmaple here
control_one_object = dcc.Dropdown(
    id='dropdown', 
    options=[{
        'label': 'Value One',
        'value': 'Value1'
    }, {
        'label': 'Value Two',
        'value': 'Value2'
    }],
    value='Value1', # default value
    #multi=True
)

# control 2
control_two_title = html.P('Control 2 Items nested in dbc.Card', 
    style={'textAlign': 'center'}
)
control_two_object = dbc.Card([dbc.RadioItems(
    id='radio_items',
    options=[{
    'label': 'Value One',
    'value': 'value1'
    }, {
    'label': 'Value Two',
    'value': 'value2'
    }],
    value='value1', # default selected value
    style={'margin': 'auto'}
)])



# enter the controls into this template
controls = dbc.FormGroup(
    [
        control_one_title,
        control_one_object,
        html.Br(),
        
        
        control_two_title,
        control_two_object,
        html.Br(),
        
        # submit button
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
        
    ]
)



# define the sidebar content
sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)




# define the first card
# can also include images using dbc.CardImg(src='url', top=True), but keep separate from CardBody
# can use dbc.CardHeader('Header Title') to give a header separated with a line
first_card = dbc.CardBody(
    [
        html.H5('First Card Title', className='card-title'),
        # can use html.P or any other html components here
        html.Div(id='card1_content'),
    ]
)


# define the second card
# if using multiple dbc options within a card, make it a list
second_card = [
    dbc.CardHeader('This card has a header'),
    dbc.CardBody(
        [
            html.H5('This card has warning text', className='card-title'),
            html.P('Some card text, can use f strings here', className='card-text'),
        ]
    ),
]

# define a card to be used in a bit
third_card = [
    # set a card header
    dbc.CardHeader('I also have a card header'),
    dbc.CardBody(
        [
            html.H5('Card 3 Title', className='card-title'),
            html.P('Primary Color', className='card-text',),
        ]
    ),
]

# define a card to be used in a bit
fourth_card = [
    # set a card header
    dbc.CardHeader('Card Header'),
    dbc.CardBody(
        [
            html.H5('Card 4 Title', className='card-title'),
            html.P('Info Text', className='card-text',),
        ]
    ),
]

# define a card deck for a row
fr_card_deck = dbc.CardDeck(
    [
        # first card
        dbc.Card(first_card),
        
        # second card
        dbc.Card(second_card, color='warning', inverse=True),
        
        # third card that uses a variable rather than explicitly setting
        # this also sets some additional card settings, inverse=True flips the text colors for dark backgrounds
        dbc.Card(third_card, color='primary', inverse=True),
        
        # colors of interest include 'primary', 'secondary', 'info', 'success', 'warning', 'danger', 'light', 'dark'
        # can use variables and check values to set the card colors
        dbc.Card(fourth_card, color='info', inverse=True)
    ]
)

# define the app content here
# using cards for the first row where values can be displayed
content_first_row = dbc.Row([
    
    fr_card_deck
    
])

# define tab content here
#tab1 = dcc.Tab(
#    id='tab-1',
#    label='Tab 1',
    
    # tab content here
#    children=[
#        dbc.Row(
#            [
#                dbc.Col(
#                    dcc.Graph(id='tab1_graph1'), md=4
#                ),
#                dbc.Col(
#                    dcc.Graph(id='tab1_graph2'), md=6
#                )
#            ]
#        )
#    ]
#)

#tab2 = dcc.Tab(
#    id='tab-2',
#    label='Tab 2',
    
    # tab content here
#    children=[
#        dbc.Row(
#            [
#                dbc.Col(
#                    dcc.Graph(id='tab2_graph1'), md=12
#                )
#            ]
#        )
#    ]
#)



data_canada = df3[df3.country == 'Canada']
fig1 = px.bar(data_canada, x='year', y='pop', hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
    labels={'pop': 'population of Canada'}
)
fig1.update_layout(title='Canada Population Over Time')


# design a shiny style tabbed layout

# each figure in the metrics tab should be a tabbed layout wiht plot/data
figure1 = (
    dbc.Col(
        dcc.Tabs(
            id='figure1_plot',
            children=[
                dcc.Tab(
                    id='plot',
                    label='Plot',
                    children=[dcc.Graph(id='metrics_graph1', figure=fig1)]
                ),
                dcc.Tab(
                    id='figure1_table',
                    label='Table',
                    children=[
                        
                        # can assign DataTable to a var and use that here
                        dash_table.DataTable(
                        id='data_table2',
                        columns = [{'name': i, 'id': i} for i in data_canada.columns],
                        data=data_canada.to_dict('records'),
                        
                        # these settings work well for a page with a navbar on the side, and two cols of plots
                        style_table={'overflowX': 'auto'},
                        style_cell={'minWidth': '120%', 'width': '120%', 'maxWidth': '120%'},
                        page_size=10)
                    
                    ]
                )
            ]
        ), md=6
    , style={'padding': '25px'}  
    )
)

data_usa = df3[df3.country == 'United States']
fig2 = px.bar(data_usa, x='year', y='pop', hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
    labels={'pop': 'population of USA'}
)
fig2.update_layout(title='US Population Over Time')

figure2 = (
    dbc.Col(
        dcc.Tabs(
            id='figure2_plot',
            children=[
                dcc.Tab(
                    id='plot2',
                    label='Plot',
                    children=[dcc.Graph(id='metrics_graph2', figure=fig2)]
                ),
                dcc.Tab(
                    id='figure2_table',
                    label='Table',
                    children=[
                        
                        # could use a variable and assign the DataTable to that var
                        dash_table.DataTable(
                        id='data_table3',
                        columns = [{'name': i, 'id': i} for i in data_usa.columns],
                        data=data_usa.to_dict('records'),
                        
                        # these settings work well for a page with a navbar on the side, and two cols of plots, I think I like these settings better
                        style_table={'overflowX': 'auto'},
                        style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
                        page_size=10)
                        
                    
                    ]
                )
            ]
        ), md=6
    , style={'padding': '25px'}  
    )
)


fig3 = px.scatter(df3.query('year==2007'), x='gdpPercap', y='lifeExp',
    size='pop', color='continent', hover_name='country', log_x=True, size_max=60
)

# set the tabbed layout for a full width figure
figure3 = [
    dbc.Col(
        dcc.Tabs(
            id='figure3_plot',
            children=[
                dcc.Tab(
                    id='plot3',
                    label='Plot',
                    children=[dcc.Graph(id='metrics_graph3', figure=fig3)]
                ),
                dcc.Tab(
                    id='figure3_table',
                    label='Table',
                    children=[
                        dash_table.DataTable(
                            id='data_table4',
                            columns=[{'name': i, 'id': i} for i in df3.columns],
                            data=df3.to_dict('records'),
                            
                            # these settings work well for a page with a navbar on the side, and two cols of plots, I think I like these settings better
                            style_table={'overflowX': 'auto'},
                            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
                            page_size=10
                        )
                    ]
                )
            ]
        )
    )
]

# define the shiny style metrics tab

# each 'figure' below consists of a tabbed layout of Plot/Table
metrics = dcc.Tab(
    id='metrics',
    label='Metrics',
    
    # change this to a tabbed layout with Plot/Table configuration
    children=[
        #dbc.Row(
        #    [
        #        dbc.Col(
        #            dcc.Graph(id='metrics_graph1'), md=12
        #        )
        #    ]
        #),
        dbc.Row([figure1, figure2]),
        dbc.Row(figure3)
            #[
            #    dbc.Col(
            #        dcc.Graph(id='metrics_graph2'), md=12
            #    )
            #]
        #)
    ]
)

# primary data table setup
primary_data_table = dash_table.DataTable(
    id='data_table',
    columns = [{'name': i, 'id': i} for i in df.columns],
    data=df.to_dict('records')
)

# setup primary data table here
data = dcc.Tab(
    id='data',
    label='Data',
    
    # add the table here
    children=[
        dbc.Col(
            primary_data_table
        )
    ]
)

# design a shiny style tabbed layout
content_primary_tab_design = dbc.Row(
    dbc.Col(
        dcc.Tabs(
            id='shiny-style-tabbing',
            
            #value='metrics',
            
            # add tabs here
            children=[
                metrics,
                data
            ]
        )
    )
)












# this content_second_row is designed to be a tabbed layout
#content_second_row = dbc.Row(
#    dbc.Col(
#        dcc.Tabs(id='tabs-container',
#            # set default selected tab
#            value='tab-1',
#            
#            # add tabs here
#            children=[
#                tab1,
#                tab2
#            ]
#            
#        )
#    )
#)

# the third row is setup to show plots going across in 3 columns
#content_third_row = dbc.Row(
#    [
#        dbc.Col(
#            dcc.Graph(id='graph_1'), md=4
#        ),
#        dbc.Col(
#            dcc.Graph(id='graph_2'), md=4
#        ),
#        dbc.Col(
#            dcc.Graph(id='graph_3'), md=4
#        )
#    ]
#)


# the content of the app goes here
content = html.Div(
    [
        html.H2('Dashboard Title', style=TEXT_STYLE),
        html.Hr(),
        
        # enter your content rows here
        content_first_row,
        
        # add spacing as needed
        html.Hr(),
        
        # primary tab layout here
        content_primary_tab_design,
        #html.Hr(),
        
        #content_second_row,
        #content_third_row
        
    ],
    style=CONTENT_STYLE

)

# define the app layout after defining the other objects
app.layout = html.Div([sidebar, content])

# define a callback to update a card's text based on the dropdown with id='dropdown'
@app.callback(
    Output('card1_content', 'children'),
    [Input('dropdown', 'value')])
def update_card1(value):
    return f'{value} is selected in the dropdown'
    


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)