#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""dash_tools module containing objects frequently used in Dash applications."""

from pandas import DataFrame
from copy import deepcopy
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table


class DashDF(DataFrame):
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
        if type(column_names) == str:
            if column_names in cols:
                self[column_names] = self[column_names].apply(lambda x: '{:.2f} %'.format(x))
            else:
                raise KeyError(f'{column_names} not found in dataframe columns.')
        elif type(column_names) == list:
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
    def get_formatted_dash_table(self, header=True, sort_cols=None, ascending=True):

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
            striped=True
        )

        return table

    # get interactive dash table
    def get_interactive_dash_table(self, cell_width='150px', page_size=10, sort_cols=None, ascending=True):

        if sort_cols:
            data = self.sort_values(sort_cols, ascending=ascending).to_dict('records')
        else:
            data = self.to_dict('records')

        table = dash_table.DataTable(

            # define the data
            columns=[{'name': i, 'id': i} for i in self.columns],
            data=data,

            # define filter and sort behavior
            filter_action='native',
            sort_action='native',

            # define table layout
            style_cell={'minWidth': cell_width,
                        'width': cell_width,
                        'maxWidth': cell_width},
            style_table={'overflowX': 'auto'},
            page_size=page_size)

        return table


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
        self.dash_title_text = {
            'textAlign': 'center',
            'color': '#191970',
            'margin-top': '30px',
            'margin-bottom': '20px'
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
                    children=[table_content]
                )
            ]
        ), md=md
    )

    return figure
