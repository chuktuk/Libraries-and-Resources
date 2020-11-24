#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Primary dashboard module."""

# imports
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from .data import create_dataframe, get_data, format_dataframe

import plotly.express as px
import plotly.graph_objects as go

############################################ CUSTOM CSS STYLES ##################################################

# set additional css styling
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    # 'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# define custom css dictionaries
SIDEBAR_STYLE_MULTI = {
    # 'position': 'absolute',
    # 'top': 0,
    # 'left': 0,
    # 'bottom': 0,
    # 'width': '20%',
    # 'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TITLE_TEXT_STYLE = {
    'margin-top': '30px',
    'margin-bottom': '20px',
    'textAlign': 'center',
    'color': '#191970'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

# global dashboard.py objects
df3 = px.data.gapminder()
df3['year'] = df3['year'].astype('int')

data = create_dataframe()

data2 = get_data()
data2 = format_dataframe(data2)


# init single page dashboard
def init_dashboard_single_page(server):
    """Create a plotly dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp_template_single/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    ################################################ DATA QUERIES ################################################

    # moved outside of function

    ############################################# DATA WRANGLING ##########################################

    # extract Canada data
    data_canada = df3[df3.country == 'Canada']

    # extract US data
    data_usa = df3[df3.country == 'United States']

    ############################################# LISTS ######################################################

    years = sorted(list(df3.year.unique()))

    ########################################### UI CONTROLS AND INPUTS #########################################

    ################ 1. Sidebar Controls and Titles ###################

    # very important
    # primary flask app navigation
    navigation_title = html.H2('Navigation', style=TEXT_STYLE)
    go_home = html.A('Application Home', href="/", style={'textAlign': 'center'})

    # control 1
    control_one_title = html.P('Control 1 Display Name', style={'textAlign': 'center'})
    # using a dropdown for example here
    control_one_object = dcc.Dropdown(
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
    param_sidebar = html.Div(
        [
            html.H2('Parameters', style=TEXT_STYLE),
            html.Hr(),
            controls
        ],
        style=SIDEBAR_STYLE,
    )

    nav_sidebar = html.Div(
        [
            navigation_title,
            html.Hr(),
            go_home
        ],
        style=SIDEBAR_STYLE
    )

    sidebar = dbc.Col([nav_sidebar, param_sidebar], style={'position': 'fixed'})

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

    ############################## 3. Tables #########################################

    # primary data table setup
    primary_data_table = dash_table.DataTable(
        id='data_table',
        columns=[{'name': i, 'id': i} for i in df3.columns],
        data=df3.to_dict('records'), filter_action='native', sort_action='native'
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
        style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                    'whiteSpace': 'normal'},
        page_size=10,
        filter_action='native',
        sort_action='native'
    )

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
                            # add controls for year slider
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

    # define the app layout after defining the other objects
    dash_app.layout = html.Div([sidebar, content])

    # initialize the callbacks using function below
    init_callbacks_single_page(dash_app)

    return dash_app.server


# init callbacks
def init_callbacks_single_page(dash_app):
    # IMPORTANT
    # any previously 'global' variables are not found within this function

    # define a callback to update a card's text based on the dropdown with id='dropdown'
    @dash_app.callback(
        Output('card1_content', 'children'),
        [Input('dropdown', 'value')])
    def update_card1(value):
        return f'{value} is selected in the dropdown'

    # define a callback that has multiple outputs based on one input
    # to update card colors, you must update the dbc.Card object
    # to update card text, you must update the parts of a card (dbc.CardHeader or dbc.CardBody for example)
    @dash_app.callback(
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
    @dash_app.callback(
        Output('card3_content', 'children'),
        [Input('dropdown', 'value'), Input('radio_items', 'value')])
    def update_card3(dropdown_value, radio_value):
        return f'The dropdown value is {dropdown_value}, and the radio value is {radio_value}.'

    # define a callback that uses the submit button
    # using the Input as the submit button, with the n_clicks as the property to watch
    # using state to monitor the actual input data
    @dash_app.callback(
        Output('card4_content', 'children'),
        [Input('submit_button', 'n_clicks')],
        [State('dropdown', 'value'),
         State('radio_items', 'value')])
    def update_card4(n_clicks, dropdown_value, radio_value):
        content = [html.P(f'''Dropdown Value = {dropdown_value}, Radio Value = {radio_value}'''),
                   html.P(f'''This card only updates when the Submit Button is clicked. n_clicks={n_clicks}.''')]

        return content

    # figure3 plot and table
    @dash_app.callback([Output('metrics_graph3', 'figure'),
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
            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        'whiteSpace': 'normal'},
            page_size=10,
            filter_action='native',
            sort_action='native')

        return fig, table


def init_multi_page_dashboard(server):
    """Create a plotly dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp_template_multi/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # create options for sidebar filters
    app_one_filter1_options = [{'label': i, 'value': i} for i in sorted(list(data.Category.unique()))]
    app_one_filter1_selected = [i for i in sorted(list(data.Category.unique()))]

    app_one_filter2_options = [{'label': i, 'value': i} for i in sorted(list(data.Department.unique()))]
    app_one_filter2_selected = [i for i in sorted(list(data.Department.unique()))]

    # app one sidebar filters
    app_one_filter1_title = dbc.Label(
        'Categories',
        style={'textAlign': 'center'}
    )
    app_one_filter1 = dbc.Card(
        dbc.Checklist(
            id='app-one-filter1',
            options=app_one_filter1_options,
            value=app_one_filter1_selected,
        ), style={'padding': '5px'}
    )

    app_one_filter2_title = dbc.Label(
        'Departments',
        style={'textAlign': 'center'}
    )
    app_one_filter2 = dbc.Card(
        dbc.Checklist(
            id='app-one-filter2',
            options=app_one_filter2_options,
            value=app_one_filter2_selected,
        ), style={'padding': '5px'}
    )

    # app one figure filters
    app_one_figure1_dropdown_title = dbc.Label(
        'Stage',
        style={'textAlign': 'center'}
    )
    app_one_figure1_dropdown = dcc.Dropdown(
        id='app-one-figure1-dropdown',
        options=[{'label': i, 'value': i} for i in sorted(list(data.Stage.unique()))],
        value='BFG'
    )

    app_one_figure2_radio_title = dbc.Label(
        'Stage',
        style={'textAlign': 'center'}
    )
    app_one_figure2_radio = dbc.RadioItems(
        id='app-one-figure2-radio',
        options=[{'label': i, 'value': i} for i in sorted(list(data.Stage.unique()))],
        value='BFG'
    )

    app_one_figure2_dropdown_title = dbc.Label(
        'Analyze By',
        style={'textAlign': 'center'}
    )
    app_one_figure2_dropdown = dcc.Dropdown(
        id='app-one-figure2-dropdown',
        options=[{'label': i, 'value': i} for i in ['Category', 'Department']],
        value='Category'
    )

    # app two filters
    app_two_filter1_title = dbc.Label(
        'Filter 1',
        style={'textAlign': 'center'}
    )
    app_two_filter1 = dbc.Card(
        dbc.Checklist(
            id='app-two-filter1',
            options=[{'label': i, 'value': i} for i in range(10)],
            value=[i for i in range(10)]
        )
    )

    app_two_filter2_title = dbc.Label(
        'Filter 2',
        style={'textAlign': 'center'},
    )
    app_two_filter2 = dbc.Card(
        dbc.Checklist(
            id='app-two-filter2',
            options=[{'label': f'Option {i}', 'value': f'Option {i}'} for i in range(2, 10, 2)]
        )
    )

    # app two figure filters
    app_two_by_list = ['Rate Class Descr',
                       'EAM Department Name',
                       'Manufacturer',
                       'Component Description',
                       'Asset Alias']
    app_two_timeframe_list = ['All Years'] + sorted(list(data2['WO Actual Finish Year'].unique()))
    app_two_measure_list = ['Total Work Order Cost', 'Actual Labor Cost', 'Actual Material Cost', 'Actual Service Cost']

    app_two_timeframe_title = dbc.Label(
        'Timeframe',
        style={'textAlign': 'center'}
    )
    app_two_timeframe_dropdown = dcc.Dropdown(
        id='app-two-timeframe-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_timeframe_list],
        value='All Years'
    )

    app_two_by_list_title = dbc.Label(
        'Analyze By',
        style={'textAlign': 'center'}
    )
    app_two_by_list_dropdown = dcc.Dropdown(
        id='app-two-by-list-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_by_list],
        value=app_two_by_list[0]
    )

    app_two_measure_title = dbc.Label(
        'Variable to Plot',
        style={'textAlign': 'center'}
    )
    app_two_measure_dropdown = dcc.Dropdown(
        id='app-two-measure-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_measure_list],
        value=app_two_measure_list[0]
    )

    # sidebar form groups
    app_one_form_group = dbc.FormGroup(
        [
            dbc.FormGroup([app_one_filter1_title, app_one_filter1]),
            dbc.FormGroup([app_one_filter2_title, app_one_filter2]),
            dbc.Button('Submit New Query', id='app-one-submit-query', color='primary')
        ]
    )

    app_two_form_group = dbc.FormGroup(
        [
            dbc.FormGroup([app_two_filter1_title, app_two_filter1]),
            dbc.FormGroup([app_two_filter2_title, app_two_filter2]),
            dbc.Button('Submit New Query', id='app-two-submit-query', color='primary')
        ]
    )

    # sidebars
    go_home = html.A('Application Home', href="/", style={'textAlign': 'center'})

    nav_sidebar = html.Div(
        [
            html.H2('Navigation', style=TEXT_STYLE),
            html.Hr(),
            go_home
        ],
        style={'padding-top': '15px', 'padding-bottom': '30px'},
        # width={'size': 3}
    )

    app_one_param_sidebar = html.Div(
        [
            html.H2('App One Parameters', style=TEXT_STYLE),
            html.Hr(),
            app_one_form_group
        ],
        # style=SIDEBAR_STYLE_MULTI,
        # width={'size': 3}
    )

    app_two_param_sidebar = html.Div(
        [
            html.H2('App Two Parameters', style=TEXT_STYLE),
            html.Hr(),
            app_two_form_group
        ],
        # style=SIDEBAR_STYLE_MULTI,
        # width={'size': 3}
    )

    app_one_sidebar = dbc.Col([nav_sidebar, app_one_param_sidebar],
                              style=SIDEBAR_STYLE_MULTI,
                              width={'size': 3})
    app_two_sidebar = dbc.Col([nav_sidebar, app_two_param_sidebar],
                              style=SIDEBAR_STYLE_MULTI,
                              width={'size': 3})

    # app one cards and card deck
    app_one_selected_filters_card = [
        dbc.CardHeader('Currently Selected Filters'),
        dbc.CardBody(
            [
                html.Div(
                    id='app-one-selected-filters-card'
                )
            ]
        )
    ]

    app_one_download_data_card = [
        dbc.CardHeader('Download Data'),
        dbc.CardBody(
            [
                html.P('Download Data with Applied Filters'),
                html.P('Right-click button and Open in New Tab to download data'),
                dbc.Button(
                    'Download csv',
                    id='app-one-download-button',
                    color='primary',
                    href='/dashapp_template_multi/app_one/urlToDownload',
                    n_clicks=0
                )
            ]
        )
    ]

    app_one_card_deck = dbc.CardDeck(
        [
            dbc.Card(app_one_selected_filters_card, color='info', inverse=True),
            dbc.Card(app_one_download_data_card, color='light')
        ]
    )

    # app two cards and card deck
    app_two_selected_filters_card = [
        dbc.CardHeader('Selected Filters'),
        dbc.CardBody(
            [
                html.Div(
                    id='app-two-selected-filters-card'
                )
            ]
        )
    ]

    app_two_calculation_card = [
        dbc.CardHeader('A Calculation Card'),
        dbc.CardBody(
            [
                html.P('Change the Parameters in the Sidebar to change the color of this card.'),
                html.Div(
                    id='app-two-calculation-card'
                )
            ]
        )
    ]

    app_two_download_data_card = [
        dbc.CardHeader('Download Data'),
        dbc.CardBody(
            [
                html.P('Download Data with Applied Filters'),
                html.P('Right-click button and Open in New Tab to download'),
                dbc.Button(
                    'Download csv',
                    id='app-two-download-button',
                    color='primary',
                    href='/dashapp_template_multi/app_two/urlToDownload',
                    n_clicks=0
                )
            ]
        )
    ]

    app_two_card_deck = dbc.CardDeck(
        [
            dbc.Card(app_two_selected_filters_card, color='info', inverse=True),

            dbc.Card(app_two_calculation_card, id='change-card-color', inverse=True),

            dbc.Card(app_two_download_data_card, color='light')
        ]
    )

    # figures

    app_one_figure1 = dbc.Col(
        dbc.Tabs(
            children=[
                dbc.Tab(
                    id='app-one-figure1-tab',
                    label='Plot',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([app_one_figure1_dropdown_title, app_one_figure1_dropdown],
                                        style={'display': 'inline-block'},
                                        width=3)
                            ], style={'padding-top': '15px'}),
                            dcc.Graph(id='app-one-figure1-plot')
                        ])
                    ]
                ),
                dbc.Tab(
                    id='app-one-figure1-table-tab',
                    label='Table',
                    children=[
                        html.Div(id='app-one-figure1-table')
                    ]
                )
            ]
        ),
    )

    app_one_figure2 = dbc.Col(
        dbc.Tabs(
            children=[
                dbc.Tab(
                    id='wo-counts-ts-plot-tab',
                    label='Plot',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([app_one_figure2_radio_title, app_one_figure2_radio],
                                        style={'display': 'inline-block'},
                                        width=3),
                                dbc.Col([app_one_figure2_dropdown_title, app_one_figure2_dropdown],
                                        style={'display': 'inline-block'},
                                        width=4),
                                dbc.Col(width=4)
                            ], style={'padding-top': '15px'}),
                            dcc.Graph(id='app-one-figure2-plot')
                        ])
                    ]
                ),
                dbc.Tab(
                    id='app-one-figure2-table-tab',
                    label='Table',
                    children=[
                        html.Div(id='app-one-figure2-table')
                    ]
                )
            ]
        )
    )

    app_two_figure = dbc.Col(
        dbc.Tabs(
            id='app-two-figure',
            children=[
                dbc.Tab(
                    id='app-two-figure-plot-tab',
                    label='Plot',
                    tab_id='plot',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([app_two_timeframe_title, app_two_timeframe_dropdown],
                                        style={'display': 'inline-block'},
                                        width=3),
                                dbc.Col([app_two_by_list_title, app_two_by_list_dropdown],
                                        style={'display': 'inline-block'},
                                        width=4),
                                dbc.Col([app_two_measure_title, app_two_measure_dropdown],
                                        style={'display': 'inline-block'},
                                        width=4)
                            ], style={'padding-top': '15px'}),
                            dcc.Graph(id='app-two-figure-plot')
                        ])
                    ]
                ),
                dbc.Tab(
                    id='app-two-figure-table-tab',
                    label='Table',
                    tab_id='table',
                    children=[
                        html.Div(id='app-two-figure-table')
                    ]
                )
            ],
        ),
    )

    # app one metrics
    app_one_metrics = dbc.Col(
        [
            dbc.Card(app_one_figure1,
                     style={'height': '650px', 'padding': '10px'}),
            html.Hr(),

            dbc.Card(app_one_figure2,
                     style={'height': '650px', 'padding': '10px'})
        ]
    )

    # app one data
    app_one_data = dbc.Col(
        id='app-one-primary-data'
    )

    # app one content
    app_one_content = dbc.Col(
        [
            html.H3('App One Title', style=TEXT_STYLE),
            html.Hr(),

            # card deck
            app_one_card_deck,
            html.Hr(),

            dbc.Tabs(
                [
                    dbc.Tab(app_one_metrics, label='Metrics', style={'padding-top': '40px'}, tab_id='metrics'),
                    dbc.Tab(app_one_data, label='Data', style={'padding-top': '40px'}, tab_id='data')
                ]
            )
        ],
        width={'size': 8},
        style={'padding-left': '50px'}
    )

    # app two metrics
    app_two_metrics = dbc.Col(
        [
            dbc.Card(app_two_figure,
                     style={'height': '700px', 'padding': '10px'})
        ]
    )

    # app two data
    app_two_data = dbc.Col(
        id='app-two-primary-data',
        children=[
            html.Div(
                dash_table.DataTable(
                    id='app-one-figure1-data-table',
                    columns=[{'name': i, 'id': i} for i in data2.columns],
                    data=data2.to_dict('records'),

                    style_table={'overflowX': 'auto'},
                    style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                                'whiteSpace': 'normal'},
                    page_size=30,
                    filter_action='native',
                    sort_action='native')
            )
        ]
    )

    # app two content
    app_two_content = dbc.Col(
        [
            html.H3('App Two Title', style=TEXT_STYLE),
            html.Hr(),

            # card deck
            app_two_card_deck,
            html.Hr(),

            dbc.Tabs(
                [
                    dbc.Tab(app_two_metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                    dbc.Tab(app_two_data, label='Data', tab_id='data', style={'padding-top': '40px'})
                ]
            )
        ],
        width={'size': 8},
        style={'padding-left': '50px'}
    )

    # sidebar/content layout for each app
    app_one = dbc.Row([app_one_sidebar, app_one_content], style={'padding': '30px'})
    app_two = dbc.Row([app_two_sidebar, app_two_content], style={'padding': '30px'})

    # assemble apps in tabs
    app_tabs = dcc.Tabs(
        [
            dcc.Tab(
                label='The First App',
                children=app_one
            ),
            dcc.Tab(
                label='The Second App',
                children=app_two
            )
        ]
    )

    # DEFINE PRIMARY APP LAYOUT
    primary_app_content = dbc.Col(
        [
            html.H1('Multi-Tab Paged Dashboard', style=TITLE_TEXT_STYLE),

            html.Div(
                [
                    app_tabs
                ]
            )
        ]
    )

    # define the app layout after defining the other objects
    dash_app.layout = html.Div(primary_app_content)

    # initialize the callbacks using function below
    init_callbacks_multi_page(dash_app)

    return dash_app.server


def init_callbacks_multi_page(dash_app):

    # app one primary data
    @dash_app.callback(
        Output('app-one-primary-data', 'children'),
        [Input('app-one-submit-query', 'n_clicks')],
        [State('app-one-filter1', 'value'),
         State('app-one-filter2', 'value')]
    )
    def update_app_one_primary_data(n_clicks, cats, depts):
        tdata = data[data['Category'].isin(cats)]
        tdata = tdata[tdata['Department'].isin(depts)]

        table = dash_table.DataTable(
            id='app-one-primary-data-table',
            columns=[{'name': i, 'id': i} for i in tdata.columns],
            data=tdata.to_dict('records'),

            style_table={'overflowX': 'auto'},
            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        'whiteSpace': 'normal'},
            page_size=50,
            filter_action='native',
            sort_action='native')

        return table

    # app-one figure 1 plot and data
    @dash_app.callback(
        [Output('app-one-figure1-plot', 'figure'),
         Output('app-one-figure1-table', 'children')],
        [Input('app-one-figure1-dropdown', 'value')]
    )
    def update_app_one_figure_one(mask):
        tdata = data[data['Stage'] == mask]

        tdata.sort_values('Value1', inplace=True)
        tdata['Cat'] = tdata[['Category', 'Department']].apply(lambda x: ''.join(x.values.astype(str)), axis=1)
        fig = px.bar(tdata.loc[:10, :], x='Cat', y='Value1')

        table = dash_table.DataTable(
            id='app-one-figure1-data-table',
            columns=[{'name': i, 'id': i} for i in tdata.columns],
            data=tdata.to_dict('records'),

            style_table={'overflowX': 'auto'},
            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        'whiteSpace': 'normal'},
            page_size=10,
            filter_action='native',
            sort_action='native')

        return fig, table

    # app one figure 2 plot and data
    @dash_app.callback(
        [Output('app-one-figure2-plot', 'figure'),
         Output('app-one-figure2-table', 'children')],
        [Input('app-one-figure2-radio', 'value'),
         Input('app-one-figure2-dropdown', 'value')]
    )
    def update_app_one_figure_two(stage, x):

        tdata = data[data['Stage'] == stage]
        tdata = tdata.groupby(x)['Value1'].sum()
        x = list(tdata.index)


        fig = px.bar(x = x, y = tdata)

        tdata = tdata.reset_index()
        table = dash_table.DataTable(
            id='app-one-figure1-data-table',
            columns=[{'name': i, 'id': i} for i in tdata.columns],
            data=tdata.to_dict('records'),

            style_table={'overflowX': 'auto'},
            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        'whiteSpace': 'normal'},
            page_size=10,
            filter_action='native',
            sort_action='native')

        return fig, table

    # app two selected filters
    @dash_app.callback(
        [Output('app-one-selected-filters-card', 'children')],
        [Input('app-two-submit-query', 'n_clicks')],
        [State('app-one-filter1', 'value'),
         State('app-one-filter2', 'value')]
    )
    def update_app_two_selected_filters(n_clicks, mask1, mask2):
        return [
            html.P(f'Filter 1: {[i for i in mask1]}'),
            html.P(f'Filter 2: {[i for i in mask2]}')
        ]

    # app two selected filters
    @dash_app.callback(
        [Output('app-two-selected-filters-card', 'children')],
        [Input('app-two-submit-query', 'n_clicks')],
        [State('app-two-filter1', 'value'),
         State('app-two-filter2', 'value')]
    )
    def update_app_two_selected_filters(n_clicks, mask1, mask2):
        return [
            html.P(f'Filter 1: {[i for i in mask1]}'),
            html.P(f'Filter 2: {[i for i in mask2]}')
        ]

    # update app 2 figure and table
    @dash_app.callback(
        [Output('app-two-figure-plot', 'figure'),
         Output('app-two-figure-table', 'children')],
        [Input('app-two-timeframe-dropdown', 'value'),
         Input('app-two-by-list-dropdown', 'value'),
         Input('app-two-measure-dropdown', 'value')]
    )
    def update_app_two_figure(timeframe, by, measure):
        if timeframe == 'All Years':
            tdf = data2
        else:
            tdf = data2[data2['WO Actual Finish Year'] == timeframe]

        series = tdf.groupby(by)[measure].sum().sort_values(ascending=False)[:10]

        title = f'Top {measure} by {by} for {timeframe}'

        fig = go.Figure(data=[go.Bar(x=series.index, y=series.values)])

        fig.update_layout(title=title, yaxis_title=measure, height=550)

        max_size = max([len(i) for i in series.index])

        if max_size > 32:
            fig.update_layout(xaxis={'tickfont': {'size': 10}})

        table = dash_table.DataTable(
            id='app-one-figure1-data-table',
            columns=[{'name': i, 'id': i} for i in tdf.columns],
            data=tdf.to_dict('records'),

            style_table={'overflowX': 'auto'},
            style_cell={'height': 'auto', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                        'whiteSpace': 'normal'},
            page_size=10,
            filter_action='native',
            sort_action='native')

        return fig, table
