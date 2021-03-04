"""
Color points by categories
---------------------------
The :meth:`pygmt.Figure.plot` method can be used to plot symbols which are
color-coded by categories.
"""

import numpy as np
import pandas as pd
import pygmt

# Load sample iris data, and convert 'species' column to categorical dtype
df = pd.read_csv("https://github.com/mwaskom/seaborn-data/raw/master/iris.csv")
df["species"] = df.species.astype(dtype="category")

# Use pygmt.info to get region bounds (xmin, xmax, ymin, ymax)
# The below example will return a numpy array like [2.  4.4 4.3 7.9]
region = pygmt.info(
    table=df[["sepal_width", "sepal_length"]],  # x and y columns
    per_column=True,  # report output as a numpy array
)

# Make our 2D categorial scatter plot, coloring each of the 3 species differently
fig = pygmt.Figure()

# Generate basemap of 10cm x 10cm size
fig.basemap(
    region=region,
    projection="X10c/10c",
    frame=['xafg+l"Sepal Width"', 'yafg+l"Sepal Length"', "WSen"],
)

# Define colormap to use for three categories
pygmt.makecpt(cmap="inferno", color_model="+c", series=(0, 3, 1))

fig.plot(
    x=df.sepal_width,  # Use one feature as x data input
    y=df.sepal_length,  # Use another feature as y data input
    sizes=df.petal_width
    / df.petal_length,  # Vary each symbol size according to the ratio of the two remaining features
    color=df.species.cat.codes.astype(int),  # Points colored by categorical number code
    cmap=True,  # Use colormap created by makecpt
    no_clip=True,  # Do not clip symbols that fall exactly on the map bounds
    style="cc",  # Use circles as symbols with size in centimeter units
    transparency=40,  # Set transparency level for all symbols to deal with overplotting
)

fig.show()
