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
# PyGMT accepts a variety of datetime objects to plot data and create charts.
# Aside from the built-in Python datetime object, PyGmt supports input using
# ``pandas``, ``numpy``, ``xarray`` as well as properly formatted strings.
# These data types can be used to plot specific points as well as get
# passed into the ``region`` parameter to create a range of the data on an axis.
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

x = [
    datetime.date(2010, 6, 1),
    datetime.date(2011, 6, 1),
    datetime.date(2012, 6, 1),
    datetime.date(2013, 6, 1),
]
y = [1, 2, 3, 5]

fig = pygmt.Figure()
fig.plot(
    projection="X10c/5c",
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

x = [
    datetime.datetime(2021, 1, 1, 3, 45, 1),
    datetime.datetime(2021, 1, 1, 6, 15, 1),
    datetime.datetime(2021, 1, 1, 13, 30, 1),
    datetime.datetime(2021, 1, 1, 20, 30, 1),
]
y = [5, 3, 1, 2]

fig = pygmt.Figure()
fig.plot(
    projection="X10c/5c",
    region=[
        datetime.datetime(2021, 1, 1, 0, 0, 0),
        datetime.datetime(2021, 1, 2, 0, 0, 0),
        0,
        6,
    ],
    frame=["WS", "af"],
    x=x,
    y=y,
    style="c0.4c",
    pen="1p",
    color="blue",
)

fig.show()

########################################################################################
# Using ISO Format
# -------------------------
#
# In addition to Python's ``datetime`` library, PyGmt also supports passing times
# in ISO format. Much like in the previous examples, these valued are stored in
# list ``x`` in string format. Basic ISO strings are formatted as ``YYYY-MM-DD``
# with each ``-`` delineated section marking the four digit year value, two digit
# month value, and two digit day value respectively.
#
# When including time of day into ISO strings, the ``T`` character is used, as
# can be seen in the following example. This character is immediately followed
# by a string formatted as ``hh:mm:ss`` where each ``:`` delineated section marking
# the two digit hour value, two digit minute value, and two digit second value
# respectively. The figure in the following example is plotted over a horizontal
# range of one year from 1/1/2016 to 1/1/2017.

x = ["2016-02-01", "2016-06-04T14", "2016-10-04T00:00:15", "2016-12-01T05:00:15"]
y = [1, 3, 5, 2]
fig = pygmt.Figure()
fig.plot(
    projection="X10c/5c",
    region=["2016-01-01", "2017-01-1", 0, 6],
    frame=["WSen", "afg"],
    x=x,
    y=y,
    style="a0.45c",
    pen="1p",
    color="dodgerblue",
)

fig.show()

###############################################################################
# Mixing and matching datetime and ISO
#
# ADD DESCRIPTION

x = ["2020-02-01", "2020-06-04", "2020-10-04", datetime.datetime(2021, 1, 15)]
y = [1.3, 2.2, 4.1, 3]
fig = pygmt.Figure()
fig.plot(
    projection="X10c/5c",
    region=[datetime.datetime(2020, 1, 1), datetime.datetime(2021, 3, 1), 0, 6],
    frame=["WSen", "afg"],
    x=x,
    y=y,
    style="i0.4c",
    pen="1p",
    color="yellow",
)

fig.show()

########################################################################################
# Using :meth:`pandas.date_range`
# ------------------------------------------------
#
# ADD DESCRIPTION

x = pd.date_range("2013-05-01", periods=6, freq="4D")
y = [4, 5, 6, 8, 6, 3]

fig = pygmt.Figure()
fig.plot(
    projection="X10c/10c",
    region=[datetime.datetime(2013, 4, 30), datetime.datetime(2013, 5, 30), 0, 10],
    frame=["WSen", "ag"],
    x=x,
    y=y,
    style="s0.4c",
    pen="1p",
    color="pink",
)

fig.show()

########################################################################################
# Using ``xarray.DataArray``
# -------------------------------------
#
# In this example, instead of using a ``pd.date_range`` object, ``x`` is initialized
# as an ``xarray.DataArray`` object. Such object provide a wrapper around traditional
# data formats allowing this data to have varrying labeled dimensions and support
# operations that use various pieces of metadata. The following code uses a
# ``pandas.date_range`` object to fill the DataArray with data, yet this is not
# essential for the creation of a valid DataArray.

x = xr.DataArray(data=pd.date_range(start="2020-01-01", periods=4, freq="Q"))
y = [4, 7, 5, 6]

fig = pygmt.Figure()
fig.plot(
    projection="X10c/10c",
    region=[datetime.datetime(2020, 1, 1), datetime.datetime(2021, 4, 1), 0, 10],
    frame=["WSen", "ag"],
    x=x,
    y=y,
    style="n0.4c",
    pen="1p",
    color="red"
)
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
