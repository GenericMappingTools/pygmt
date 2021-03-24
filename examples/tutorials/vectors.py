"""
Plot vectors
==========

Plotting vectors is handled by :meth:`pygmt.Figure.plot`.

.. note::

    This tutorial assumes the use of a Python notebook, such as IPython or Jupyter Notebook.
    To see the figures while using a Python script instead, use
    ``fig.show(method="external")`` to display the figure in the default PDF viewer.

    To save the figure, use ``fig.savefig("figname.pdf")`` where ``"figname.pdf"``
    is the desired name and file extension for the saved figure.
"""
# TODO: change this number to reflect the correct thumbnail
# sphinx_gallery_thumbnail_number = 3

import numpy as np
import pygmt

########################################################################################
# Plot Caretesian Vectors
# ----------
#
# Create a simple Cartesian vector using a starting point through
# ``x``, ``y``, and ``direction`` parameters. The direction is specified
# by a list of two 1d arrays structured as ``[[angle_in_degrees], [length]]``
#
# On the shown figure, the plot is projected on a 10cm X 10cm region,
# which is specified by the ``projection`` parameter.
# The magnitude of the vector also uses centimeters by default but
# could be changed using :meth:`pygmt.config`
# (Check the next examples for unit changes)
#
# Notice that the ``v`` in the ``style`` parameter stands for
# vector; it distinguishes it from regular lines and allows for
# different customization.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    x=2,
    y=8,
    direction=[[-45], [6]],
    style="v0c",
)
fig.show()

########################################################################################
# In this example, we apply the same concept shown previously to plot multiple
# vectors. Notice that instead of passing int/float to ``x`` and ``y``, a list
# of all x and y coordinates will be passed. Similarly, the length of direction
# list will increase accordingly.
#
# Additionally, we changed the style of the vector to include a red
# arrowhead and increased the thickness of the line. A list of different
# styling attributes can be found in
# [Vector attributes documentation](https://www.pygmt.org/latest/gallery/lines/vector_heads_tails.html)

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    x=[2, 4],
    y=[8, 1],
    direction=[[-45, 23], [6, 3]],
    style="v0.6c+e",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# The default unit of vector magnitude/length is centimeters.
# However, this can be changed to inches or points. Note that, in GMT,
# one point is defined as 1/72 inch.
#
# In this example, the graphed region is 10in X 4in, however,
# the magnitude of the first vector is still graphed in centimeters.
# Using ``pygmt.config(PROJ_LENGTH_UNIT="i")``, the default unit
# can be changed to inches in the second plotted vector.

fig = pygmt.Figure()
# Vector 1 with default unit as cm
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10i/4i",
    frame="a",
    x=2,
    y=8,
    direction=[[0], [3]],
    style="v1c+e",
    pen="2p",
    color="red3",
)
# Vector 2 after changing default unit to in
with pygmt.config(PROJ_LENGTH_UNIT="i"):
    fig.plot(
        x=2,
        y=7,
        direction=[[0], [3]],
        style="v1c+e",
        pen="2p",
        color="red3",
    )
fig.show()

########################################################################################
# Vectors can also be plotted by including all the information
# about a vector in a single list. However, this requires creating
# a list for all vectors and passing it into a ``numpy`` array object.
# Each vector list contains the information structured as:
# ``[x_start, y_start, direction_degrees, magnitude]``
#
# If this approach is chosen, ``data`` parameter must be
# used instead of ``x``, ``y`` and  ``direction``.

vector_1 = [2, 3, 45, 4]
# Create a list of lists that include each vector information
vectors = np.array([vector_1])
# vectors structure: [[ 2  3 45  4]]

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    data=vectors,
    style="v0.6c+e",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# Using the functionality mentioned in the previous example,
# multiple vectors can be plotted at the same time. Another
# vector could be simply added to the 2d ``numpy`` array object
# and passed using ``data`` parameter.

# vector specifications structured as: [x_start, y_start, direction_degrees, magnitude]
vector_1 = [2, 3, 45, 4]
vector_2 = [7.5, 8.3, -120.5, 7.2]
# Create a list of lists that include each vector information
vectors = np.array([vector_1] + [vector_2])
# vectors structure:
# [[   2.     3.    45.     4. ]
#  [   7.5    8.3 -120.5    7.2]]

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    data=vectors,
    style="v0.6c+e",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# In this example, cartesian vectors are plotted over a Mercator
# projection of the continental US. The x values represent the
# longitude and y values represent the latitude where the vector starts

# create a plot with coast, Mercator projection (M) over the continental US
fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M15c",
    frame="ag",
    borders=1,
    area_thresh=4000,
    shorelines="0.25p,black",
    land="grey",
    water="lightblue",
)

style = "v0.6c+bc+ea+a30"
fig.plot(
    x=-110,
    y=40,
    style=style,
    pen="1p",
    color="red3",
    direction=[[-25], [3]],
)

# vector specifications structured as: [x_start, y_start, direction_degrees, magnitude]
vector_2 = [-82, 40.5, 138, 3]
vector_3 = [-71.2, 45, -115.7, 6]
# Create a list of lists that include each vector information
vectors = np.array([vector_2] + [vector_3])

fig.plot(
    data=vectors,
    style=style,
    pen="1p",
    color="yellow",
)

fig.show()

########################################################################################
# Another example of plotting cartesian vectors over a coast plot. This time
# a Transverse Mercator projection is used. Additionally, ``numpy.linespace``
# is used to create 5 vectors with equal stops.

# create a plot with coast, Mercator projection (M) over the continental US
fig = pygmt.Figure()
fig.coast(
    region=[20, 50, 30, 45],
    projection="T35/12c",
    frame=True,
    borders=1,
    area_thresh=4000,
    shorelines="0.25p,black",
    land="lightbrown",
    water="lightblue",
)

x = np.linspace(36, 42, 5)  # x values = [36.  37.5 39.  40.5 42. ]
y = np.linspace(39, 39, 5)  # y values = [39. 39. 39. 39.]
direction = np.linspace(-90, -90, 5)  # direction values = [-90. -90. -90. -90.]
length = np.linspace(1.5, 1.5, 5)  # length values = [1.5 1.5 1.5 1.5]

fig.plot(
    x=x,
    y=y,
    style="v0.4c+ea",
    pen="0.6p",
    color="red3",
    direction=[direction, length],
)


fig.show()

########################################################################################
# # Plot Circular Vectors
# ----------
#
# Circular vectors can be plotted using an ``x_start`` and ``y_start`` value to
# specify where the origin of the circle will be located on the plane. The
# variable ``radius`` is used to specify the radius of the circle while the
# ``degree_start`` and ``degree_stop`` parameters specify at what angle the arc
# will begin and end respectively.

# vector specifications structured as: [x_start, y_start, radius, degree_start, degree_stop]
data = np.array([[4, 4, 2, 90, 270]])

fig = pygmt.Figure()
fig.plot(
    region=[0, 8, 0, 8],
    projection="X10c/10c",
    frame="a",
    data=data,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)
fig.show()



########################################################################################
# FIXME: Everything after this is from ``lines.py`` and must be removed
#
# Additional line segments can be added by including additional values for ``x``
# and ``y``.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 6, 9],
    y=[5, 7, 4],
    pen="1p,black",
)
fig.show()

########################################################################################
# To plot multiple lines, :meth:`pygmt.Figure.plot` needs to be used for each
# additional line. Arguments such as ``region``, ``projection``, and ``frame`` do
# not need to be repeated in subsequent uses.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 6, 9],
    y=[5, 7, 4],
    pen="2p,blue",
)
fig.plot(x=[2, 4, 10], y=[3, 8, 9], pen="2p,red")
fig.show()

########################################################################################
# Change line attributes
# ----------------------
#
# The line attributes can be set by the ``pen`` parameter. ``pen`` takes a string
# argument with the optional values *width*,\ *color*,\ *style*.
#
# In the example below, the pen width is set to ``5p``, and with ``black`` as the
# default color and ``solid`` as the default style.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 8],
    y=[3, 9],
    pen="5p",
)
fig.show()

########################################################################################
# The line color can be set and is added after the line width to the ``pen`` parameter.
# In the example below, the line color is set to ``red``.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 8],
    y=[3, 9],
    pen="5p,red",
)
fig.show()

########################################################################################
# The line style can be set and is added after the line width or color to the
# ``pen`` parameter.  In the example below, the line style is set to
# ``..-`` (*dot dot dash*), and the default color ``black`` is used.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 8],
    y=[3, 9],
    pen="5p,..-",
)
fig.show()

########################################################################################
# The line width, color, and style can all be set in the same ``pen`` parameter. In the
# example below, the line width is set to ``7p``, the color is set to ``green``, and the
# line style is ``-.-`` (*dash dot dash*).
#
# For a gallery showing other ``pen`` settings, see :doc:`/gallery/lines/linestyles`.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X25c/20c",
    frame="a",
    x=[1, 8],
    y=[3, 9],
    pen="7p,green,-.-",
)
fig.show()

########################################################################################
# # Plot Geographic Vectors
# ----------

fig = pygmt.Figure()
fig.plot(
    region=[0, 8, 0, 8],
    projection="X10c/10c",
    frame="a",
    data=data,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# Georgraphic Vector using the `fig.coast` of the region of the United States.
# The plotting of the georgraphic vectors when using latitude and longitude
# are labeled by having Latitude negative, coming first and longitude come second.
# Then and array is created to create the vectors to follow the one before. 
import pygmt
import numpy as np
fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M15c",
    frame=True,
    borders=1,
    area_thresh=4000,
    shorelines="0.25p,black",
)
# Plot geographic vectors using latitude and longitude.
ME = [-69.4455, 45.2538]
CHI = [-87.6298, 41.8781]
SEA = [-122.3321, 47.6062]
NO = [-90.0715, 29.9511]
KC = [-94.5786, 39.0997]
CA = [-119.4179, 36.7783]
# Add array to piece together the vectors.
data = np.array([ME + CHI, CHI + SEA, SEA + KC, KC + NO, NO + CA])
fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()
########################################################################################
# Geographic graph using x and y values to set a start and an ending point.
# Use `fig.coast` to display the ouput of a coast. `x` and `y` are cordinates
# on a grid. `x` which is Idaho and `y` is chicago. The geographical vector
# is going from Idaho to Chicago.

import pygmt
import numpy as np
fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M15c",
    frame=True,
    borders=1,
    area_thresh=4000,
    shorelines="0.25p,black",
)
x = [-114.7420, 44.0682]
y = [-87.6298, 41.8781]
data = np.array([x + y])

fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()

#################################################################################

import pygmt
import numpy as np

fig = pygmt.Figure()
fig.coast(
    shorelines="1/0.5p",
    region=[-180, -20, 0, 90],
    projection="Poly/12c",
    land="gray",
    borders="1/thick,black",
    frame="afg10",
)
x = [-99.1332, 19.4326]
y = [-69.4455, 45.2538]
z = [-122.5210, 47.6249]
data = np.array([x + y, y + z])

fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()
