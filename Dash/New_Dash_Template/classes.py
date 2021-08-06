#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""This module provides custom classes to create dash/flask applications."""


# imports
from pandas import DataFrame
from copy import deepcopy
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table


class Styles:
    def __init__(self):
        self.__repr__ = 'Custom css styles for dash app.'
        self.title_text = {
            'color':  '#191970'
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
            'background-color':  '#f8f9fa'
        }
        self.dash_title_text = {
            'textAlign': 'center',
            'color':  '#191970',
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
            'color':  '#191970'
        }
        self.dash_card_text = {
            'textAlign': 'center',
            'color':  '#0074D9'
        }


class DashboardControls:
    """Class that creates and manages a set of dashboard controls.

    Usage:
        Create a new instance of DashboardControls for each dashboard. Add form groups or controls
        as needed. Access those objects from the DashboardControls object using its name.

        This class should be imported to the controls module, where instances can be created within factory functions
        for the app. Those factory functions can be imported to the layout module to generate their instances
        and to assemble the app layout.

    """

    def __init__(self, name):
        self.name = name
        self.controls = {}
        self.form_groups = {}

    def __repr__(self):
        return f'Dashboard Controls for {self.name}'

    def add_control(self, control_name, control_label, control):
        self.controls[control_name] = {
            'label': control_label,
            'control': control
        }

    def get_control(self, control_name):
        if control_name not in self.controls.keys():
            raise KeyError(f'control name not found. has the control been added to {self.name}?')
        else:
            return self.controls[control_name]

    def add_form_group(self, form_group_name, form_group):
        self.form_groups[form_group_name] = form_group

    def get_form_group(self, form_group_name):
        if form_group_name not in self.form_groups.keys():
            raise KeyError(f'form group name not found. has the form group been added to {self.name}?')
        else:
            return self.form_groups[form_group_name]


class DashboardFigures:
    def __init__(self, name):
        self.name = name
        self.figures = {}
        self.tables = {}

    def __repr__(self):
        return f'Dashboard Figures for {self.name}'

    def add_figure(self, figure_name, figure):
        self.figures[figure_name] = figure

    def get_figure(self, figure_name):
        if figure_name not in self.figures.keys():
            raise KeyError(f'figure name not found. has the figure been added to {self.name}?')
        else:
            return self.figures[figure_name]

    def add_table(self, table_name, table):
        self.tables[table_name] = table

    def get_table(self, table_name):
        if table_name not in self.figures.keys():
            raise KeyError(f'table name not found. has the table been added to {self.name}?')
        else:
            return self.tables[table_name]


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

            # new styling
            style_header={'whiteSpace': 'normal'},
            fixed_rows={'headers': True},
            style_table={'height': '400px'},
            virtualization=True,
            style_cell={'minWidth': cell_width},
            export_format='csv'

            # old styling
            # define table layout
            # style_cell={'minWidth': cell_width,
            #             'width': cell_width,
            #             'maxWidth': cell_width},
            # style_table={'overflowX': 'auto'},
            
            # page_size=page_size)
        )

        return table
