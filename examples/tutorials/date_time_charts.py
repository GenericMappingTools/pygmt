"""
Plotting Datetime Charts
========================

Creating datetime charts is handled by :meth:`pygmt.Figure.basemap`.

Plotting datetime data points is handled by :meth:`pygmt.Figure.basemap`.
"""
# sphinx_gallery_thumbnail_number = 0

import datetime
import numpy as np
import pandas as pd
import pygmt
import xarray as xr

########################################################################################
# Datetime Input Types
# ----------------------
#
# PyGmt accepts a variety of datetime objects to plot data and create charts.
# Aside from the built-in Python datetime object, PyGmt supports input using
# ``pandas``, ``numpy`` and ``xarray``. These data types can be used to plot
# specific points as well as get passed into the ``region`` parameter to
# create a range of the data on an axis.
#
# The following examples will demonstrate how to create plots
# using the differnt datetime objects

###############################################################################
# Using Python's ``Datetime``
# ---------------------------------------
#
# In this example, Python's built-in ``datetime`` package is used
# to create data points stored in list ``x``. The format of the
# data is ``(Y, M, D)``. Additionally, dates are passed into the
# ``region`` parameter in the format
# ``(x_start, x_end, y_start, y_end)``,
# where the date range is plotted on the x-axis.
# An additonal notable parameter is `style`, where it's specified
# that data points are to be plotted in an **X** shape with a size
# of 0.3 centimeters.
#

x = [datetime.date(2010, 6, 1), datetime.date(2011, 6, 1),
    datetime.date(2012, 6, 1), datetime.date(2013, 6, 1)]
y = [1, 2, 3, 5]

fig = pygmt.Figure()
fig.plot(projection="X10c/5c",
    region=[datetime.date(2010, 1, 1), datetime.date(2014, 12, 1), 0, 6],
    frame=["WSen", "afg"],
    x=x,
    y=y,
    style="x0.3c",
    pen="1p",
    )

fig.show()

###############################################################################
# In addition to specifying the date, ``datetime`` supports
# the exact time of the data points. Using :meth:`datetime.datetime`
# the ``region`` paramter as well as data points can be created
# using this format ``(Y, M, D, H, M, S)`` where ``H`` is hours
# using 24 hour format.
#
# Some notable differences to the previous example include
# - Modifying ``frame`` to only include West(left) and South
# (bottom) border, and removing grid lines
# - Using circles to plot data points shown through ``c``
# in ``style`` parameter

x = [datetime.datetime(2021,1,1,3,45,1), datetime.datetime(2021,1,1,6,15,1),
    datetime.datetime(2021,1,1,13,30,1), datetime.datetime(2021,1,1,20,30,1)]
y = [5, 3, 1, 2]

fig = pygmt.Figure()
fig.plot(projection="X10c/5c",
    region=[datetime.datetime(2021, 1, 1, 0,0,0), datetime.datetime(2021, 1, 2, 0,0,0), 0, 6],
    frame=["WS", "af"],
    x=x,
    y=y,
    style="c0.4c",
    pen="1p",
    color="blue"
 )


fig.show()

########################################################################################
# `pandas.DatetimeIndex`

# pandas.DatetimeIndex
x = pd.date_range("2013", periods=3, freq="YS")
y = [4, 5, 6]
fig.plot(x, y, style="t0.4c", pen="1p", color="gold")

fig.show()

# Code

########################################################################################
# `xarray.DataArray`

# xarray.DataArray
x = xr.DataArray(data=pd.date_range(start="2015-03", periods=3, freq="QS"))
y = [7.5, 6, 4.5]
fig.plot(x, y, style="s0.4c", pen="1p")

fig.show()

# Code

########################################################################################
# Raw date-time in ISO format

# raw datetime strings
x = ["2016-02-01", "2016-06-04T14", "2016-10-04T00:00:15"]
y = [7, 8, 9]
fig.plot(x, y, style="a0.4c", pen="1p", color="dodgerblue")

fig.show()
# Code

########################################################################################
# Python built-in: `datetime.datetime`

# the Python built-in datetime and date
x = [datetime.date(2018, 1, 1), datetime.datetime(2019, 6, 1, 20, 5, 45)]
y = [6.5, 4.5]
fig.plot(x, y, style="i0.4c", pen="1p", color="seagreen")

fig.show()

# Code

########################################################################################
# Python built-in: `datetime.date`

# Code

########################################################################################
# Passing Min/Max Time into `region` parameter using `pygmt.info`
# ----------------------
#
# Explanation of supported parameters + bug at #597.

# Code

########################################################################################
# Setting Primary and Secondary Time Axes
# ----------------------
#
# Explanation.

# Code
