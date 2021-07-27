#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""This module defines the layout for each dashboard.

Each create_layout_ function must be called in the init_dashboard_ function in the dashboard.py module."""

# imports
import base64
import os

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

try:
    import app.plotlydash.controls as controls
    import app.plotlydash.data as data
    import app.plotlydash.figures as figures
    from app.utility_scripts import dash_tools as tools
except ModuleNotFoundError:
    import controls
    import data
    import figures
    import dashtools as tools

from werkzeug.utils import import_string

# create an instance of the config class
try:
    cfg = import_string(os.getenv('CONFIG_CLASS'))()
except:
    import fallback_config as fc

    config = os.getenv('CONFIG_CLASS')
    if config == 'config.ProdConfig':
        cfg = fc.ProdConfig()
    elif config == 'config.TestConfig':
        cfg = fc.TestConfig()
    else:
        cfg = fc.DevConfig()

# create any data global objects
styles = tools.DashStyles()


# main blanket tracking dashboard overview layout
def create_layout_page1():
    """The create_layout_ function for the main dashboard.

    :return: returns the sidebars and content objects needed for this layout.
    """

    # cards
    card1 = [
        dbc.CardHeader('Card 1'),
        dbc.CardBody(
            [
                html.Div(id='car1')
            ]
        )
    ]

    # overview page metrics
    metrics = [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='an-id-for-a-callback')
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dbc.Card(
                            card1,
                            style={'background-color': '#ebf5e9'}
                        ), style={'padding-top': '10px'}
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(dbc.CardBody(dcc.Graph(id='a-plot-for-callbacks'))),
                            style={'margin-top': '12px'}
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('More Content')
                    ]
                )
            ], style={'margin-top': '10px'}
        )
    ]

    # primary data
    primary_data = dbc.Row(
        dbc.Col(
            id='primary-data'
        )
    )

    Content = dbc.Col(
        [
            html.H3('Page Title', style=styles.dash_text),
            html.Hr(),

            dbc.CardDeck([card1]),
            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                dbc.Button(
                                    'Download csv',
                                    id='download-data',
                                    color='primary'
                                ),
                                style={'display': 'inline-block'}
                            ),
                            html.Div(
                                'Right-click and open link in new tab to download data',
                                style={'display': 'inline-block', 'margin-left': '15px'}
                            )
                        ]
                    )
                ]
            ),
            html.Hr(),

            dbc.Tabs(
                [
                    dbc.Tab(metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                    dbc.Tab(primary_data, label='Data', tab_id='data', style={'padding-top': '40px'})
                ],
                active_tab='metrics'
            )
        ],
        width={'size': 8},
        style={'padding-left': '50px', 'padding-right': '50px', 'padding-top': '0.5em', 'margin-top': '15px'}
    )

    return controls.sidebar, content


# the dashboard resources page
def create_dashboard_resources_layout():
    """This function creates the layout for the dashboard resources page and returns its content."""

    # title row
    title_row = dbc.Row(
        [
            dbc.Col(
                [
                    html.H3('Dashboard Resources', style=styles.title_text),
                    html.Hr()
                ]
            )
        ]
    )

    info_card_deck = dbc.CardDeck(
        [
            # Links Card
            dbc.Card(
                [
                    dbc.CardHeader('Useful Links'),
                    dbc.CardBody(
                        [
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            html.A(
                                                style={'display': 'inline-block', 'padding-right': '10px'}
                                            ),
                                            html.Div('(Permissions Required)', style={'display': 'inline-block'})
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.A(
                                                style={'display': 'inline-block', 'padding-right': '10px'}
                                            ),
                                            html.Div('(Permissions Required)', style={'display': 'inline-block'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ],
            ),

            # page descriptions card
            dbc.Card(
                [
                    dbc.CardHeader('Dashboard Page Content'),
                    dbc.CardBody(
                        [
                            html.Strong('Page 1 (Overview)'),
                            html.P('- Page 1 Stuff'),
                            # html.Br(),
                            html.Strong('Dashboard Resources'),
                            html.P('- Links and Useful Information')
                        ]
                    )
                ]
            ),
            
            # download help card
            dbc.Card(
                [
                    dbc.CardHeader('Download .csv Help'),
                    dbc.CardBody(
                        [
                            html.P('Always right-click and open Download csv links in new tab.'),
                            html.P('If downloads are not exporting correctly, try clearing your browser cache.')
                        ]
                    )
                ]
            ),

            # shameless plug card
            dbc.Card(
                [
                    dbc.CardHeader('Need Advanced Analytics?'),
                    dbc.CardBody(
                        [
                            html.P(
                                'Just Contact Us.')
                        ]
                    )
                ]
            ),

            # about app card
            # figures.make_about_app_card('72c7cb03-b899-4de2-8d74-f7b04d7688d7')
        ]
    )

    # info row
    info_row = dbc.Row(
        [
            dbc.Col(
                [
                    info_card_deck
                ]
            )
        ]
    )

    # assemble the final rows into a list
    content = html.Div(
        [
            title_row,
            info_row
        ], style={'padding': '10px'}
    )

    return content


# create layout function to create the main page layout
def create_layout():
    if 'plotlydash' in cfg.APPLICATION_HOME:
        logo = ''.join([cfg.APPLICATION_HOME, '/images/sclogo_no_background.png'])
    else:
        logo = ''.join([cfg.APPLICATION_HOME, '/app/', cfg.STATIC_FOLDER, '/images/sclogo_no_background.png'])
    try:
        logo_base64 = base64.b64encode(open(logo, 'rb').read()).decode('ascii')
    except FileNotFoundError:
        logo = 'images/sclogo_no_background.png'
        logo_base64 = base64.b64encode(open(logo, 'rb').read()).decode('ascii')

    layout = html.Div(
        [
            # represents the URL bar, doesn't render anything, needed for navbar functionality
            dcc.Location(id='url', refresh=False),

            dbc.Row(
                dbc.Col(
                    dbc.Navbar(
                        [
                            html.A(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Img(src=f'data:image/png;base64,{logo_base64}',
                                                     style={'height': '40px'}),
                                            style={'background': 'white', 'padding': '5px'}
                                        ),
                                        dbc.Col(
                                            dbc.NavbarBrand(
                                                'Dashboard Title',
                                                className='ml-2',
                                                style={
                                                    'padding-left': '1em'
                                                }
                                            )
                                        )
                                    ],
                                    align='center',
                                    no_gutters=True
                                ),
                                href='/'
                            ),
                            dbc.NavbarToggler(id='navbar-toggler'),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(
                                            dbc.NavbarBrand(
                                                'Navigation'
                                            )
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                'Page 1',
                                                href='/',
                                                className='btn btn-primary',
                                                style={'margin-right': '10px'}
                                            )
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                'Page 2',
                                                href='/page2',
                                                className='btn btn-primary',
                                                style={'margin-right': '10px'}
                                            )
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                'Dashboard Resources',
                                                href='/dashboard_resources',
                                                className='btn btn-primary',
                                                style={'margin-right': '10px'}
                                            )
                                        )
                                    ], style={'position': 'absolute', 'right': '10px'}
                                ),
                                id='navbar-collapse',
                                navbar=True
                            )
                        ],
                        color='dark',
                        dark=True
                    )
                )
            ),
            html.Hr(),
            html.Div(
                id='page-content',
            )
        ]
    )

    return layout
