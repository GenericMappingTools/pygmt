"""
Plotting vectors
================

Plotting vectors is handled by :meth:`pygmt.Figure.plot`.

.. note::

    This tutorial assumes the use of a Python notebook, such as IPython or Jupyter Notebook.
    To see the figures while using a Python script instead, use
    ``fig.show(method="external")`` to display the figure in the default PDF viewer.

    To save the figure, use ``fig.savefig("figname.pdf")`` where ``"figname.pdf"``
    is the desired name and file extension for the saved figure.
"""
# sphinx_gallery_thumbnail_number = 6

import numpy as np
import pygmt

########################################################################################
# Plot Cartesian Vectors
# ----------------------
#
# Create a simple Cartesian vector using a starting point through
# ``x``, ``y``, and ``direction`` parameters.
# On the shown figure, the plot is projected on a 10cm X 10cm region,
# which is specified by the ``projection`` parameter.
# The direction is specified
# by a list of two 1d arrays structured as ``[[angle_in_degrees], [length]]``.
# The angle is measured in degrees and moves counter-clockwise from the
# horizontal.
# The length of the vector also uses centimeters by default but
# could be changed using :meth:`pygmt.config`
# (Check the next examples for unit changes).
#
# Notice that the ``v`` in the ``style`` parameter stands for
# vector; it distinguishes it from regular lines and allows for
# different customization. ``0c`` is used to specify the size
# of the arrow head which explains why there is no arrow on either
# side of the vector.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    x=2,
    y=8,
    style="v0c",
    direction=[[-45], [6]],
)
fig.show()

########################################################################################
# In this example, we apply the same concept shown previously to plot multiple
# vectors. Notice that instead of passing int/float to ``x`` and ``y``, a list
# of all x and y coordinates will be passed. Similarly, the length of direction
# list will increase accordingly.
#
# Additionally, we change the style of the vector to include a red
# arrow head at the end (**+e**) of the vector and increase the thickness of the vector stem. A list of different
# styling attributes can be found in
# :doc:`Vector heads and tails </gallery/lines/vector_heads_tails>`.

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c/10c",
    frame="ag",
    x=[2, 4],
    y=[8, 1],
    style="v0.6c+e",
    direction=[[-45, 23], [6, 3]],
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# The default unit of vector length is centimeters,
# however, this can be changed to inches or points. Note that, in PyGMT,
# one point is defined as 1/72 inch.
#
# In this example, the graphed region is 5in X 5in, but
# the length of the first vector is still graphed in centimeters.
# Using ``pygmt.config(PROJ_LENGTH_UNIT="i")``, the default unit
# can be changed to inches in the second plotted vector.

fig = pygmt.Figure()
# Vector 1 with default unit as cm
fig.plot(
    region=[0, 10, 0, 10],
    projection="X5i/5i",
    frame="ag",
    x=2,
    y=8,
    style="v1c+e",
    direction=[[0], [3]],
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
# a 2D list or numpy array containing all vectors.
# Each vector list contains the information structured as:
# ``[x_start, y_start, direction_degrees, length]``
#
# If this approach is chosen, the ``data`` parameter must be
# used instead of ``x``, ``y`` and  ``direction``.

# Create a list of lists that include each vector information
vectors = [[2, 3, 45, 4]]  # vectors structure: [[ 2  3 45  4]]

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
# vector could be simply added to the 2D list or numpy
# array object
# and passed using ``data`` parameter.

# vector specifications structured as: [x_start, y_start, direction_degrees, length]
vector_1 = [2, 3, 45, 4]
vector_2 = [7.5, 8.3, -120.5, 7.2]
# Create a list of lists that include each vector information
vectors = np.array([vector_1, vector_2])
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
# longitude and y values represent the latitude where the vector starts.
#
# This example also shows some of the styles a vector supports.
# ``+ba`` specifies that the begining point of the vector ``+b``
# should take the shape of a circle ``c``. Similarly, the end
# point of the vector ``+e`` should have an arrow shape ``a``
# (to draw a plain arrow, use ``A`` instead). Lastly, the ``+a``
# specifies the angle of the vector head apex (30 degrees in
# this example).
#
# More styling options can be found here
# :doc:`Vector heads and tails </gallery/lines/vector_heads_tails>`.

# create a plot with coast, Mercator projection (M) over the continental US
fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M10c",
    frame="ag",
    borders=1,
    shorelines="0.25p,black",
    area_thresh=4000,
    land="grey",
    water="lightblue",
)

style = "v0.4c+bc+ea+a30"
fig.plot(
    x=-110,
    y=40,
    style=style,
    pen="1p",
    color="red3",
    direction=[[-25], [3]],
)

# vector specifications structured as: [x_start, y_start, direction_degrees, length]
vector_2 = [-82, 40.5, 138, 2.5]
vector_3 = [-71.2, 45, -115.7, 4]
# Create a list of lists that include each vector information
vectors = [vector_2, vector_3]

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
    projection="T35/10c",
    frame=True,
    borders=1,
    shorelines="0.25p,black",
    area_thresh=4000,
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
    style="v0.4c+ea+bc",
    direction=[direction, length],
    pen="0.6p",
    color="red3",
)


fig.show()

########################################################################################
# Plot Circular Vectors
# ---------------------
#
# When plotting circular vectors, there are 5 values that should be included in
# a 2D list or ``np.array()`` object in order to create
# a valid plot. The vectors must be passed to the ``data`` parameter.
# The first two values in ``circular_vector_1`` represent the origin of the
# circle that will be plotted. The next value is the radius which is represented
# on the plot in centimeters. Finally, the last two values represent the degree
# at which the plot will start and stop. In this example, the result shown is the
# left half of a circle as the plot starts at 90 degrees and goes until 270.
# It is important to note that when plotting circular vectors, the style value
# should begin with an ``m``.

# vector specifications structured as: [x_start, y_start, radius, degree_start, degree_stop]
circular_vector_1 = [0, 0, 2, 90, 270]

data = [circular_vector_1]

fig = pygmt.Figure()
fig.plot(
    region=[-5, 5, -5, 5],
    projection="X10c",
    frame="ag",
    data=data,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)

# Another example using np.array()
circular_vector_2 = [0, 0, 4, -90, 90]

data = np.array([circular_vector_2])

fig.plot(
    data=data,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# When plotting multiple vectors there is a multitude of numpy functions
# that can make this process easier. In the following example, three main numpy
# functions are used. The first of which is ``np.arange`` which iterates from 0
# to the value of ct. This function is used to generate random data points for
# ``radius`` and ``stopdir`` since these values are intended to be different in
# each of the five vectors begin plotted. The second function is ``np.full``
# which creates a ``numpy.ndarray``. Finally, all of this data is congregated into
# a final ``numpy.ndarray`` called data using ``np.column_stack``. This is then
# passed to the plot function and the resulting figure is shown below.

ct = 5
radius = 3 - (0.5 * np.arange(0, ct))
startdir = np.full(ct, 90)
stopdir = 180 + (50 * np.arange(0, ct))

data = np.column_stack([np.full(ct, 0), np.full(ct, 0), radius, startdir, stopdir])

fig = pygmt.Figure()
fig.plot(
    region=[-5, 5, -5, 5],
    projection="X10c",
    frame="ag",
    data=data,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# Much like when plotting regular vectors, the default unit used is centimeters.
# When this is changed to inches, the size of the plot appears larger when the
# projection units do not change. Below is an example of two circular vectors.
# One is plotted using the default unit, and the second is plotted using inches.
# The difference in size of the two vectors provides good insight into how this
# functionality works.

circular_vector_1 = [6, 5, 2, 90, 270]
circular_vector_2 = [6, 5, 1, 90, 270]

data_1 = [circular_vector_1]

fig = pygmt.Figure()
fig.plot(
    region=[0, 10, 0, 10],
    projection="X10c",
    frame="ag",
    data=data_1,
    style="m0.5c+ea",
    pen="2p",
    color="red3",
)

data_2 = [circular_vector_2]
with pygmt.config(PROJ_LENGTH_UNIT="i"):
    fig.plot(
        data=data_2,
        style="m0.5c+ea",
        pen="2p",
        color="red3",
    )
fig.show()

########################################################################################
# Plot Geographic Vectors
# -----------------------
# Geographic graph using x and y values to set a start and an ending point.
# Use ``fig.coast`` to plot a coast. ``x`` and ``y`` are coordinates
# on a grid that we are using. ``x`` is Idaho and ``y`` is Chicago in this example.
# The geographical vector is going from Idaho to Chicago. To style geographic
# vectors, use ``=`` at the begining of the ``style`` parameter.
# Other styling features such as arrow head color and line thickness
# can be passed into
# ``pen`` and ``color``parameters

fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M10c",
    frame=True,
    borders=1,
    shorelines="0.25p,black",
    area_thresh=4000,
)
point_1 = [-114.7420, 44.0682]
point_2 = [-87.6298, 41.8781]
data = np.array([point_1 + point_2])

fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()

########################################################################################
# This Geographic Vector is using the `fig.coast` of the region of the United States.
# The plotting of the geographic vectors when using latitude and longitude
# are labeled by having the coordinates displayed.
# Then an array is created so the vectors follow the one vector before it. You
# can diplay this array any way you want.

fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M10c",
    frame=True,
    borders=1,
    shorelines="0.25p,black",
    area_thresh=4000,
)
# Plot geographic vectors using coordinates.
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

#################################################################################
# This is a polyconic projection of geographic vectors. This projection
# is set to poly. The MC, ME, WA variables are connected to Mexico City (MC)
# Maine (ME), and Washington (WA). Each variable has a coordinate corrensponding
# that place.

fig = pygmt.Figure()
fig.coast(
    shorelines="1/0.5p",
    region=[-180, -20, 0, 90],
    projection="Poly/12c",
    land="gray",
    borders="1/thick,black",
    frame="afg10",
)
MC = [-99.1332, 19.4326]
ME = [-69.4455, 45.2538]
WA = [-122.5210, 47.6249]
data = np.array([MC + ME, ME + WA])

fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()

################################################################################
# This geographic vector is using the Mercator projection. For this we have
# ``fig.coast`` with the region, frame, land and projection type. Then for the vector
# points we are starting at SA which is South Africa and going to four different
# places.

fig = pygmt.Figure()
fig.coast(
    region=[-180, 180, -80, 80],
    frame="afg",
    land="lightbrown",
    water="lightblue",
    projection="M0/0/12c",
)
SA = [22.9375, -30.5595]
EUR = [15.2551, 54.5260]
ME = [-69.4455, 45.2538]
AS = [100.6197, 34.0479]
NM = [-105.8701, 34.5199]
data = np.array([SA + EUR, SA + ME, SA + AS, SA + NM])

fig.plot(
    data=data,
    style="=0.5c+ea+s",
    pen="2p",
    color="red3",
)
fig.show()
