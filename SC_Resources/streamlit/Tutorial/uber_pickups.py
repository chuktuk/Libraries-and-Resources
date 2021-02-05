#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Basic app displaying uber pickups.
Streamlit operations are executed sequentially, and values can be updated.
Can use if statements to control, can use user inputs, or can simply update after operations complete."""

import streamlit as st
import pandas as pd
import numpy as np

# title
st.title('Uber Pickups in NYC')

# load some data
date_column = 'date/time'
url = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'


# load some data
# decorator here caches the data so it doesn't have to load every time
@st.cache
def load_data(nrows):
    data = pd.read_csv(url, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    data[date_column] = pd.to_datetime(data[date_column])
    return data


# load data and show state of loading
# top line occurs before load_data(), value is updated after load_data() completes
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done (using st.cache)')

# display data table of the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# create a histogram of pickup times (bins are hourly)
st.subheader('Histogram of pickup times')
hist_values = np.histogram(data[date_column].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)


# create a map showing pickup locations
def display_map_data(hour):
    if isinstance(hour, int):
        assert hour < 24, '"hour" must be an integer between 0-23 or the word "all"'
        filtered_data = data[data[date_column].dt.hour == hour]
        st.subheader(f'Map of pickups at {hour}:00')
        st.map(filtered_data)
    else:
        assert hour == 'all', '"hour" must be an integer between 0-23 or the word "all"'
        st.subheader('Map of all pickups')
        st.map(data)


# let user pick the data
if st.checkbox('Filter map data by hour'):
    hour = st.slider('hour', 0, 23, 17)
    display_map_data(hour)
else:
    display_map_data('all')
