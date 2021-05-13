#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""dash_tools module containing objects frequently used in Dash applications."""
from abc import ABC

from pandas import DataFrame
from copy import deepcopy
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table


# functions to create layout objects
# create card function
def create_card(title, div_id, card_id, color='light', outline=False, inverse=False, content=None):
    """This function creates and returns a dbc.Card object.

    :param title: The card title
    :param div_id: The html id for the div component of the card content. Used to update card content in callbacks.
    :param card_id: The html id for the card. Used to change card color in callbacks.
    :param color: default = 'light': One of 'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light',
                  'dark'.
    :param outline: boolean: default = False: Whether or not 'color' only applied to the card outline.
    :param inverse: boolean: default = False: Whether card text color is black (False) or white (True).
    :param content: default = None: The content to display on the card. If all card content is set by a callback, leave
                    as None.
    :return: Returns a dbc.Card object.
    """
    if content:
        body = dbc.CardBody(
            [
                html.Div(
                    children=[content],
                    id=div_id,
                    className='card-text'
                )
            ]
        )
    else:
        body = dbc.CardBody(
            [
                html.Div(
                    id=div_id,
                    className='card-text'
                )
            ]
        )

    card_layout = [
        dbc.CardHeader(title),
        dbc.CardBody(
            body
        )
    ]

    card = dbc.Card(card_layout, id=card_id, color=color, outline=outline, inverse=inverse)

    return card


# create a tabbed figure with Plot and Table tabs
def make_dash_figure(plot_content, table_content, table_id, md):
    """Assembles plot content and table content into a tabbed layout for a figure.

    :param plot_content: The 'children' value for the plot tab. Should be a dcc.Graph() object or an html.Div() object
                         containing a figure such as controls and dcc.Graph(). The html_id for the plot_content must be
                         set outside this function.
    :param table_content: The 'children' value for the table tab. Can contain an html.Div with a table or be None for
                          use with callbacks
    :param table_id: The html_id of the table to be used for callbacks
    :param md: The md value to set the width of the figure (integer 0-12)
    :return: Returns a dbc.Col object containing a tabbed layout (Plot/Table)
    """

    figure = dbc.Col(
        dbc.Tabs(
            children=[
                dbc.Tab(
                    label='Plot',
                    children=[
                        plot_content
                    ]
                ),
                dbc.Tab(
                    label='Table',
                    id=table_id,
                    children=[
                        table_content
                    ]
                )
            ]
        ), md=md
    )

    return figure


# classes
class DashDF(DataFrame, ABC):
    """Dash dataframe class. This is built on a pandas dataframe and adds some commonly used features for dash apps.

    Methods
    -------
        convert_currency(column_names):
            Supply a single column or a list of columns with numeric data types, and this method will format them as
            strings with a currency format of $1,234.56.

        convert_percent(column_names):
            Supply a single column or a list of columns with numeric data types, and this method will format them as
            strings with a percent format of 12.34%.

        get_formatted_dash_table(header=True, sort_cols=None, ascending=True):
            Returns a static formatted dash bootstrap component table object. You can't filter or sort this table,
            so sort the dataframe first. Options to provide a column or list of columns by which to sort.

        get_interactive_dash_table(cell_width='150px', page_size=10, sort_cols=None, ascending=True):
            Returns a dash_table object that can be filtered and sorted. Options to provide a column or list of
            columns by which to sort.

    """

    # ensure that this class does not modify the original dataframe
    def __init__(self, df):
        super().__init__(deepcopy(df))

    # convert currency method
    def convert_currency(self, column_names):
        cols = self.columns
        if type(column_names) == str:
            if column_names in cols:
                self[column_names] = self[column_names].apply(lambda x: '${:,.2f}'.format(x))
            else:
                raise KeyError(f'{column_names} not found in dataframe columns.')
        elif type(column_names) == list:
            for column in column_names:
                if column in cols:
                    self[column] = self[column].apply(lambda x: '${:,.2f}'.format(x))
                else:
                    raise KeyError(f'{column} not found in dataframe columns.')
        else:
            raise TypeError(
                'column_names must be a string with the name of a column or a list of column names as strings.'
            )

    # convert percent method
    def convert_percent(self, column_names):
        cols = self.columns
        if isinstance(column_names, str):
            if column_names in cols:
                self[column_names] = self[column_names].apply(lambda x: '{:.2f} %'.format(x))
            else:
                raise KeyError(f'{column_names} not found in dataframe columns.')
        elif isinstance(column_names, list):
            for column in column_names:
                if column in cols:
                    self[column] = self[column].apply(lambda x: '{:.2f} %'.format(x))
                else:
                    raise KeyError(f'{column} not found in dataframe columns.')
        else:
            raise TypeError(
                'column_names must be a string with the name of a column or a list of column names as strings.'
            )

    # get dash data table function
    # this function returns a formatted table that is NOT interactive but looks nice
    # use for rendering tables with relatively few rows and columns
    def get_formatted_dash_table(self, header=True, sort_cols=None, ascending=True, size='md'):

        if sort_cols:
            data = self.sort_values(sort_cols, ascending=ascending)
        else:
            data = self

        rows, cols = self.shape

        if header:
            table_header = html.Thead(
                html.Tr([html.Td(i) for i in self.columns])
            )
        else:
            table_header = None

        table_body = html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(data.iloc[row, col]) for col in range(cols)
                    ]
                ) for row in range(rows)
            ]
        )

        table = dbc.Table(
            [table_header, table_body],
            bordered=True,
            hover=True,
            striped=True,
            size=size
        )

        return table

    # get interactive dash table
    def get_interactive_dash_table(self, cell_width='150px', page_size=10, sort_cols=None, ascending=True):

        if sort_cols:
            data = self.sort_values(sort_cols, ascending=ascending).to_dict('records')
        else:
            data = self.to_dict('records')

        long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in self.columns if
                             len(column) >= 30]
        med_column_names = [{"if": {"column_id": column}, "min-width": "250px"} for column in self.columns if
                            (len(column) > 15 and len(column)) < 30]
        small_column_names = [{"if": {"column_id": column}, "min-width": "150px"} for column in self.columns if
                              len(column) <= 15]

        adjusted_columns = long_column_names + med_column_names + small_column_names

        table = dash_table.DataTable(

            # define the data
            columns=[{'name': i, 'id': i} for i in self.columns],
            data=data,

            # tooltip_data=[
            #     {
            #         column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()
            #     } for row in data
            # ],
            # tooltip_duration=None,

            # define filter and sort behavior
            filter_action='native',
            sort_action='native',

            # define table layout
            # style_cell={'minWidth': cell_width,
            #             'width': cell_width,
            #             'maxWidth': cell_width},
            style_table={'overflowX': 'auto'},
            # style_data={''},

            style_cell_conditional=adjusted_columns,

            page_size=page_size)

        return table


# assemble multi-page/tab app content
def make_primary_content(metrics, data, title, width=None, primary_card_deck=None, multi=True):
    """

    :param width:
    :param metrics:
    :param data:
    :param title:
    :param primary_card_deck:
    :param multi:
    :return: primary content (metrics/data) tabs for the dashboard page
    """

    # set default width
    if not width:
        width = {'size': 8}

    if multi:
        # organize content for a multi page/tab dash app
        if primary_card_deck:
            content = dbc.Col(
                [
                    html.H3(title, style=styles.dash_text),
                    html.Hr(),

                    primary_card_deck,
                    html.Hr(),

                    dbc.Tabs(
                        [
                            dbc.Tab(metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                            dbc.Tab(data, label='Data', tab_id='data', style={'padding-top': '40px'})
                        ],
                        active_tab='metrics'
                    )
                ],
                width=width,
                style={'padding-left': '50px', 'padding-right': '50px', 'padding-top': '0.5em', 'margin-top': '15px'}
            )
        else:
            content = dbc.Col(
                [
                    html.H3(title, style=styles.dash_text),
                    html.Hr(),

                    dbc.Tabs(
                        [
                            dbc.Tab(metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                            dbc.Tab(data, label='Data', tab_id='data', style={'padding-top': '40px'})
                        ],
                        active_tab='metrics'
                    )
                ],
                width=width,
                style={'padding-left': '50px', 'padding-right': '50px', 'padding-top': '0.5em', 'margin-top': '15px'}
            )
    else:
        # organize content for a single page/tab dash app
        if primary_card_deck:
            content = dbc.Col(
                [
                    html.H2(title, style=styles.dash_content_title_text),
                    html.Hr(),

                    primary_card_deck,

                    html.Hr(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Tabs(
                                [
                                    dbc.Tab(metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                                    dbc.Tab(data, label='Data', tab_id='data', style={'padding-top': '40px'})
                                ],
                                active_tab='metrics'
                            )
                        )
                    )
                ],
                style=styles.dash_content
            )
        else:
            content = dbc.Col(
                [
                    html.H2(title, style=styles.dash_content_title_text),
                    html.Hr(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Tabs(
                                [
                                    dbc.Tab(metrics, label='Metrics', tab_id='metrics', style={'padding-top': '40px'}),
                                    dbc.Tab(data, label='Data', tab_id='data', style={'padding-top': '40px'})
                                ],
                                active_tab='metrics'
                            )
                        )
                    )
                ],
                style=styles.dash_content
            )

    return content


class DashStyles:
    """This class contains dictionaries for easy styling of dash components."""

    def __init__(self):
        self.__repr__ = 'Custom css styles for dash app.'
        self.title_text = {
            'color': '#191970'
        }
        self.sidebar_single_page = {
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '20%',
            'padding': '20px 10px',
            'background-color': '#f8f9fa'
        }
        self.sidebar_multi_page = {
            'background-color': '#f8f9fa'
        }
        self.sidebar_column = {
            'background-color': '#f8f9fa',
            'margin': '10px'
        }
        self.sidebar_title = {
            'textAlign': 'center',
            'color': '#191970',
            'padding-top': '0.5em',
            'padding-left': '1em',
            'padding-right': '1em'
        }
        self.dash_title_text = {
            # 'textAlign': 'center',
            'color': '#191970',
            'margin-top': '30px',
            'margin-bottom': '20px'
        }
        self.dash_content_title_text = {
            'margin-top': '10px',
            'textAlign': 'center',
            'color': '#191970',
            'padding-top': '0.5em'
        }
        self.dash_content = {
            'margin-left': '25%',
            'margin-right': '5%',
            'top': 0,
            'padding': '20px 10px'
        }
        self.dash_text = {
            'textAlign': 'center',
            'color': '#191970'
        }
        self.dash_card_text = {
            'textAlign': 'center',
            'color': '#0074D9'
        }


# LAYOUT Classes relying on DashStyles
# create class instances
styles = DashStyles()

# navigation variables
navigation_title = html.H2('Navigation', style=styles.dash_text)
go_home = html.A('Application Home', href='/', style=styles.dash_text)
back_to_dashboards = html.A('Back to Dashboards', href='/dashboards', style=styles.dash_text)


# sidebars class
class DashboardSidebars:
    """A separate instance of this class should be created for each dashboard.

        IMPORTANT:
            The 'name' parameter for each content object should match the 'name' parameter for its associated
            sidebar object in the DashboardContent instance, and should be the name you want to appear on the tab
            if using a multi-page app.
    """

    def __init__(self):
        self.__repr__ = 'Sidebars for the dashboard.'

        # set a standard navigation section for Flask apps
        self.__nav = html.Div(
            [
                navigation_title,
                html.Hr(),
                go_home,
                html.Br(),
                back_to_dashboards
            ], style={'padding-top': '15px', 'padding-bottom': '30px'}
        )

    # allow creation of attributes to add fully developed sidebar objects as attributes
    def add_sidebar(self, name, sidebar):
        if not isinstance(name, str):
            raise TypeError('the name parameter must be a string')
        if not isinstance(sidebar, dbc.Col):
            raise TypeError(f'the sidebar parameter must be an instance of "dbc.Col()"')
        setattr(self, name, sidebar)

    # allow creation of sidebars that also use the nav component in Flask apps
    def add_sidebar_w_nav(self, name, parameters, multi=True):
        if not isinstance(name, str):
            raise TypeError('the name parameter must be a string')
        if not isinstance(parameters, html.Div):
            raise TypeError('the parameters passed must be an html.Div()')
        if multi:
            sidebar = dbc.Col(
                [self.__nav, parameters],
                style=styles.sidebar_multi_page,
                width={'size': 3}
            )
        else:
            sidebar = dbc.Col(
                [self.__nav, parameters],
                style={'position': 'fixed'}
            )
        # set the attribute
        setattr(self, name, sidebar)

    # return a list of sidebar names
    def list_sidebars(self):
        """
        :return: returns the attribute names for all of the sidebar objects stored in the instance
        """
        return [key for key, value in self.__dict__.items() if isinstance(value, dbc.Col)]

    # return the actual sidebars
    def get_sidebars(self):
        """
        :return: returns all of the sidebar objects stored in the instance
        """
        return [value for key, value in self.__dict__.items() if isinstance(value, dbc.Col)]


# content class
class DashboardContent:
    """A separate instance of this class should be created for each dashboard.

    IMPORTANT:
        The 'name' parameter for each content object should match the 'name' parameter for its associated
        sidebar object in the DashboardSidebar instance, and should be the name you want to appear on the tab
        if using a multi-page app.
    """

    def __init__(self):
        self.__repr__ = 'Content for the dashboard.'

    # allow creation of content attributes
    def add_content(self, name, content):
        if not isinstance(name, str):
            raise TypeError('the name parameter must be a string')
        if not isinstance(content, dbc.Col):
            raise TypeError('the content must be an instance of "dbc.Col()"')
        setattr(self, name, content)

    # return a list of content attribute names
    def list_contents(self):
        """
        :return: returns the attribute names for all of the content objects stored in the instance
        """
        return [key for key, value in self.__dict__.items() if isinstance(value, dbc.Col)]

    # return the actual contents
    def get_contents(self):
        """
        :return: returns all of the content objects stored in the instance
        """
        return [value for key, value in self.__dict__.items() if isinstance(value, dbc.Col)]


# application layout function
def create_layout(paging, sidebars, contents, objects, main_title=None):
    """This function creates and returns the layout for a dash app.

    :param paging: either 'multi' or 'single' to designate whether the primary dash app has multiple pages/tabs
    :param sidebars: an instance of the DashboardSidebars class
    :param contents: an instance of the DashboardContent class
    :param objects: a string or a list of attribute names to extract for the dashboard.
                    this value must represent attributes added to the sidebars/contents objects using the
                    .add_sidebar() and .add_content() methods.

                    in the case of multi-page/tab apps, this list is also the name of the primary tabs.
    :param main_title: the main title for the dashboard. only used/required for multi-page/tab layouts
    :return: returns the layout for the dash app
    """

    if paging == 'single':
        if not isinstance(objects, str):
            raise TypeError('attr_name must be a string if designing a single page layout')
        if objects not in sidebars.list_sidebars() or objects not in contents.list_contents():
            raise ValueError('attr_name not found in both sidebars and contents objects')

        layout = dbc.Row(
            [
                sidebars.__getattribute__(objects),
                contents.__getattribute__(objects)
            ],
            style={'padding': '30px'}
        )

    elif paging == 'multi':
        if not isinstance(objects, list):
            raise TypeError('attr_name must be a list of strings.')
        if not main_title:
            raise ValueError('main_title is required for multi page layouts.')

        tabs = []
        for obj in objects:
            if not isinstance(obj, str):
                raise TypeError('attr_name must be a list of strings.')
            if obj not in sidebars.list_sidebars() or obj not in contents.list_contents():
                raise ValueError('every attribute name in attr_name must be an in both sidebars and contents')

            # create tabs for each attribute in the obj list
            tabs.append(
                dcc.Tab(
                    label=obj,
                    children=[
                        dbc.Row(
                            [
                                sidebars.__getattribute__(obj),
                                contents.__getattribute__(obj)
                            ],
                            style={'padding': '30px'}
                        )
                    ]
                )
            )

        layout = html.Div(
            dbc.Col(
                [
                    html.H1(main_title, style=styles.dash_title_text),

                    html.Div(
                        [
                            dcc.Tabs(tabs)
                        ]
                    )
                ]
            )
        )
    else:
        raise ValueError('paging must either be "single" or "multi"')

    return layout
