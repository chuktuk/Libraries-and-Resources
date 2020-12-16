#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The figures module contains objects needed to generate the figures and tables for all dashboards."""

from copy import deepcopy

import dash_table

import plotly.express as px
import plotly.graph_objects as go

from .data import DataFuncs

# instantiate datafuncs
datafuncs = DataFuncs()

# global data and list objects
df3 = datafuncs.get_gapminder_data()
data1 = datafuncs.create_dataframe()
data2 = datafuncs.get_data()
data2 = datafuncs.format_dataframe(data2)
data_canada, data_usa, years = datafuncs.extract_gapminder_objects(df3)


# class definition
class DashboardFigures:
    def __init__(self, name):
        self.name = name
        self.figures = {}
        self.tables = {}

    def __repr__(self):
        return f'Dashboard Figures for {self.name}'

    def add_figure(self, figure_name, figure):
        if figure_name not in self.figures:
            self.figures[figure_name] = figure

    def add_table(self, table_name, table):
        if table_name not in self.tables:
            self.tables[table_name] = table


# SINGLE PAGE DASHBOARD FIGURE FUNCTIONS
# PLOTS
# figure1 plot
def plot_figure1():
    fig1 = px.bar(
        data_canada,
        x='year',
        y='pop',
        hover_data=['lifeExp', 'gdpPercap'],
        color='lifeExp',
        labels={'pop': 'population of Canada'}
    )
    fig1.update_layout(title='Canada Population (Bars) and Life Expectancy (Color) Over Time', titlefont={'size': 12})
    return fig1


# figure2 plot
def plot_figure2():
    fig2 = px.bar(
        data_usa,
        x='year',
        y='pop',
        hover_data=['lifeExp', 'gdpPercap'],
        color='lifeExp',
        labels={'pop': 'population of USA'}
    )
    fig2.update_layout(title='US Population (Bars) and Life Expectancy (Color) Over Time', titlefont={'size': 12})
    return fig2


# figure3 plot and table
# this figure is updated in a callback, so it's not added to the dashboard figure class
def plot_figure3(year):
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


# TABLES
# primary data table setup
def get_primary_data_sp():
    primary_data_table = dash_table.DataTable(
        id='data_table',
        columns=[{'name': i, 'id': i} for i in df3.columns],
        data=df3.to_dict('records'), filter_action='native', sort_action='native'
    )
    return primary_data_table


# figure1 table
def get_figure1_table():
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
    return figure1_table


# figure2 table
def get_figure2_table():
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
    return figure2_table


# STORE SINGLE PAGE FIGURE OBJECTS IN THE CLASS INSTANCE
single_page_figures = DashboardFigures(name='Single Page Dashboard')
single_page_figures.add_figure('figure1', plot_figure1())
single_page_figures.add_figure('figure2', plot_figure2())
single_page_figures.add_figure('figure3', plot_figure3)
single_page_figures.add_table('primary_table', get_primary_data_sp())
single_page_figures.add_table('table1', get_figure1_table())
single_page_figures.add_table('table2', get_figure2_table())


# MULTI PAGE DASHBOARD FIGURE FUNCTIONS
# PLOTS
# figure 1 plot and data
def get_app_one_fig_one(mask):
    tdata = deepcopy(data1[data1['Stage'] == mask])

    tdata.sort_values('Value1', inplace=True)
    tdata['Cat'] = tdata[['Category', 'Department']].apply(lambda x: ''.join(x.values.astype(str)), axis=1)
    fig = px.bar(tdata, x='Cat', y='Value1')

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


# app one figure two
def get_app_one_figure_two(stage, x):
    tdata = data1[data1['Stage'] == stage]
    tdata = tdata.groupby(x)['Value1'].sum()
    x = list(tdata.index)

    fig = px.bar(x=x, y=tdata)

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


# app two figure
def get_app_two_figure(timeframe, by, measure):
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


# TABLES
# primary table
def generate_multi_db_primary_data(cats, depts):
    tdata = data1[data1['Category'].isin(cats)]
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


# STORE MULTI PAGE FIGURE OBJECTS IN THE CLASS INSTANCE
multi_page_figures = DashboardFigures(name='Multi Page Dashboard')
multi_page_figures.add_table('primary_table', generate_multi_db_primary_data)
multi_page_figures.add_figure('app_one_fig_one', get_app_one_fig_one)
multi_page_figures.add_figure('app_one_fig_two', get_app_one_figure_two)
multi_page_figures.add_figure('app_two_fig', get_app_two_figure)
