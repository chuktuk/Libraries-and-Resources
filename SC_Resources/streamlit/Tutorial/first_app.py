#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Run the application using `streamlit run first_app.py` in a terminal in the /Tutorial directory."""


import time
import streamlit as st
import numpy as np
import pandas as pd


# create a dataframe
df = pd.DataFrame(
        {
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
        }
    )

# add app title
st.title('My First App')

# writing to the app
st.write('See a pandas dataframes displayed differently below.')
st.write('Using `st.write(df)`')
st.write(df)
st.write('Using `st.dataframe(df)`')
st.dataframe(df)
st.write('Using `st.table(df)`')
st.table(df)

# basic line chart
if st.sidebar.checkbox('Show line chart'):
    chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
    )
    st.line_chart(chart_data)

# plot basic map
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

# basic selectbox
st.sidebar.write('Basic selectbox')
option = st.sidebar.selectbox(
    'Pick a number',
    df['first column']
)
# items alone on a line get printed (just like st.write())
st.sidebar.write('You selected: ', option)

# more sidebar magic
left_column, right_column = st.sidebar.beta_columns(2)
pressed = left_column.button('Press me')
if pressed:
    right_column.write('Woohoo!')

# progress bar
lcol, rcol = st.sidebar.beta_columns(2)
compute = lcol.button('Compute')
if compute:
    st.sidebar.write('Starting a long computation...')
    latest_iteration = st.sidebar.empty()
    bar = st.sidebar.progress(0)
    for i in range(100):
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)
    st.sidebar.write("And now we're done!")

# expandable containers
expander = st.sidebar.beta_expander('FAQ')
expander.write('Here is a really long explanation about something that you want to be hidden most of the time.')
