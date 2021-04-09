"""
Plotting Datetime Charts
========================

Plotting datetime charts is handled by :meth:`pygmt.Figure.basemap`.

.. note::

    This tutorial assumes the use of a Python notebook, such as IPython or Jupyter Notebook.
    To see the figures while using a Python script instead, use
    ``fig.show(method="external")`` to display the figure in the default PDF viewer.

    To save the figure, use ``fig.savefig("figname.pdf")`` where ``"figname.pdf"``
    is the desired name and file extension for the saved figure.
"""
# sphinx_gallery_thumbnail_number = 0

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
# The length of the vector uses centimeters by default but
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
# arrow head at the end (**+e**) of the vector and increase the
# thickness (``pen="2p"``) of the vector stem. A list of different
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
# Vector 2 after changing default unit to inch
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
# ``[x_start, y_start, direction_degrees, length]``.
#
# If this approach is chosen, the ``data`` parameter must be
# used instead of ``x``, ``y`` and  ``direction``.

# Create a list of lists that include each vector information
vectors = [[2, 3, 45, 4]]

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
# array object and passed using ``data`` parameter.

# Vector specifications structured as: [x_start, y_start, direction_degrees, length]
vector_1 = [2, 3, 45, 4]
vector_2 = [7.5, 8.3, -120.5, 7.2]
# Create a list of lists that include each vector information
vectors = [vector_1, vector_2]
# Vectors structure: [[2, 3, 45, 4], [7.5, 8.3, -120.5, 7.2]]

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
# The beginning point of the vector (**+b**)
# should take the shape of a circle (**c**). Similarly, the end
# point of the vector (**+e**) should have an arrow shape (**a**)
# (to draw a plain arrow, use **A** instead). Lastly, the **+a**
# specifies the angle of the vector head apex (30 degrees in
# this example).

# Create a plot with coast, Mercator projection (M) over the continental US
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

# Plot a vector using the x, y, direction parameters
style = "v0.4c+bc+ea+a30"
fig.plot(
    x=-110,
    y=40,
    style=style,
    direction=[[-25], [3]],
    pen="1p",
    color="red3",
)

# vector specifications structured as: [x_start, y_start, direction_degrees, length]
vector_2 = [-82, 40.5, 138, 2.5]
vector_3 = [-71.2, 45, -115.7, 4]
# Create a list of lists that include each vector information
vectors = [vector_2, vector_3]

# Plot vectors using the data parameter.
fig.plot(
    data=vectors,
    style=style,
    pen="1p",
    color="yellow",
)
fig.show()

########################################################################################
# Another example of plotting cartesian vectors over a coast plot. This time
# a Transverse Mercator projection is used. Additionally, :func:`numpy.linspace`
# is used to create 5 vectors with equal stops.

x = np.linspace(36, 42, 5)  # x values = [36.  37.5 39.  40.5 42. ]
y = np.linspace(39, 39, 5)  # y values = [39. 39. 39. 39.]
direction = np.linspace(-90, -90, 5)  # direction values = [-90. -90. -90. -90.]
length = np.linspace(1.5, 1.5, 5)  # length values = [1.5 1.5 1.5 1.5]

# Create a plot with coast, Mercator projection (M) over the continental US
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

fig.plot(
    x=x,
    y=y,
    style="v0.4c+ea+bc",
    direction=[direction, length],
    pen="0.6p",
    color="red3",
)

fig.show()
