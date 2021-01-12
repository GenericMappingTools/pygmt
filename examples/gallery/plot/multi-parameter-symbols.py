"""
Multi-parameter symbols
-------------------------

The :meth:`pygmt.Figure.plot` method can plot individual multi-parameter symbols by passing 
the corresponding shortcuts listed below to the ``style`` argument. Additionally, we must define 
the required parameters in a 2d list or numpy array (``[[parameters]]`` for a single symbol 
or ``[[parameters_1],[parameters_2],[parameters_i]]`` for several ones) or use an 
appropriately formatted input file and pass it to ``data``. 

The following symbols are available:

- **e**: ellipse, ``[[lon, lat, direction, major_axis, minor_axis]]``
- **j**: rotated rectangle, ``[[lon, lat, direction, width, height]]``
- **r**: rectangle, ``[[lon, lat, width, height]]``
- **R**: rounded rectangle, ``[[lon, lat, width, height, radius]]``
- **w**: pie wedge, ``[[lon, lat, radius, startdir, stopdir]]``, the last two arguments are 
  directions given in degrees counter-clockwise from horizontal 

Upper-case versions **E**, **J**, and **W** are similar to **e**, **j** and **w** but expect geographic 
azimuths and distances.

For more advanced options, see the full option list at :gmt-docs:`plot.html`.
"""

import numpy as np
import pygmt

fig = pygmt.Figure()

fig.basemap(region=[0, 6, 0, 2], projection="x3c", frame=True)

###################
# ELLIPSE
data = np.array([[0.5, 1, 45, 3, 1]])

fig.plot(data=data, style="e", color="orange", pen="2p,black")

###################
# ROTATED RECTANGLE
data = np.array([[1.5, 1, 120, 5, 0.5]])

fig.plot(data=data, style="j", color="red3", pen="2p,black")

###################
# RECTANGLE
data = np.array([[3, 1, 4, 1.5]])

fig.plot(data=data, style="r", color="dodgerblue", pen="2p,black")

###################
# ROUNDED RECTANGLE
data = np.array([[4.5, 1, 1.25, 4, 0.5]])

fig.plot(data=data, style="R", color="seagreen", pen="2p,black")

###################
# PIE WEDGE
data = np.array([[5.5, 1, 2.5, 45, 330]])

fig.plot(data=data, style="w", color="lightgray", pen="2p,black")

fig.show()
