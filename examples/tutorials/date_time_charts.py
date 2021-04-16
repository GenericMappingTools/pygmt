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
# The following example provides context on how both ``datetime`` and ``ISO``
# date data can be plotted using PyGMT. This can be helpful when dates and times
# are coming from different sources, meaning conversions do not need to take place
# between ISO and datetime in order to create valid plots.

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
# In the following example, a ``pandas.date_range`` object is used to pass date
# data to the PyGMT figure. This object is set using the pandas method ``date_range()``.
# This particular object contains 7 different ``pandas.Timestamp`` objects, with the
# number being manipulated by the periods argument. Each period begins at the start
# of a business quarter as denoted by BQS when passed to the freq argument. The inital
# date is first argument that is passed to ``date_range()`` and it marks the first
# data in the object ``x`` that will be plotted.

x = pd.date_range("2018-03-01", periods=7, freq="BQS")
y = [4, 5, 6, 8, 6, 3, 5]

fig = pygmt.Figure()
fig.plot(
    projection="X10c/10c",
    region=[datetime.datetime(2017, 12, 31), datetime.datetime(2019, 12, 31), 0, 10],
    frame=["WSen", "ag"],
    x=x,
    y=y,
    style="i0.4c",
    pen="1p",
    color="purple",
)

fig.show()

########################################################################################
# Using :meth:`xarray.DataArray`
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
    color="red",
)
fig.show()

# Code

########################################################################################
# Generating Region Using :meth:`pygmt.info`
# ----------------------
#
# Explanation of supported parameters + bug at #597.

data = [['20200712',1000],
       ['20200714',1235],
       ['20200716',1336],
       ['20200719',1176],
       ['20200721',1573],
       ['20200724',1893],
       ['20200729',1634]]

df = pd.DataFrame(
  data,columns = ['Date','Score'])

df['Date'] = pd.to_datetime(
          df['Date'],
          format='%Y%m%d')

fig = pygmt.Figure()
region = pygmt.info(
    table=df[["Date", "Score"]],
    per_column=True,
    spacing=(5000, 1200),
)

fig.plot(
    region=region,
    projection="X15c/10c",
    frame=['WSen', "afg"],
    x=df.Date,
    y=df.Score,
    style="c0.4c",
    pen="1p",
    color="green3",
)
fig.show()

########################################################################################
# Setting Primary and Secondary Time Axes
# ----------------------
#
# This example focuses on labeling the axes and setting intervals
# at which the labels are expected to appear. All of these modification
# are added to the ``frame`` argument and each item in that list modifies
# a specific section of the plot.
#
# Starting off with ``WS``, adding this string means that only
# Western/Left **(W)** and Southern/Bottom **(S)** borders of
# the plot will be shown. For more information on this, please
# refer to :docs:`pygmt.Frames`.
#
# The other important item in the ``frame`` list is
# ``sxa1Of1D``. This string modifies the secondary
# labeling **(s)** of the x-axis **(x)**. Specifically,
# it sets the main annotation and major tick spacing interval
# to one month **(O)** (capital letter o, not zero). Additionally,
# it sets the minor tick spacing interval to 1 day **(D)**.
# The labeling of this axis is also modified using
# ``pygmt.config(FORMAT_DATE_MAP="o")`` to use the month's
# name instead of its number.

x = pd.date_range("2013-05-02", periods=10, freq="2D")
y = [4, 5, 6, 8, 9, 5, 8, 9, 4, 2]

fig = pygmt.Figure()
with pygmt.config(FORMAT_DATE_MAP="o"):    
    fig.plot(projection="X15c/10c",
        region=[datetime.datetime(2013, 5, 1), datetime.datetime(2013, 5, 25), 0, 10],
        frame=["WS", "sxa1Of1D", "pxa5d", "pya1+ucm", "sy+lLength"],
        x=x,
        y=y,
        style="c0.4c",
        pen="1p",
        color="green3",
    )

fig.show()

########################################################################################
# The same concept shown above can be applied to smaller
# as well as larger intervals. In this example,
# data is plotted for different times throughout two days.
# Primary x-axis labels are modified to repeat every 6 hours
# and secondary x-axis label repeats every day and shows
# the day of the week.
#
# Other notable mentions in this example is
# ``pygmt.config(FORMAT_CLOCK_MAP="-hhAM")``
# which specifies the used format for time.
# In this case, leading zeros are removed
# using **(-)**, and only hours are displayed.
# Additionally, an AM/PM system is being used
# instead of a 24-hour system.

x = pd.date_range("2021-04-15", periods=8, freq="6H")
y = [2, 5, 3, 1, 5, 7, 9, 6]

fig = pygmt.Figure()
with pygmt.config(FORMAT_CLOCK_MAP="-hhAM"):
    fig.plot(projection="X15c/10c",
        region=[datetime.datetime(2021, 4, 14, 23, 0, 0), datetime.datetime(2021, 4, 17), 0, 10],
        frame=["WS", "sxa1K", "pxa6H", "pya1+ukm/h", "sy+lSpeed"],
        x=x,
        y=y,
        style="n0.4c",
        pen="1p",
        color="lightseagreen",
    )

fig.show()
