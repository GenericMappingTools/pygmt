r"""
Dynamic data visualization using ``Panel``
==========================================
*Please run the following code examples in a notebook environment otherwise
the interactive parts of this tutorial will not work. You can use the button
"Download Jupyter notebook: panel_extension.ipynb" at the bottom of this page
to download this script as a Jupyter notebook.*

The library ``Panel`` (https://panel.holoviz.org/index.html) can be used to
create interactive dashboards by connecting user-defined widgets to plots.
``Panel`` can be used as an extension to Jupyter notebook / lab.

This tutorial is split into three parts:
- Make a static map
- Make a dynamic map
- Add a grid for Earth relief
"""

# sphinx_gallery_thumbnail_number = 1


# Import the requiered packages
import numpy as np
import panel as pn
import pygmt

pn.extension()


###############################################################################
# Make a static map
# -----------------

# Create figure instance
fig = pygmt.Figure()
fig.coast(
    projection="G30/15/10c",  # Orthographic projection
    region="g",  # global
    frame="g30",  # Add gridlines in steps of 30 degrees on top
    land="gray",
    water="lightblue",
    shorelines="1/0.25p,gray50",
)
fig.show()


###############################################################################
# Make a dynamic map
# ------------------
# Vary the central longitude used for the Orthographic projection to create
# a rotation of the Earth around the vertical axis.

# Create a slider
slider_lon = pn.widgets.DiscreteSlider(
    name="Central longitude",
    options=list(np.arange(0, 361, 10)),
    value=0,
)


# Define a function for plotting the single slices
@pn.depends(central_lon=slider_lon)
def view(central_lon):
    # Create figure instance
    fig = pygmt.Figure()
    fig.coast(
        # Vary the central longitude used for the Orthographic projection
        projection="G" + str(central_lon) + "/15/12c",
        region="g",
        frame="g30",  # Add gridlines in steps of 30 degrees on top
        land="gray",
        water="lightblue",
        shorelines="1/0.25p,gray50",
    )
    return fig


# Make an interactive dashboard
pn.Column(slider_lon, view)


###############################################################################
# Add a grid for Earth relief
# ---------------------------

# Download a grid for Earth relief
grd_relief = pygmt.datasets.load_earth_relief(resolution="10m")

# Create a slider
slider_lon = pn.widgets.DiscreteSlider(
    name="Central longitude",
    options=list(np.arange(0, 361, 10)),
    value=0,
)


# Define a function for plotting the single slices
@pn.depends(central_lon=slider_lon)
def view(central_lon):
    # Create figure instance
    fig = pygmt.Figure()
    # Set up a colormap for the elevation
    pygmt.makecpt(
        cmap="oleron",
        series=[int(np.min(grd_relief)), int(np.max(grd_relief))+1, 100],
    )
    # Plot the grid for the elevation
    fig.grdimage(
        projection="G" + str(central_lon) + "/15/12c",
        region="g",
        grid=grd_relief,  # Use gird downloaded above
        cmap=True,  # Use colormap defined above
        frame="g30",  # Add gridlines in steps of 30 degrees on top
    )
    # Add a colorbar for the elevation
    fig.colorbar(frame=["a2000f1000", "x+lElevation", "y+lm"])
    return fig


# Make an interactive dashboard
pn.Column(slider_lon, view)

