"""
3D Scatter plots
----------------

The :meth:`pygmt.Figure.plot3d` method can be used to plot symbols in 3D.
In the example below, we show how the
`Iris flower dataset <https://en.wikipedia.org/wiki/Iris_flower_data_set>`__
can be visualized using a perspective 3D plot. The ``region``
parameter has to include the :math:`x`, :math:`y`, :math:`z` axis limits in the
form of (xmin, xmax, ymin, ymax, zmin, zmax), which can be done automatically
using :meth:`pygmt.info`. To plot the z-axis frame, set ``frame`` as a
minimum to something like ``frame=["WsNeZ", "zaf"]``. Use ``perspective`` to
control the azimuth and elevation angle of the view, and ``zscale`` to adjust
the vertical exaggeration factor.
"""

import pandas as pd
import pygmt

# Load sample iris data and convert 'species' column to categorical dtype
df = pd.read_csv("https://github.com/mwaskom/seaborn-data/raw/master/iris.csv")
df.species = df.species.astype(dtype="category")
# Make a list of the indiviudal categories of the 'species' column
# ['setosa', 'versicolor', 'virginica']
# By default they are in alphabetical order
labels = list(df.species.cat.categories)

# Use pygmt.info to get region bounds (xmin, xmax, ymin, ymax, zmin, zmax)
# The below example will return a numpy array [0.0, 3.0, 4.0, 8.0, 1.0, 7.0]
region = pygmt.info(
    data=df[["petal_width", "sepal_length", "petal_length"]],  # x, y, z columns
    per_column=True,  # report the min/max values per column as a numpy array
    # round the min/max values of the first three columns to the nearest
    # multiple of 1, 2 and 0.5, respectively
    spacing=(1, 2, 0.5),
)

# Make a 3D scatter plot, coloring each of the 3 species differently
fig = pygmt.Figure()

# Define a colormap to be used for three categories, define the range of the
# new discrete CPT using series=(lowest_value, highest_value, interval), use
# color_model="+cSetosa,Versicolor,Virginica" to write the discrete color
# palette "cubhelix" in categorical format and add the species names as
# annotations for the colorbar

# Please note that by default pandas assigns the categorical number code
# in a lexical or alphabetical manner to the individual categories.
# Thus, also the labels for the colorbar have to be given to color_model
# in alphabetical order.
# In case you want another or non-alphabetical order, you firstly have
# to adjust the categorical number code. For handling and manipulating
# categorical data in pandas you may have a look at:
# https://pandas.pydata.org/docs/user_guide/categorical.html

pygmt.makecpt(
    cmap="cubhelix",
	# Use the minum and maximum of the categorical number code
	# to set the lowest_value and the highest_value of the CPT
    series=(df.species.cat.codes.min(), df.species.cat.codes.max(), 1),
	# convert ['setosa', 'versicolor', 'virginica'] to 'setosa,versicolor,virginica'
    color_model="+c" + ",".join(labels),
)

fig.plot3d(
    # Use petal width, sepal length and petal length as x, y and z data input,
    # respectively
    x=df.petal_width,
    y=df.sepal_length,
    z=df.petal_length,
    # Vary each symbol size according to another feature (sepal width, scaled
    # by 0.1)
    size=0.1 * df.sepal_width,
    # Use 3D cubes ("u") as symbols, with size in centimeter units ("c")
    style="uc",
    # Points colored by categorical number code
    color=df.species.cat.codes.astype(int),
    # Use colormap created by makecpt
    cmap=True,
    # Set map dimensions (xmin, xmax, ymin, ymax, zmin, zmax)
    region=region,
    # Set frame parameters
    frame=[
        'WsNeZ3+t"Iris flower data set"',  # z axis label positioned on 3rd corner, add title
        'xafg+l"Petal Width (cm)"',
        'yafg+l"Sepal Length (cm)"',
        'zafg+l"Petal Length (cm)"',
    ],
    # Set perspective to azimuth NorthWest (315°), at elevation 25°
    perspective=[315, 25],
    # Vertical exaggeration factor
    zscale=1.5,
)

# Add colorbar legend
fig.colorbar(xshift=3.1)

fig.show()
