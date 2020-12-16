#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The layouts module assembles the layout for each dash app and returns a dash.layout object.
These objects are organized into dashboards in the dashboard module."""

# imports
from .data import DataFuncs
from .controls import single_page_db_controls, multi_page_db_controls
from .figures import single_page_figures
from .styles import Styles

import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# instantiate datafuncs and styles
datafuncs = DataFuncs()
styles = Styles()

# GLOBAL OBJECTS
# flask navigation
navigation_title = html.H2('Navigation', style=styles.dash_text)
go_home = html.A('Application Home', href="/", style=styles.dash_text)
back_to_dashboards = html.A('Back to Dashboards', href="/dashboards", style=styles.dash_text)
# dataframes and lists
df3 = datafuncs.get_gapminder_data()
data = datafuncs.create_dataframe()
data2 = datafuncs.get_data()
data2 = datafuncs.format_dataframe(data2)
data_canada, data_usa, years = datafuncs.extract_gapminder_objects(df3)


def create_single_page_app_layout():
    # SIDEBAR
    # define the sidebar content
    param_sidebar = html.Div(
        [
            html.H2('Parameters', style=styles.dash_text),
            html.Hr(),
            single_page_db_controls.form_groups['sidebar_form_group']
        ],
        style=styles.sidebar_single_page
    )

    nav_sidebar = html.Div(
        [
            navigation_title,
            html.Hr(),
            go_home,
            html.Br(),
            back_to_dashboards
        ],
        style=styles.sidebar_single_page
    )

    sidebar = dbc.Col([nav_sidebar, param_sidebar], style={'position': 'fixed'})

    # DASHBOARD CONTENT

    # 1. Cards and Card Decks

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
                html.P(id='card3_content', className='card-text'),
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
                html.Div(id='card4_content', className='card-text'),
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

    # Canada data plot/table
    figure1 = dbc.Col(
        dbc.Tabs(
            id='figure1_plot',
            children=[
                dbc.Tab(
                    id='plot',
                    label='Plot',

                    # figure added directly here (not using a callback)
                    children=[dcc.Graph(id='metrics_graph1', figure=single_page_figures.figures['figure1'])]
                ),
                dbc.Tab(
                    id='figure1_table',
                    label='Table',

                    # table added directly here (not using a callback)
                    children=[single_page_figures.tables['table1']]
                )
            ]
        ),
        md=6
    )

    # US data plot/table
    figure2 = dbc.Col(
        dbc.Tabs(
            id='figure2_plot',
            children=[
                dbc.Tab(
                    id='plot2',
                    label='Plot',
                    children=[dcc.Graph(id='metrics_graph2', figure=single_page_figures.figures['figure2'])]
                ),
                dbc.Tab(
                    id='figure2_table',
                    label='Table',
                    children=[single_page_figures.tables['table2']]
                )
            ]
        ),
        md=6
    )

    # gapminder plot/table
    figure3 = dbc.Col(
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
                            single_page_db_controls.controls['year_slider']['control']
                        ])
                    ]
                ),
                dbc.Tab(
                    id='figure3_table',
                    label='Table'
                    # figure set in a callback
                )
            ]
        )
    )

    # this is the primary layout for metrics tab (main app area)
    # each 'figure' below consists of a tabbed layout of Plot/Table
    metrics_tab = dbc.Tab(
        id='metrics',
        label='Metrics',

        # metrics objects here
        # use dbc.Row and/or dbc.Col to organize objects
        children=[
            dbc.Row([figure1, figure2], style={'padding-top': '30px'}),
            dbc.Row([figure3], style={'padding-top': '30px'})
        ]
    )

    # setup primary data table here
    data_tab = dbc.Tab(
        id='data',
        label='Data',

        # this is the primary data table
        children=[
            dbc.Row(dbc.Col(
                single_page_figures.tables['primary_table']
            ))
        ]
    )

    # using cards for the first row where values can be displayed
    content_first_row = dbc.Row([

        # the card deck that can be used to display values
        dbc.Col(fr_card_deck)

    ])

    # primary layout using a tabbed design
    content_primary_tab_design = dbc.Row(
        dbc.Col(
            dbc.Tabs(
                id='primary-content',

                # add tabs here
                children=[
                    metrics_tab,
                    data_tab
                ]
            )
        )
    )

    # this is the 'content' of the app, or everything that's not part of the sidebar
    # this design uses rows to organize main app content
    content = dbc.Col(
        [
            html.H2('Dashboard Title', style=styles.dash_text),
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
        style=styles.dash_content
    )

    return sidebar, content


# create the multi page app layout
def create_multi_page_app_layout():
    # sidebars
    nav_sidebar = html.Div(
        [
            html.H2('Navigation', style=styles.dash_text),
            html.Hr(),
            go_home,
            html.Br(),
            back_to_dashboards
        ],
        style={'padding-top': '15px', 'padding-bottom': '30px'},
    )

    app_one_param_sidebar = html.Div(
        [
            html.H2('App One Parameters', style=styles.dash_text),
            html.Hr(),
            multi_page_db_controls.form_groups['app_one_form_group']
        ],
    )

    app_two_param_sidebar = html.Div(
        [
            html.H2('App Two Parameters', style=styles.dash_text),
            html.Hr(),
            multi_page_db_controls.form_groups['app_two_form_group']
        ],
    )

    app_one_sidebar = dbc.Col([nav_sidebar, app_one_param_sidebar],
                              style=styles.sidebar_multi_page,
                              width={'size': 3})
    app_two_sidebar = dbc.Col([nav_sidebar, app_two_param_sidebar],
                              style=styles.sidebar_multi_page,
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
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_one_figure1_dropdown']['label'],
                                        multi_page_db_controls.controls['app_one_figure1_dropdown']['control']
                                    ],
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
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_one_figure2_radio']['label'],
                                        multi_page_db_controls.controls['app_one_figure2_radio']['control']
                                    ],
                                    style={'display': 'inline-block'},
                                    width=3),
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_one_figure2_dropdown']['label'],
                                        multi_page_db_controls.controls['app_one_figure2_dropdown']['control']
                                    ],
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
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_two_timeframe_dropdown']['label'],
                                        multi_page_db_controls.controls['app_two_timeframe_dropdown']['control']
                                    ],
                                    style={'display': 'inline-block'},
                                    width=3),
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_two_by_list_dropdown']['label'],
                                        multi_page_db_controls.controls['app_two_by_list_dropdown']['control']
                                    ],
                                    style={'display': 'inline-block'},
                                    width=4),
                                dbc.Col(
                                    [
                                        multi_page_db_controls.controls['app_two_measure_dropdown']['label'],
                                        multi_page_db_controls.controls['app_two_measure_dropdown']['control']
                                    ],
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
    app_one_metrics = dbc.Row(dbc.Col(
        [
            dbc.Card(app_one_figure1,
                     style={'height': '650px', 'padding': '10px'}),
            html.Hr(),

            dbc.Card(app_one_figure2,
                     style={'height': '650px', 'padding': '10px'})
        ]
    ))

    # app one data
    app_one_data = dbc.Row(dbc.Col(
        id='app-one-primary-data'
    ))

    # app one content
    app_one_content = dbc.Col(
        [
            html.H3('App One Title', style=styles.dash_text),
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
    app_two_metrics = dbc.Row(dbc.Col(
        [
            dbc.Card(app_two_figure,
                     style={'height': '700px', 'padding': '10px'})
        ]
    ))

    # app two data
    app_two_data = dbc.Row(dbc.Col(
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
    ))

    # app two content
    app_two_content = dbc.Col(
        [
            html.H3('App Two Title', style=styles.dash_text),
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
            html.H1('Multi-Tab Paged Dashboard', style=styles.dash_title_text),

            html.Div(
                [
                    app_tabs
                ]
            )
        ]
    )

    return primary_app_content
