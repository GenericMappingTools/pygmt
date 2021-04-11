"""
Plotting Datetime Charts
========================

Creating datetime charts is handled by :meth:`pygmt.Figure.basemap`.

Plotting datetime data points is handled by :meth:`pygmt.Figure.basemap`.

.. note::

    This tutorial assumes the use of a Python notebook, such as IPython or Jupyter Notebook.
    To see the figures while using a Python script instead, use
    ``fig.show(method="external")`` to display the figure in the default PDF viewer.

    To save the figure, use ``fig.savefig("figname.pdf")`` where ``"figname.pdf"``
    is the desired name and file extension for the saved figure.
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
# Aside from the built in Python datetime object, PyGmt supports input using
# ``pandas``, ``numpy`` and ``xarray``. These data types can be used to plot
# specific points and be passed into the ``region`` parameter to become and
# axis for the data points.

########################################################################################
# ## Python's datetime


x = [datetime.date(2010, 6, 1), datetime.date(2011, 6, 1),
    datetime.date(2012, 6, 1), datetime.date(2013, 6, 1)]
y = [1, 2, 3, 5]

fig = pygmt.Figure()
fig.plot(projection="X10c/5c",
    region=[datetime.date(2010, 1, 1), datetime.date(2014, 12, 1), 0, 6],
    frame=["WSen", "af"],
    x=x,
    y=y,
    style="c0.4c",
    pen="1p",
    color="red3")

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
