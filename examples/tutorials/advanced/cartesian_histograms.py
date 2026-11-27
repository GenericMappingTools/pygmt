"""
Cartesian histograms
====================

Cartesian histograms can be generated using the :meth:`pygmt.Figure.histogram` method.
In this tutorial, different histogram related aspects are addressed:

- General set up: bin width, bar fill
- Histogram styles: bar orientation, stair-steps
- Histogram types: count and frequency percent, cumulative values, distribution curve
- Multi-dataset histograms: grouped bars, stacked bars, overlayed bars
"""

# %%
import numpy as np
import pygmt
from pygmt.params import Axis, Frame, Pattern

# %%
# Generate random data from a normal distribution:

rng = np.random.default_rng(seed=100)

# Mean of distribution
mean = 100
# Standard deviation of distribution
stddev = 20

# Create two data sets
data1 = rng.normal(loc=mean, scale=stddev, size=42)
data2 = rng.normal(loc=mean, scale=stddev * 2, size=42)


# %%
# General set up
# --------------
#

# %%
# Bin width: ``series`` parameter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To define the width of the bins, the ``series`` parameter has to be specified.
# Use the ``pen`` parameter to adjust width, color, and style of the outlines.

fig = pygmt.Figure()

fig.histogram(
    # Define the plot range as a list of xmin, xmax, ymin, ymax
    # Let ymin and ymax determined automatically by setting both to the same value
    region=[0, 200, 0, 0],
    # Cartesian projection with a width of 8 centimeters
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    # Set the bin width via the "series" parameter based on region
    series=10,
    pen="0.5p,gray30",
)

# Shift plot origin by the previous plot's width ("+w") plus 2 centimeters to the right
fig.shift_origin(xshift="w+2c")

fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    # Set minimum, maximum and bin with for the bins
    series=[75, 120, 10],
    pen="0.5p,gray30",
)

fig.shift_origin(xshift="w+2c")

fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    # Set bin boundaries explicitly
    series=np.array([50, 75, 80, 90, 100, 110, 120, 140, 180]),
    pen="0.5p,gray30",
)

fig.show()


# %%
# Bar fill: ``fill`` and ``cmap`` parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The bars can be filled via the ``fill`` parameter with either a color (or a pattern).
# Besides a constant color, ``fill`` can take two specific arguments, ``"position"`` and
# ``"value"`` using the mid-coordinate or the value (count or percent) of the bin,
# respectively. Both require creating a colormap via :func:`pygmt.makecpt` first and
# setting ``cmap=True``. It's also possible to pass the filename (with extension) of a
# CPT to ``cmap`` previsouly created and saved, but it is not supported to directly pass
# a GMT master CPT yet.

fig = pygmt.Figure()

fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
)

fig.shift_origin(xshift="w+2c")

pygmt.makecpt(cmap="SCM/batlow", series=[0, 200, 10])
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="position",
    cmap=True,
    pen="0.5p,gray30",
)
fig.colorbar(label="mid-coordinate of bin")

fig.shift_origin(xshift="w+3.5c")

pygmt.makecpt(cmap="SCM/batlow", series=[0, 15, 1])
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="value",
    cmap=True,
    pen="0.5p,gray30",
)
fig.colorbar(label="count of bin")

fig.show()


# %%
# Histogram styles
# ----------------
#

# %%
# Bar orientation
# ~~~~~~~~~~~~~~~
#
# By default, a histogram with vertical bars is created. Horizontal bars can be
# achieved via ``horizontal=True``.

fig = pygmt.Figure()

# Create histogram for data1 with vertical bars
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
)

fig.shift_origin(xshift="w+2c")

# Create histogram for data1 with horizontal bars
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
    # Use horizontal bars. Note that the x- and y-axes are flipped, with the x-axis
    # plotted vertically and the y-axis plotted horizontally.
    horizontal=True,
)

fig.show()


# %%
# Stair-steps
# ~~~~~~~~~~~
#
# A stair-step diagram can be created by setting ``stairs=True``. Then only the
# outer outlines of the bars are drawn, and no internal bars are visible.

fig = pygmt.Figure()

# Create histogram for data1 using bars
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
)

fig.shift_origin(xshift="w+2c")

# Create histogram for data1 using stair-steps
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
    stairs=True,
)

fig.show()


# %%
# Histogram types
# ---------------
#

# %%
# Counts and frequency percent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# By default, a histogram showing the counts in each bin is created
# (``histtype="count"``). To show the percentage of values in each bin, set the
# ``histtype`` parameter to ``"percent"``. For further
# options please have a look at the documentation of :meth:`pygmt.Figure.histogram`.

fig = pygmt.Figure()

# Create histogram for data2 showing counts
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data2,
    series=10,
    fill="bisque",
    pen="0.5p,gray30",
    # Choose counts via the "histtype" parameter
    histtype="count",
)

fig.shift_origin(xshift="w+2c")

# Create histogram for data2 showing frequency percent
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    # Add suffix % (+u)
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=2, tick=1, unit="%", label="Frequency percent"),
    ),
    data=data2,
    series=10,
    fill="bisque",
    pen="0.5p,gray30",
    # Choose percentages via the "histtype" parameter
    histtype="percent",
)

fig.show()


# %%
# Cumulative values
# ~~~~~~~~~~~~~~~~~
#
# To create a histogram showing the cumulative values set ``cumulative=True``. Here, the
# bars of the cumulative histogram are filled with a :class:`pygmt.params.Pattern` via
# the ``fill`` parameter. Annotate each bar with the counts it represents using the
# ``annot`` parameter.

fig = pygmt.Figure()

# Create histogram for data1 showing the counts per bin
fig.histogram(
    region=[0, 200, 0, len(data1) + 1],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=5, tick=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
    # Annotate each bar with the counts it represents
    annot=True,
)

fig.shift_origin(xshift="w+2c")

# Create histogram for data1 showing the cumulative counts
fig.histogram(
    region=[0, 200, 0, len(data1) + 1],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=5, tick=1, label="Cumulative counts"),
    ),
    data=data1,
    series=10,
    # Fill bars with GMT pattern 8, with white background and black foreground.
    fill=Pattern(8, bgcolor="white", fgcolor="black"),
    pen="0.5p,gray30",
    cumulative=True,
    annot=True,
    # Offset the annotations by 10 points in negative y-direction
    annot_offset="-10p",
)


fig.show()


# %%
# Distribution curve
# ~~~~~~~~~~~~~~~~~~
#
# Use the ``distribution`` parameter to plot equivalent normal distribution curves for
# mean, median, or lms additional on top of the histogram. Via ``distribution_pen`` pass
# a list of strings to adjust the pen used for the different curves.

fig = pygmt.Figure()

fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data2,
    series=10,
    fill="bisque",
    pen="0.5p,gray30",
    distribution=["mean", "median", "lms"],
    distribution_pen=["1.5p,cyan2", "1.5p,steelblue,4_2", "1.5p,darkblue,2_2"],
)

# Create legend
for pen, label in zip(
    ["1.5p,cyan2", "1.5p,steelblue,4_2", "1.5p,darkblue,2_2"],
    ["mean", "median", "lms"],
    strict=False,
):
    fig.plot(x=[-2, -1], y=[-2, -1], pen=pen, label=label)
fig.legend()

fig.show()


# %%
# Multi-dataset histograms
# ------------------------
#

# %%
# Overlaid bars
# ~~~~~~~~~~~~~
#
# Overlaid or overlapping bars can be achieved by plotting two or several histograms,
# each for one data set, on top of each other. The legend entry can be specified via
# the ``label`` parameter.
#
# Limitations of histograms with overlaid bars are:
#
# - Mixing of colors or/and patterns
# - Visually more colors or/and patterns than data sets
# - Visually a "third histogram" (or more in case of more than two data sets)

fig = pygmt.Figure()

# Create histogram for data1
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
    # Set legend entry
    label="data1",
)

# Create histogram for data2
# It is plotted on top of the histogram for data1
fig.histogram(
    data=data2,
    series=10,
    # Fill bars with color "bisque", use a transparency of 50% ("@50")
    fill="bisque@50",
    pen="0.5p,gray30",
    label="data2",
)

# Add legend
fig.legend()

fig.show()


# %%
# Stacked bars
# ~~~~~~~~~~~~
#
# Histograms with stacked bars are not directly supported by PyGMT. Thus, before
# plotting, combined data sets have to be created from the single data sets. Then,
# stacked bars can be achieved similar to overlaid bars via plotting two or several
# histograms on top of each other.
#
# Limitations of histograms with stacked bars are:
#
# - No common baseline
# - Partly not directly clear whether overlaid or stacked bars

# Combine the two data sets to one data set
data_merge = np.concatenate((data1, data2), axis=None)

fig = pygmt.Figure()

# Create histogram for data2 by using the combined data set
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data_merge,
    series=10,
    fill="bisque",
    pen="0.5p,gray30",
    # The combined data set appears in the final histogram visually as data set data2
    label="data2",
)

# Create histogram for data1
# It is plotted on top of the histogram for data2
fig.histogram(
    data=data1,
    series=10,
    fill="lightbrown",
    pen="0.5p,gray30",
    label="data1",
)

# Add legend
fig.legend()

fig.show()


# %%
# Grouped bars
# ~~~~~~~~~~~~
#
# By setting the ``bar_width`` parameter in respect to the values passed to the
# ``series`` parameter histograms with grouped bars can be created.
#
# Limitations of histograms with grouped bars are:
#
# - Careful setting width and position of the bars in respect to the bin width
# - Difficult to see the variations of the single data sets

# Width used for binning the data
binwidth = 10

fig = pygmt.Figure()
pygmt.config(MAP_GRID_PEN="0.01p,gray60,2_2")

# Create histogram for data1
fig.histogram(
    region=[0, 200, 0, 0],
    projection="X8c",
    frame=Frame(
        axes="WStr",
        xaxis=Axis(annot=20, tick=10, grid=10),
        yaxis=Axis(annot=1, label="Counts"),
    ),
    data=data1,
    series=binwidth,
    fill="lightbrown",
    pen="0.5p,gray30",
    # Calculate the bar width in respect to the bin width, here for two data sets half
    # of the bin width
    bar_width=binwidth / 2,
    # Offset the bars to align each bar with the left limit of the corresponding bin
    bar_offset=-binwidth / 4,
    label="data1",
)

# Create histogram for data2
fig.histogram(
    data=data2,
    series=binwidth,
    fill="bisque",
    pen="0.5p,gray30",
    bar_width=binwidth / 2,
    bar_offset=binwidth / 4,
    label="data2",
)

# Add legend
fig.legend()

fig.show()

# sphinx_gallery_thumbnail_number = 6
