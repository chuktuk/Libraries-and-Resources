#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is a primary layout for dash apps.

#######################    THE PRIMARY DASH FILE SHOULD BE NAMED app.py   ######################

References:

https://dash.plotly.com/dash-core-components/tabs
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
https://dash.plotly.com/datatable

If using chained callbacks, use dcc.Dropdown instead of dbc.Select

"""

################################################### IMPORTS ##########################################################

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


############################################ CUSTOM CSS STYLES ##################################################


# set additional css styling
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',   # absolute position might work better
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

################################################ DATA QUERIES ################################################

# read in sample data
# df = pd.read_csv('gap.csv')
# df2 = pd.read_csv('states.csv')
df3 = px.data.gapminder()
df3['year'] = df3['year'].astype('int')

############################################# DATA WRANGLING ##########################################


# extract Canada data
data_canada = df3[df3.country == 'Canada']

# extract US data
data_usa = df3[df3.country == 'United States']

############################################# LISTS ######################################################

years = sorted(list(df3.year.unique()))

########################################### UI CONTROLS AND INPUTS #########################################

################ 1. Sidebar Controls and Titles ###################


# control 1
control_one_title = html.P('Control 1 Display Name', style={'textAlign': 'center'})
# using a dropdown for example here
control_one_object = dcc.Dropdown( # can also use a dbc.Select object / but this isn't compatible with chained callbacks
    id='dropdown',
    options=[{
        'label': 'Value One',
        'value': 'Value1'
    }, {
        'label': 'Value Two',
        'value': 'Value2'
    }],
    value='Value1',  # default value
    # multi=True
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
    value='value1',  # default selected value
    style={'margin': 'auto'}
)])

# submit button
submit_button = dbc.Button(
    id='submit_button',
    n_clicks=0,
    children='Submit',
    color='primary',
    block=True
)

################# 2. Figure Controls #####################

# year slider for gapminder plot
year_slider = dcc.Slider(
    id='year-slider',
    min=min(years),
    max=max(years),
    value=max(years),
    marks={str(i): str(i) for i in years},
    step=None
)

########### 3. Define Form Groups if Needed #########


controls = dbc.FormGroup(
    [
        control_one_title,
        control_one_object,
        html.Br(),

        control_two_title,
        control_two_object,
        html.Br(),

        submit_button,

    ]
)

################################################ SIDEBAR ###############################################

# define the sidebar content
sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

########################################## DASHBOARD CONTENT #########################################

########################### 1. Cards and Card Decks ###############################

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
            html.H5('This card has dynamic color based on the radio items selection', className='card-title'),
            html.P(id='card2_content', className='card-text'),
        ]
    ),
]

# define a card to be used in a bit
third_card = [
    # set a card header
    dbc.CardHeader('Primary Color Card'),
    dbc.CardBody(
        [
            html.H5('Card 3 Title', className='card-title'),
            html.P(id='card3_content', className='card-text', ),
        ]
    ),
]

# define a card to be used in a bit
fourth_card = [
    # set a card header
    dbc.CardHeader('Info Color'),
    dbc.CardBody(
        [
            # html.H5('Card 4 Title', className='card-title'),
            html.Div(id='card4_content', className='card-text', ),
        ]
    ),
]

# define a card deck for a row
fr_card_deck = dbc.CardDeck(
    [
        # first card
        dbc.Card(first_card),

        # second card
        dbc.Card(second_card, id='second_card', inverse=True),

        # third card that uses a variable rather than explicitly setting
        # this also sets some additional card settings, inverse=True flips the text colors for dark backgrounds
        dbc.Card(third_card, color='primary', inverse=True),

        # colors of interest include 'primary', 'secondary', 'info', 'success', 'warning', 'danger', 'light', 'dark'
        # can use variables and check values to set the card colors
        dbc.Card(fourth_card, color='info', inverse=True)
    ]
)

################################# 2. Plots ####################################

# figure1 plot
fig1 = px.bar(data_canada, x='year', y='pop', hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
              labels={'pop': 'population of Canada'}
              )
fig1.update_layout(title='Canada Population (Bars) and Life Expectancy (Color) Over Time', titlefont={'size': 12})

# figure2 plot
fig2 = px.bar(data_usa, x='year', y='pop', hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
              labels={'pop': 'population of USA'}
              )
fig2.update_layout(title='US Population (Bars) and Life Expectancy (Color) Over Time', titlefont={'size': 12})

# figure 3 plot is defined using a callback at the bottom


############################## 3. Tables #########################################

# primary data table setup
primary_data_table = dash_table.DataTable(
    id='data_table',
    columns=[{'name': i, 'id': i} for i in df3.columns],
    data=df3.to_dict('records'), filter_action='native', sort_action='native',
    page_size=50
)

# figure1 table
figure1_table = dash_table.DataTable(
    id='data_table1',
    columns=[{'name': i, 'id': i} for i in data_canada.columns],
    data=data_canada.to_dict('records'),

    # these settings work well for a page with a navbar on the side, and two cols of plots
    style_table={'overflowX': 'auto'},
    style_cell={'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
    page_size=10,
    filter_action='native',
    sort_action='native'
)

# figure2 table
figure2_table = dash_table.DataTable(
    id='data_table2',
    columns=[{'name': i, 'id': i} for i in data_usa.columns],
    data=data_usa.to_dict('records'),

    style_table={'overflowX': 'auto'},
    style_cell={'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
    page_size=10,
    filter_action='native',
    sort_action='native'
)

# figure3 table created using a callback below


########################### 4. Other Objects ######################################


################################################# APP LAYOUT ###############################################


####################### 1. Assemble Tab Content Into Figures ############################
'''Each figure is a self contained object with tabs'''

# Canada data plot/table
figure1 = (
    dbc.Col(
        dbc.Tabs(
            id='figure1_plot',
            children=[
                dbc.Tab(
                    id='plot',
                    label='Plot',

                    # figure added directly here (not using a callback)
                    children=[dcc.Graph(id='metrics_graph1', figure=fig1)]
                ),
                dbc.Tab(
                    id='figure1_table',
                    label='Table',

                    # table added directly here (not using a callback)
                    children=[figure1_table]
                )
            ]
        ), md=6
        , style={'padding': '25px'}  # , 'background-color': '#f8f9fa'}
    )
)

# US data plot/table
figure2 = (
    dbc.Col(
        dbc.Tabs(
            id='figure2_plot',
            children=[
                dbc.Tab(
                    id='plot2',
                    label='Plot',
                    children=[dcc.Graph(id='metrics_graph2', figure=fig2)]
                ),
                dbc.Tab(
                    id='figure2_table',
                    label='Table',
                    children=[figure2_table]
                )
            ]
        ), md=6
        , style={'padding': '25px'}  # , 'background-color': '#f8f9fa'}
    )
)

# gapminder plot/table
figure3 = [
    dbc.Col(
        dbc.Tabs(
            id='figure3_plot',
            children=[
                dbc.Tab(
                    id='plot3',
                    label='Plot',
                    children=[

                        # figure 3 consists of a div with a plot and its slider
                        html.Div([
                            dcc.Graph(id='metrics_graph3'),  # no figure specified here, set using a callback
                            year_slider
                        ])

                    ]
                ),
                dbc.Tab(
                    id='figure3_table',
                    label='Table'

                    # no table specified here, set using a callback

                )
            ]
        )  # , style={'background-color': '#f8f9fa'}
    )
]

################# 2. Assemble Tabbed Figures into Primary Metrics/Data Tab Layout ################
'''This section adds your self contained figures into a tabbed layout.

metrics includes the primary content, and data is the primary data behind the app.'''

# this is the primary layout for metrics tab (main app area)
# each 'figure' below consists of a tabbed layout of Plot/Table
metrics = dbc.Tab(
    id='metrics',
    label='Metrics',

    # metrics objects here
    # use dbc.Row and/or dbc.Col to organize objects
    children=[
        dbc.Row([figure1, figure2]),
        dbc.Row(figure3)
    ],

    style={'padding-left': '15px', 'padding-right': '15px'}
)

# setup primary data table here
data = dbc.Tab(
    id='data',
    label='Data',

    # this is the primary data table
    children=[
        dbc.Col(
            primary_data_table
        )
    ]
)

########################## 3. Upper Level App Layout ############################
'''Organize app content into rows and cols and specify higher level layout.'''

# using cards for the first row where values can be displayed
content_first_row = dbc.Row([

    # the card deck that can be used to display values
    fr_card_deck

])

# primary layout using a tabbed design
content_primary_tab_design = dbc.Row(
    dbc.Col(
        dbc.Tabs(
            id='primary-content',

            # add tabs here
            children=[
                metrics,
                data
            ]
        )
    )
)

# this is the 'content' of the app, or everything that's not part of the sidebar
# this design uses rows to organize main app content
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
        # html.Hr(),

        # add any additional rows here

    ],
    style=CONTENT_STYLE

)

####################### 4. Initialize App and Set the layout Attribute ###################

# initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# define the app layout after defining the other objects
app.layout = html.Div([sidebar, content])

########################################### CALLBACKS ##################################################
'''Define callbacks for user inputs and interactivity.'''


############ 1. Card Callbacks ###############

# define a callback to update a card's text based on the dropdown with id='dropdown'
@app.callback(
    Output('card1_content', 'children'),
    [Input('dropdown', 'value')])
def update_card1(value):
    return f'{value} is selected in the dropdown'


# define a callback that has multiple outputs based on one input
# to update card colors, you must update the dbc.Card object
# to update card text, you must update the parts of a card (dbc.CardHeader or dbc.CardBody for example)
@app.callback(
    [Output('card2_content', 'children'),
     Output('second_card', 'color')],
    [Input('radio_items', 'value')])
def update_card2(value):
    if value == 'value1':
        color = 'warning'
    if value == 'value2':
        color = 'danger'

    return f'{value} is selected in the radio buttons', color


# define a callback with multiple inputs
@app.callback(
    Output('card3_content', 'children'),
    [Input('dropdown', 'value'), Input('radio_items', 'value')])
def update_card3(dropdown_value, radio_value):
    return f'The dropdown value is {dropdown_value}, and the radio value is {radio_value}.'


# define a callback that uses the submit button
# using the Input as the submit button, with the n_clicks as the property to watch
# using state to monitor the actual input data
@app.callback(
    Output('card4_content', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'),
     State('radio_items', 'value')])
def update_card4(n_clicks, dropdown_value, radio_value):
    content = [html.P(f'''Dropdown Value = {dropdown_value}, Radio Value = {radio_value}'''),
               html.P(f'''This card only updates when the Submit Button is clicked. n_clicks={n_clicks}.''')]

    return content


########### 2. Plot/Table Callbacks #################

# figure3 plot and table
@app.callback([Output('metrics_graph3', 'figure'),
               Output('figure3_table', 'children')],
              [Input('year-slider', 'value')])
def update_fig3(year):
    df = df3.query(f'year=={year}')
    fig = px.scatter(df, x='gdpPercap', y='lifeExp', size='pop', color='continent',
                     hover_name='country', log_x=True, size_max=60)
    fig.update_layout(title=f'GDP Per Capita vs. Life Expectancy for {year}',
                      annotations=[{'xref': 'paper', 'yref': 'paper', 'x': -0.03, 'y': 1.08, 'showarrow': False,
                                    'text': 'Each Bubble is a Country: Bubble Size Represents Population'}])

    table = dash_table.DataTable(
        id='data_table3',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),

        style_table={'overflowX': 'auto'},
        style_cell={'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
        page_size=10,
        filter_action='native',
        sort_action='native')

    return fig, table


########################################## RUN SERVER ####################################################

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
