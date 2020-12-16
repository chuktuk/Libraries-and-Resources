#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The data module contains objects needed to wrangle data and generate tables."""

import pandas as pd
import plotly.express as px


class DataFuncs:

    @staticmethod
    def create_dataframe():
        """Create the dataframe for the dashboard."""

        df = pd.read_csv('data/data.csv', header=0)
        return df

    @staticmethod
    def get_data():
        df = pd.read_csv('data/data2.csv',
                         dtype={'Manufacturer': 'str',
                                'Asset Alias': 'str',
                                'EAM Department Name': 'str',
                                'EAM Department': 'str',
                                'Rate Class Descr': 'str',
                                'Component Code': 'str',
                                'Component Description': 'str',
                                'Work Order Crew Code': 'str',
                                'Work Order Crew': 'str',
                                'Work Order Number': 'str',
                                'Work Order Status Code': 'str',
                                'Work Type': 'str',
                                'WO Actual Finish Date': 'str',
                                'WO Actual Finish Year': 'str',
                                'Work Order Reported Date': 'str',
                                'Work Order Lead Craft Person': 'str',
                                'Work Order Maintenance Planner': 'str',
                                'Work Order Description': 'str',
                                'Actual Labor Cost': 'float',
                                'Actual Material Cost': 'float',
                                'Actual Service Cost': 'float',
                                'Total Work Order Cost': 'float',
                                'Overtime Hours': 'float',
                                'Regular Hours': 'float'}
                         )
        df['WO Actual Finish Date'] = pd.to_datetime(df['WO Actual Finish Date'], format='%Y-%m-%d')
        df['Work Order Reported Date'] = pd.to_datetime(df['Work Order Reported Date'], format='%Y-%m-%d')
        df.fillna('None Specified', inplace=True)

        return df

    @staticmethod
    def format_dataframe(df):
        """Edit data types and formatting for primary OBIEE dataframe

        :param df: The primary dataframe returned from OBIEE
        :return: The formatted dataframe
        """

        # set data types
        df['WO Actual Finish Date'] = pd.to_datetime(df['WO Actual Finish Date'], format='%Y-%m-%d')
        df['Work Order Reported Date'] = pd.to_datetime(df['Work Order Reported Date'], format='%Y-%m-%d')
        df['WO Actual Finish Year'] = df['WO Actual Finish Year'].astype('int')

        # deal with missing values
        df.fillna('None Specified', inplace=True)

        # create new column YYYY-MM
        df['Actual Finish YYYY-MM'] = df['WO Actual Finish Date'].apply(lambda x: x.strftime('%Y-%m'))

        return df

    @staticmethod
    def get_gapminder_data():
        df3 = px.data.gapminder()
        df3['year'] = df3['year'].astype('int')

        return df3

    @staticmethod
    def extract_gapminder_objects(df3):
        # extract canada data
        data_canada = df3[df3.country == 'Canada']

        # extract US data
        data_usa = df3[df3.country == 'United States']

        # lists
        years = sorted(list(df3.year.unique()))

        return data_canada, data_usa, years
