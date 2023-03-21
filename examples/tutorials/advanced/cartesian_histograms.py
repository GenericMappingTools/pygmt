r"""
Cartesian histograms
====================

Cartesian histograms can be generated using the :meth:`pygmt.Figure.histogram`
method. In this tutorial different aspects regarding histograms are addressed:

- vertical and horizontal bars
- counts and frequency percent
- cumulative values
- color or pattern as fill for the bars
- overlaid, stacked, and grouped bars
"""

# sphinx_gallery_thumbnail_number = 3


# Import the required packages
import numpy as np
import pygmt

###############################################################################
# Generate random data from a normal distribution

np.random.seed(100)

# Mean of distribution
mean = 100
# Standard deviation of distribution
stddev = 20

# Create two data sets
data01 = mean + stddev * np.random.randn(42)
data02 = mean + stddev * 2 * np.random.randn(42)


###############################################################################
# Vertical and horizontal bars
# ----------------------------
# To define the width of the bins the ``series`` parameter has to be specified.
# The bars can be filled via the ``fill`` parameter with either a color or a
# pattern (see later in this tutorial). Use the ``pen`` parameter to adjust the
# outline of the bars. Choose the histogram type via the ``histtpye``
# parameter, e.g., ``0`` for counts [Default] or ``1`` for frequency percent.

# Create new figure instance
fig = pygmt.Figure()

# Create histogram for data01
fig.histogram(
    region=[0, 200, 0, 10],  # x_min, x_max, y_min, y_max
    projection="X10c",  # Cartesian projection with a width of 10 centimeters
    # Add frame, annotations (a), ticks (f), and y-axis label (+l) "Counts"
    # The numbers give the steps of annotations and ticks
    frame=["WSne", "xaf10", "ya5f1+lCounts"],
    data=data01,
    # Set the bin width via the "series" parameter
    series=10,
    # Fill the bars with color "red3"
    fill="red3",
    # Draw a black 1-point thick outline around the bars via the "pen"
    # parameter
    pen="1p",
    # Choose counts via the "histtype" parameter
    histtype=0,
)

fig.show()

###############################################################################
# By default, a histogram with vertical bars is created. Horizontal bars can
# be achieved via ``horizontal=True``.

fig = pygmt.Figure()

fig.histogram(
    region=[0, 200, 0, 10],
    projection="X10c",
    frame=["WSne", "xaf10", "ya5f1+lCounts"],
    data=data01,
    series=10,
    fill="red3",
    pen="1p",
    histtype=0,
    # Use horizontal bars
    # Please note the flip of the x and y axes regarding annotations, ticks,
    # gridlines and labels
    horizontal=True,
)

fig.show()


###############################################################################
# Cumulative values
# -----------------
# To create a histogram showing the cumulative values set ``cumulative=True``.
# Here, the bars of the cumulative histogram are filled with a pattern via
# the ``fill`` parameter. Labels for the legend can be specified via the
# ``label`` parameter.

fig = pygmt.Figure()

# Create histogram for data01
fig.histogram(
    region=[0, 200, 0, 51],
    projection="X10c",
    frame=["WSne", "xaf10", "ya5f1+lCounts"],
    data=data01,
    series=10,
    fill="red3",
    pen="1p",
    histtype=0,
    # Set label used in legend
    label="data01",
)

# Create cumulative histogram for data01
fig.histogram(
    data=data01,
    series=10,
    # Use pattern (p) number 8 as fill for the bars
    # Set the background (+b) to transparent due to not giving a color
    # Set the foreground (+f) to black [Default]
    fill="p8+b+fblack",
    pen="1p",
    histtype=0,
    # Calculate cumulative values
    cumulative=True,
    label="data01 cumulative",
)

# Add legend within the bounding box of the plot (lower-case j)
# at position Left Top
fig.legend(position="jLT")

fig.show()


###############################################################################
# Overlaid bars
# -------------
# Limitations
#
# - Mixing of colors or/and patterns
# - More colors or/and patterns than data sets
# - Visually a "third histogram"

fig = pygmt.Figure()

with fig.subplot(
    nrows=1,
    ncols=2,
    figsize=("20c", "10c"),
):
    with fig.set_panel(panel=0):
        # Create histogram for data02
        fig.histogram(
            region=[0, 200, 0, 10],
            projection="X10c",
            frame=["WSne", "xaf10", "ya5f1+lConunts"],
            data=data02,
            series=10,
            fill="orange",
            pen="1p",
            histtype=0,
        )

    with fig.set_panel(panel=1):
        # Create histogram for data01
        fig.histogram(
            region=[0, 200, 0, 10],
            projection="X10c",
            frame=["wSne", "xaf10", "ya5f1"],
            data=data01,
            series=10,
            fill="red3",
            pen="1p",
            histtype=0,
            label="data01",
        )
        # Create histogram for data02
        # It is plotted on top of the histogram for data01
        fig.histogram(
            region=[0, 200, 0, 10],
            projection="X10c",
            data=data02,
            series=10,
            # Fill bars with color "orange", use a transparency of 50% ("@50")
            fill="orange@50",
            pen="1p",
            histtype=0,
            label="data02",
        )

        # Add legend
        fig.legend()

fig.show()


###############################################################################
# Stacked bars
# ------------
# Limitations
#
# - No common baseline
# - Partly not directly clear whether overlaid or stacked

# Combined the two data sets to one data set
data_merge = np.concatenate((data01, data02), axis=None)

fig = pygmt.Figure()

with fig.subplot(
    nrows=1,
    ncols=2,
    figsize=("20c", "10c"),
):
    with fig.set_panel(panel=0):
        # Create histogram for data02
        fig.histogram(
            region=[0, 200, 0, 20],
            projection="X10c",
            frame=["WSne", "xaf10", "ya5f1+lConunts"],
            data=data02,
            series=10,
            fill="orange",
            pen="1p",
            histtype=0,
        )

    with fig.set_panel(panel=1):
        # Create histogram for data01
        fig.histogram(
            region=[0, 200, 0, 20],
            projection="X10c",
            frame=["wSne", "xaf10", "ya5f1+lConunts"],
            data=data_merge,
            series=10,
            fill="orange",
            pen="1p",
            histtype=0,
            label="data02",
        )
        # Create histogram for data02
        fig.histogram(
            region=[0, 200, 0, 20],
            projection="X10c",
            data=data01,
            series=10,
            fill="red3",
            pen="1p",
            histtype=0,
            label="data01",
        )

        # Add legend
        fig.legend()

fig.show()


###############################################################################
# Grouped bars
# ------------
# By setting the ``barwidth`` parameter in respect to the values passed to the
# ``series`` parameter histgrams with grouped bars can be created.
#
# Limitation
#
# - Careful setting the bar width in respect to the bin width in case of
#   continuous data

# Width used for binning the data
binwidth = 10

fig = pygmt.Figure()

# Create histogram for data01
fig.histogram(
    region=[0, 200, 0, 10],
    projection="X10c",
    frame=["WSne", "xaf10g10", "ya5f1+lCounts"],
    data=data01,
    series=binwidth,
    fill="red3",
    pen="1p",
    histtype=0,
    # Calculate the bar width in respect to the bin width, here for two
    # data sets half of the bin width
    # Offset (+o) the bars to align each bar with the left limit of the
    # corresponding bin
    barwidth=str(binwidth / 2) + "+o-" + str(binwidth / 4),
    label="data01",
)

# Create histogram for data02
fig.histogram(
    region=[0, 200, 0, 10],
    projection="X10c",
    data=data02,
    series=binwidth,
    fill="orange",
    pen="1p",
    histtype=0,
    barwidth=str(binwidth / 2) + "+o" + str(binwidth / 4),
    label="data02",
)

# Add legend
fig.legend()

fig.show()
