#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The controls module contains objects needed to generate the controls or user inputs for all dashboards."""

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from .data import DataFuncs

# instantiate datafuncs
datafuncs = DataFuncs()

# get global data objects
df3 = datafuncs.get_gapminder_data()
data_canada, data_usa, years = datafuncs.extract_gapminder_objects(df3)
data1 = datafuncs.create_dataframe()
data2 = datafuncs.get_data()
data2 = datafuncs.format_dataframe(data2)


# class definition
class DashboardControls:
    def __init__(self, name):
        self.name = name
        self.controls = {}
        self.form_groups = {}

    def __repr__(self):
        return f'Dashboard Controls for {self.name}'

    def add_control(self, control_name, control_label, control):
        if control_name not in self.controls:
            self.controls[control_name] = {
                'label': control_label,
                'control': control
            }

    def add_form_group(self, form_group_name, form_group):
        if form_group_name not in self.form_groups:
            self.form_groups[form_group_name] = form_group


# CONTROLS FOR THE SINGLE PAGE DASHBOARD
def generate_single_page_db_controls():
    single_page_db_controls = DashboardControls(name='Single Page Dashboard')

    # sidebar form group
    # control 1
    control_one_title = html.P('Control 1 Display Name', className='dash-text')

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
    control_two_title = html.P(
        'Control 2 Items nested in dbc.Card',
        className='dash-text'
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

    # arrange into the sidebar form group
    single_page_db_form_group = dbc.FormGroup(
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

    # add the form group
    single_page_db_controls.add_form_group('sidebar_form_group', single_page_db_form_group)

    # figure controls
    # year slider for gapminder plot
    year_slider = dcc.Slider(
        id='year-slider',
        min=min(years),
        max=max(years),
        value=max(years),
        marks={str(i): str(i) for i in years},
        step=None
    )

    single_page_db_controls.add_control('year_slider', None, year_slider)

    return single_page_db_controls


# create the multi page dashboard controls
def generate_multi_page_db_controls():
    multi_page_db_controls = DashboardControls(name='Multi Page Dashboard')

    # create options for sidebar filters
    app_one_filter1_options = [{'label': i, 'value': i} for i in sorted(list(data1.Category.unique()))]
    app_one_filter1_selected = [i for i in sorted(list(data1.Category.unique()))]

    app_one_filter2_options = [{'label': i, 'value': i} for i in sorted(list(data1.Department.unique()))]
    app_one_filter2_selected = [i for i in sorted(list(data1.Department.unique()))]

    # app one sidebar filters
    app_one_filter1_title = dbc.Label(
        'Categories',
        className='dash-text'
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
        className='dash-text'
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
        className='dash-text'
    )
    app_one_figure1_dropdown = dcc.Dropdown(
        id='app-one-figure1-dropdown',
        options=[{'label': i, 'value': i} for i in sorted(list(data1.Stage.unique()))],
        value='BFG'
    )

    multi_page_db_controls.add_control('app_one_figure1_dropdown',
                                       app_one_figure1_dropdown_title,
                                       app_one_figure1_dropdown)

    app_one_figure2_radio_title = dbc.Label(
        'Stage',
        className='dash-text'
    )
    app_one_figure2_radio = dbc.RadioItems(
        id='app-one-figure2-radio',
        options=[{'label': i, 'value': i} for i in sorted(list(data1.Stage.unique()))],
        value='BFG'
    )

    multi_page_db_controls.add_control('app_one_figure2_radio',
                                       app_one_figure2_radio_title,
                                       app_one_figure2_radio)

    app_one_figure2_dropdown_title = dbc.Label(
        'Analyze By',
        className='dash-text'
    )
    app_one_figure2_dropdown = dcc.Dropdown(
        id='app-one-figure2-dropdown',
        options=[{'label': i, 'value': i} for i in ['Category', 'Department']],
        value='Category'
    )

    multi_page_db_controls.add_control('app_one_figure2_dropdown',
                                       app_one_figure2_dropdown_title,
                                       app_one_figure2_dropdown)

    # app two filters
    app_two_filter1_title = dbc.Label(
        'Filter 1',
        className='dash-text'
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
        className='dash-text',
    )
    app_two_filter2 = dbc.Card(
        dbc.Checklist(
            id='app-two-filter2',
            options=[{'label': f'Option {i}', 'value': f'Option {i}'} for i in range(2, 10, 2)],
            value=[f'Option {i}' for i in range(2, 10, 2)]
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
        className='dash-text'
    )
    app_two_timeframe_dropdown = dcc.Dropdown(
        id='app-two-timeframe-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_timeframe_list],
        value='All Years'
    )

    multi_page_db_controls.add_control('app_two_timeframe_dropdown',
                                       app_two_timeframe_title,
                                       app_two_timeframe_dropdown)

    app_two_by_list_title = dbc.Label(
        'Analyze By',
        className='dash-text'
    )
    app_two_by_list_dropdown = dcc.Dropdown(
        id='app-two-by-list-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_by_list],
        value=app_two_by_list[0]
    )

    multi_page_db_controls.add_control('app_two_by_list_dropdown',
                                       app_two_by_list_title,
                                       app_two_by_list_dropdown)

    app_two_measure_title = dbc.Label(
        'Variable to Plot',
        className='dash-text'
    )
    app_two_measure_dropdown = dcc.Dropdown(
        id='app-two-measure-dropdown',
        options=[{'label': i, 'value': i} for i in app_two_measure_list],
        value=app_two_measure_list[0]
    )

    multi_page_db_controls.add_control('app_two_measure_dropdown',
                                       app_two_measure_title,
                                       app_two_measure_dropdown)

    # sidebar form groups
    app_one_form_group = dbc.FormGroup(
        [
            dbc.FormGroup([app_one_filter1_title, app_one_filter1]),
            dbc.FormGroup([app_one_filter2_title, app_one_filter2]),
            dbc.Button('Submit New Query', id='app-one-submit-query', color='primary')
        ]
    )

    multi_page_db_controls.add_form_group('app_one_form_group', app_one_form_group)

    app_two_form_group = dbc.FormGroup(
        [
            dbc.FormGroup([app_two_filter1_title, app_two_filter1]),
            dbc.FormGroup([app_two_filter2_title, app_two_filter2]),
            dbc.Button('Submit New Query', id='app-two-submit-query', color='primary')
        ]
    )

    multi_page_db_controls.add_form_group('app_two_form_group', app_two_form_group)

    return multi_page_db_controls


# create the objects
single_page_db_controls = generate_single_page_db_controls()
multi_page_db_controls = generate_multi_page_db_controls()
