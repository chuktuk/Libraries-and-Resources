#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


# imports
import plotly.graph_objects as go
import plotly.express as px
from plotly.validators.scatter.marker import SymbolValidator
from plotly.subplots import make_subplots

import dash_bootstrap_components as dbc
import dash_html_components as html

import numpy as np
import pandas as pd
from datetime import datetime as dt
from statsmodels.tsa.forecasting.theta import ThetaModel

try:
    import app.plotlydash.data as data
except ModuleNotFoundError:
    import data

from copy import deepcopy


# CARDS
def make_about_app_card(guid):
    deployment_info = data.get_deployment_info(guid)
    about_app_card = dbc.Card(
        [
            dbc.CardHeader('About This App'),
            dbc.CardBody(
                [html.P(f'{idx}: {value}') for idx, value in deployment_info.items()]
            )
        ],
    )
    return about_app_card


# Theta model prediction plot
def get_theta_model(blanket_info, blanket_spending, blanket_number):
    def replacer(x):
        if x == 0:
            return np.nan
        else:
            return blanket_total - x

    if blanket_number in list(
            set(blanket_info['Blanket Number'].unique()) & set(blanket_spending['Blanket Number'].unique())):

        if blanket_spending[blanket_spending['Blanket Number'] == blanket_number].shape[0] < 4:
            vendor_name = blanket_info[blanket_info['Blanket Number'] == blanket_number].reset_index()['Vendor Name'][0]

            fig = go.Figure()
            fig.update_xaxes(range=[0, 5])
            fig.update_yaxes(range=[0, 4])
            fig.add_annotation(
                x=2.5,
                y=2,
                text='Not Enough Releases to Predict',
                showarrow=False,
                font={'size': 20}
            )
            fig.update_layout(
                title=f'Blanket PO #{blanket_number} ({vendor_name})',
                height=550,
            )
            return fig, None, None, None
        else:

            dff = blanket_info[blanket_info['Blanket Number'] == blanket_number].reset_index(drop=True)
            vendor_name = dff['Vendor Name'][0]
            blanket_end_date = dff['End Date'][0]
            blanket_total = dff['Blanket Total Amount Limit'][0]

            # dff2 = blanket_spending[blanket_spending['Blanket Number'] == blanket_number].dropna(
            #     how='any').set_index('Release Date').sort_index()
            #
            # dff2['Cumulative Spent'] = dff2['Amount Billed'].cumsum()
            #
            # tdf = dff2['Cumulative Spent'].resample('B').max().apply(replacer).fillna(method='ffill')
            dff2 = data.get_total_blanket_spending(
                blanket_info, blanket_spending, blanket_number
            ).set_index('Release Date')
            tdf = dff2['Amount Billed to Date'].resample('B').max().apply(replacer).fillna(method='ffill')

            # remaining_balance = blanket_total - dff2['Cumulative Spent'].max()
            remaining_balance = blanket_total - dff2['Amount Billed to Date'].max()

            tm = ThetaModel(tdf)
            res = tm.fit()

            # need a good way to find the 2000, 3000, and 3000 steps used below
            pred = res.forecast(steps=10000)

            # ensure that the prediction goes out far enough
            if pred[-1] > 0:
                pred = res.forecast(steps=20000)
                intervals = res.prediction_intervals(steps=20000, alpha=0.05)
                # if the prediction still isn't far enough, increase by 50%
                if pred[-1] > 0:
                    pred = res.forecast(steps=30000)
                    intervals = res.prediction_intervals(steps=30000, alpha=0.05)
            else:
                intervals = res.prediction_intervals(steps=10000, alpha=0.05)

            prediction = pred[pred >= 0].index.max()

            # if past the blanket end date, the projected amount at end date is the actual amount at end date
            if blanket_end_date < dt.now():
                # find closest index to the end date and get that value
                temp_df = deepcopy(dff2.reset_index())
                # proj_amt_remaining = blanket_total - temp_df[temp_df['Release Date'] < dt.now()][
                #     'Cumulative Spent'].max()
                proj_amt_remaining = blanket_total - temp_df[temp_df['Release Date'] < dt.now()][
                    'Amount Billed to Date'].max()
            # otherwise, get the prediction
            else:
                try:
                    proj_amt_remaining = pred[blanket_end_date]
                except KeyError:
                    # # get the next business day if blanket_end_date isn't a business day
                    # next_bus_day = pd.tseries.offsets.BusinessDay(n=1) + blanket_end_date
                    # proj_amt_remaining = pred[next_bus_day]
                    # I've found two instances of KeyErrors in the predictions:
                    # One is that the blanket_end_date is a weekend (first try block below).
                    # The other is that the blanket_end_date is before today but there are releases after the end
                    # date, and this causes the end date to be out of the prediction window creating a second
                    # key error.
                    try:
                        # get the next business day if blanket_end_date isn't a business day
                        next_bus_day = pd.tseries.offsets.BusinessDay(n=1) + blanket_end_date
                        proj_amt_remaining = pred[next_bus_day]
                    except KeyError:
                        proj_amt_remaining = 'Release Date/End Date Error'
                        # if blanket_end_date < dt.now():
                        #     # find closest index to the end date and get that value
                        #     temp_df = deepcopy(dff2.reset_index())
                        #     proj_amt_remaining = blanket_total - temp_df[temp_df['Release Date'] < dt.now()][
                        #         'Cumulative Spent'].max()
                        # else:
                        #     proj_amt_remaining = 'Release Date/End Date Error'

            if not isinstance(proj_amt_remaining, str) and proj_amt_remaining >= 0:
                proj_amt_remaining = '${:,.2f}'.format(proj_amt_remaining)
            elif not isinstance(proj_amt_remaining, str) and proj_amt_remaining < 0:
                proj_amt_remaining = '-${:,.2f}'.format(abs(proj_amt_remaining))

            lower = intervals[intervals['lower'] >= 0].index.max()
            upper = intervals[intervals['upper'] >= 0].index.max()

            pred_array = pred[:prediction]
            lower_array = intervals['lower'][:lower]
            upper_array = intervals['upper'][:upper]

            #             print(upper_array)

            if not all(upper_array >= 0):
                idx = intervals[intervals['upper'] < 0].index.min()
                upper_array = intervals['upper'][:idx]

            # TODO: DELETE IF GOES HAYWIRE
            if not all(lower_array >= 0):
                idx = intervals[intervals['lower'] < 0].index.min()
                lower_array = intervals['lower'][:idx]

            if list(upper_array)[-1] > 0:
                upper_array[list(upper_array.index)[-1]] = 0

            #                 idx = upper_array[upper_array < 0].index.min()
            #                 upper_array = upper_array[:idx]

            # matplotlib representation
            #         fig = res.plot_predict(steps=3000, in_sample=True, alpha=0.05)
            #         plt.axhline(y=0, color='red')
            #         plt.axvline(x=blanket_end_date, color='green')

            # plotly
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=tdf.index,
                    y=tdf,
                    name='Spending'
                )
            )

            # set the x location for the annotation
            #             x_loc = ((dff2.index.max() - dff2.index.min()) * 0.2) + dff2.index.min()
            x_loc = upper_array.index.max() - (upper_array.index.max() - upper_array.index.min()) * 0.3
            y_loc = blanket_total * 0.7

            if remaining_balance > 0:

                if prediction > blanket_end_date:
                    text_color = 'black'
                    projection = 'Surplus'
                elif prediction < blanket_end_date:
                    text_color = 'red'
                    projection = 'Shortfall'
                else:
                    text_color = 'black'
                    projection = 'On Budget'

                fig.add_trace(
                    go.Scatter(
                        x=upper_array.index,
                        y=upper_array,
                        name='Upper Limit',
                        marker={'color': 'gray'},
                        showlegend=False,
                        fill='tonexty',
                        fillcolor='lightgray'
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=lower_array.index,
                        y=lower_array,
                        name='Lower Limit',
                        marker={'color': 'gray'},
                        showlegend=False,
                        fill='tonexty',
                        fillcolor='lightgray'
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=pred_array.index,
                        y=pred_array,
                        name='Projected',
                        marker={'color': 'red'}
                    )
                )

                fig.add_annotation(
                    x=blanket_end_date,
                    y=0,
                    text='Blanket End Date'
                )

                fig.add_annotation(
                    x=x_loc,
                    y=blanket_total * 0.9,
                    text=f'Projected {projection}',
                    font={'color': text_color, 'size': 16},
                    showarrow=False
                )

                fig.add_annotation(
                    x=x_loc,
                    y=y_loc * 1.1,
                    text=f'Blanket End Date: {blanket_end_date.date()}',
                    font={'color': text_color, 'size': 16},
                    showarrow=False
                )

                fig.add_annotation(
                    x=x_loc,
                    y=y_loc,
                    text=f'Projected Fund Depletion on {prediction.date()}',
                    font={'color': text_color, 'size': 16},
                    showarrow=False
                )

                fig.add_annotation(
                    x=x_loc,
                    y=y_loc * 0.85,
                    text=f'Projected Funds on End Date {proj_amt_remaining}',
                    font={'color': text_color, 'size': 16},
                    showarrow=False
                )

                fig.update_layout(
                    title=f'Blanket PO #{blanket_number} ({vendor_name}) Spending Forecast',
                    height=550,
                    legend={
                        'orientation': 'h',
                        'yanchor': 'bottom',
                        'xanchor': 'right',
                        'x': 1,
                        'y': 1.02
                    }
                )

            else:
                lower = dff2.index.max()
                upper = dff2.index.max()
                prediction = dff2.index.max()

                x_loc = list(tdf.index)[int(len(tdf.index) / 2)]
                y_loc = blanket_total * 0.65

                fig.add_annotation(
                    x=x_loc,
                    y=y_loc,
                    text=f'Funds Depleted on {prediction.date()}',
                    showarrow=False,
                    font={'color': 'red', 'size': 16}
                )

                fig.update_layout(
                    title=f'Blanket PO #{blanket_number} ({vendor_name}) Spending',
                    height=550,
                    #                     legend={
                    #                         'orientation': 'h',
                    #                         'yanchor': 'bottom',
                    #                         'xanchor': 'right',
                    #                         'x': 1,
                    #                         'y': 1.02
                    #                     }
                )

            return fig, lower, prediction, upper
    else:
        if blanket_number in blanket_info['Blanket Number'].unique():
            message = f'Blanket Number {blanket_number} Has No Releases'
        else:
            message = f'Blanket Number {blanket_number} Not Found'

        fig = go.Figure()
        fig.update_xaxes(range=[0, 5])
        fig.update_yaxes(range=[0, 4])
        fig.add_annotation(
            x=2.5,
            y=2,
            text=message,
            showarrow=False,
            font={'size': 20}
        )
        fig.update_layout(height=550)

        return fig, None, None, None
