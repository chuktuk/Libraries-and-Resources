#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""The data.py module contains functions needed to get and wrangle data for the application."""

# imports
import jaydebeapi
import json
import math
import os
import numpy as np
import pandas as pd
import pymongo
import requests
import datetime as dt
# from flask import current_app as app
from collections import defaultdict
from copy import deepcopy
from dateutil.relativedelta import *
from statsmodels.tsa.forecasting.theta import ThetaModel
from sklearn.linear_model import LinearRegression
from werkzeug.utils import import_string

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


# get rstudio connect username
def get_credentials(req, username=True):
    credential_header = req.headers.get('RStudio-Connect-Credentials')
    if not credential_header:
        return {}
    user_metadata = json.loads(credential_header)
    if username:
        username = user_metadata.get('user', 'Testing')
        return username
    else:
        return user_metadata


# get deployment info
def get_deployment_info(guid):
    connect_server = os.getenv('RSTUDIO_SERVER')
    api_key = os.getenv('RSTUDIO_API_KEY')
    verify = os.getenv('VERIFY')
    if os.path.exists('data_files'):
        fp = f'data_files/{verify}'
    elif os.path.exists('../data_files'):
        fp = f'../data_files/{verify}'
    elif os.path.exists('app/plotlydash/data_files'):
        fp = f'app/plotlydash/data_files/{verify}'
    else:
        fp = f'plotlydash/data_files/{verify}'
    headers = {'Authorization': 'Key ' + api_key}

    content_response = requests.get(f'{connect_server}__api__/v1/experimental/content/{guid}',
                                    headers=headers,
                                    verify=fp)
    response_data = content_response.json()

    last_update = response_data.get('last_deployed_time')
    if last_update and isinstance(last_update, str) and len(last_update) == 25:
        last_update = last_update[:10]
    else:
        last_update = 'Unknown'
    python_version = response_data.get('py_version')
    app_type = response_data.get('app_mode')
    app_title = response_data.get('title')

    deployment_info = {
        'Last Update': last_update,
        'Python Version': python_version,
        'Application Type': app_type,
        'Title': app_title
    }

    return deployment_info


# new classify/predict function to output a table for all blankets using Theta model
def generate_theta_prediction_table(blanket_info, blanket_spending, blanket_list):
    def replacer(x):
        if x == 0:
            return np.nan
        else:
            return blanket_total - x

    data = defaultdict(list)
    data['Blanket Number'] = blanket_list

    for blanket_number in blanket_list:

        if blanket_number in blanket_info['Blanket Number'].unique():

            dff = blanket_info[blanket_info['Blanket Number'] == blanket_number].reset_index(drop=True)
            vendor_name = dff['Vendor Name'][0]
            blanket_end_date = dff['End Date'][0]
            blanket_total = dff['Blanket Total Amount Limit'][0]

            if blanket_number in blanket_spending['Blanket Number'].unique():
                dff2 = blanket_spending[blanket_spending['Blanket Number'] == blanket_number].dropna(
                    how='any', subset=['Release Date', 'Amount Billed']).set_index('Release Date').sort_index()
                # dff2 = blanket_spending[blanket_spending['Blanket Number'] == blanket_number].dropna(
                #     how='any').set_index('Release Date').sort_index()
                #                 remaining_balance = '${:,.2f}'.format(dff2['Amount Remaining'].min())

                dff2['Cumulative Spent'] = dff2['Amount Billed'].cumsum()
                amount_remaining = blanket_total - dff2['Cumulative Spent'].max()
                remaining_balance = '${:,.2f}'.format(amount_remaining)

                if dff2.shape[0] < 4:
                    prediction = 'Not Enough Data'
                    difference = 'Not Enough Data'
                    status = 'Not Enough Data'
                    proj_amt_remaining = 'Not Enough Data'

                elif amount_remaining <= 0:
                    prediction = dff2.index.max()
                    difference = prediction - blanket_end_date
                    if isinstance(difference, dt.timedelta):
                        difference = difference.days
                    prediction = prediction.date()
                    proj_amt_remaining = '$0.00'
                    status = f'Funds Depleted {prediction}'

                else:
                    tdf = dff2['Cumulative Spent'].resample('B').max().apply(replacer).fillna(method='ffill')
                    # remaining_balance = '${:,.2f}'.format(blanket_total - dff2['Cumulative Spent'].max())

                    tm = ThetaModel(tdf)
                    res = tm.fit()
                    pred = res.forecast(steps=10000)
                    if pred[-1] > 0:
                        pred = res.forecast(steps=20000)
                        if pred[-1] > 0:
                            pred = res.forecast(steps=30000)

                    # if the blanket end date is past, projected amount is the actual amount on the end date
                    if blanket_end_date < dt.datetime.now():
                        # find closest index to the end date and get that value
                        temp_df = deepcopy(dff2.reset_index())
                        proj_amt_remaining = blanket_total - temp_df[temp_df['Release Date'] < dt.datetime.now()][
                            'Cumulative Spent'].max()
                    # otherwise, get the prediction
                    else:
                        try:
                            proj_amt_remaining = pred[blanket_end_date]
                        except KeyError:
                            # I've found two instances of KeyErrors in the predictions: One is that the
                            # blanket_end_date is a weekend (first try block below). The other is that the
                            # blanket_end_date is before today but there are releases after the end date,
                            # and this causes the end date to be out of the prediction window creating a second key
                            # error.
                            try:
                                # get the next business day if blanket_end_date isn't a business day
                                next_bus_day = pd.tseries.offsets.BusinessDay(n=1) + blanket_end_date
                                proj_amt_remaining = pred[next_bus_day]
                            except KeyError:
                                proj_amt_remaining = 'Release Date/End Date Error'
                                # if blanket_end_date < dt.datetime.now(): # find closest index to the end date and
                                # get that value temp_df = deepcopy(dff2.reset_index()) proj_amt_remaining =
                                # blanket_total - temp_df[temp_df['Release Date'] < dt.datetime.now()][ 'Cumulative
                                # Spent'].max() else: proj_amt_remaining = 'Release Date/End Date Error'

                    if not isinstance(proj_amt_remaining, str) and proj_amt_remaining >= 0:
                        proj_amt_remaining = '${:,.2f}'.format(proj_amt_remaining)
                    elif not isinstance(proj_amt_remaining, str) and proj_amt_remaining < 0:
                        proj_amt_remaining = '-${:,.2f}'.format(abs(proj_amt_remaining))

                    prediction = pred[pred >= 0].index.max()
                    difference = (prediction - blanket_end_date)
                    prediction = prediction.date()
                    if isinstance(difference, dt.timedelta):
                        difference = difference.days

                    if difference > 0:
                        status = 'Surplus'
                    elif difference < 0:
                        status = 'Shortfall'
                    else:
                        status = 'On Budget'

            else:
                remaining_balance = blanket_total
                prediction = 'No Releases'
                difference = 'No Releases'
                status = 'No Releases'
                proj_amt_remaining = blanket_total

        else:
            vendor_name = 'Not Found'
            blanket_end_date = 'Not Found'
            blanket_total = 'Not Found'
            remaining_balance = 'Not Found'
            prediction = 'Not Found'
            difference = 'Not Found'
            status = 'Not Found'
            proj_amt_remaining = 'Not Found'

        if isinstance(blanket_end_date, dt.datetime):
            blanket_end_date = blanket_end_date.date()

        if not isinstance(blanket_total, str):
            blanket_total = '${:,.2f}'.format(blanket_total)

        data['Vendor Name'] += [vendor_name]
        data['Blanket Total'] += [blanket_total]
        data['Amount Remaining'] += [remaining_balance]
        data['Blanket End Date'] += [blanket_end_date]
        data['Projected End Date'] += [prediction]
        data['Projected Difference ($)'] += [proj_amt_remaining]
        data['Projected Difference (Days)'] += [difference]
        data['Projected Status'] += [status]

    df = pd.DataFrame(data)

    return df
