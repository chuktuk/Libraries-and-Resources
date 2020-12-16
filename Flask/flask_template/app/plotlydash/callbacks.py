#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The callbacks module contains all of the callbacks needed to be registered with the dash apps.

Register the callbacks in dashboard.py when constructing the apps."""


from dash.dependencies import Input, Output, State
import dash_html_components as html

from .figures import single_page_figures, multi_page_figures
from .data import DataFuncs


# instantiate datafuncs
datafuncs = DataFuncs()


# SINGLE PAGE APP CALLBACKS
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
        else:
            color = 'primary'

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
        fig, table = single_page_figures.figures['figure3'](year)

        return fig, table


# MULTI PAGE APP CALLBACKS
def init_callbacks_multi_page(dash_app):
    data1 = datafuncs.create_dataframe()
    data2 = datafuncs.get_data()
    data2 = datafuncs.format_dataframe(data2)

    # app one primary data
    @dash_app.callback(
        Output('app-one-primary-data', 'children'),
        [Input('app-one-submit-query', 'n_clicks')],
        [State('app-one-filter1', 'value'),
         State('app-one-filter2', 'value')]
    )
    def update_app_one_primary_data(n_clicks, cats, depts):
        table = multi_page_figures.tables['primary_table'](cats, depts)
        return table

    # app-one figure 1 plot and data
    @dash_app.callback(
        [Output('app-one-figure1-plot', 'figure'),
         Output('app-one-figure1-table', 'children')],
        [Input('app-one-figure1-dropdown', 'value')]
    )
    def update_app_one_figure_one(mask):
        fig, table = multi_page_figures.figures['app_one_fig_one'](mask)
        return fig, table

    # app one figure 2 plot and data
    @dash_app.callback(
        [Output('app-one-figure2-plot', 'figure'),
         Output('app-one-figure2-table', 'children')],
        [Input('app-one-figure2-radio', 'value'),
         Input('app-one-figure2-dropdown', 'value')]
    )
    def update_app_one_figure_two(stage, x):
        fig, table = multi_page_figures.figures['app_one_fig_two'](stage, x)
        return fig, table

    # app two selected filters
    @dash_app.callback(
        Output('app-one-selected-filters-card', 'children'),
        [Input('app-one-submit-query', 'n_clicks')],
        [State('app-one-filter1', 'value'),
         State('app-one-filter2', 'value')]
    )
    def update_app_one_selected_filters(n_clicks, mask1, mask2):
        return [
            html.P(f'Filter 1: {[i for i in mask1]}'),
            html.P(f'Filter 2: {[i for i in mask2]}')
        ]

    # app two selected filters
    @dash_app.callback(
        Output('app-two-selected-filters-card', 'children'),
        [Input('app-two-submit-query', 'n_clicks')],
        [State('app-two-filter1', 'value'),
         State('app-two-filter2', 'value')]
    )
    def update_app_two_selected_filters(n_clicks, mask1, mask2):
        return [
            html.P(f'Filter 1: {[i for i in mask1]}'),
            html.P(f'Filter 2: {[i for i in mask2]}')
        ]

    # app two calculation card
    @dash_app.callback(
        [Output('app-two-calculation-card', 'children'),
         Output('change-card-color', 'color')],
        [Input('app-two-filter1', 'value')]
    )
    def update_app_two_calculation_card(value):
        ret = sum([int(i) for i in value])
        if ret < 3:
            col = 'info'
        elif ret < 21:
            col = 'warning'
        else:
            col = 'danger'

        ret_text = f'The sum of selected values for Filter 1 is {ret}.'

        return ret_text, col

    # update app 2 figure and table
    @dash_app.callback(
        [Output('app-two-figure-plot', 'figure'),
         Output('app-two-figure-table', 'children')],
        [Input('app-two-timeframe-dropdown', 'value'),
         Input('app-two-by-list-dropdown', 'value'),
         Input('app-two-measure-dropdown', 'value')]
    )
    def update_app_two_figure(timeframe, by, measure):
        fig, table = multi_page_figures.figures['app_two_fig'](timeframe, by, measure)
        return fig, table
