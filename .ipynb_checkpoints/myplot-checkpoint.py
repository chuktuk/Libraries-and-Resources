# same plot setup as previous example
import numpy as np
from numpy.random import random

N = 1000
source.data = {'x': np.random(N), 'y': np.random(N)}
plot = figure()
plot.circle('x', 'y', source=source)

# configure menu
menu = Select(options=['random', 'normal', 'lognormal'], value='random', title='Distribution')

def callback(attr, old, new):
    if menu.value == 'random': f = random
    elif menu.value == 'normal': f = normal
    else:                      f = lognormal
    source.data={'x': f(size=N), 'y': f(size=N)}
menu.on_change('value', callback)
layout = row(plot, menu)
curdoc().add_root(layout)