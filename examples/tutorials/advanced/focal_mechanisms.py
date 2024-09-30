"""
Plotting focal mechanisms
=========================

Focal mechanisms can be plotted with the :meth:`pygmt.Figure.meca` method.

TODO: Check GMT

- issue #7777 and PR #7778
- issue #8053
- PR #8059 ->  T pen

Beside an external file containing the input data, PyGMT allows for different
input types:

- a 1-D (single event) and 2-D array (multiple events)
- a dictionary
- a pandas DataFrame

Different conventions are supported:
TODO - input file and array, this only is for dictionary and DataFrame

- ``"aki"`` - Aki & Richards:
  *strike*, *dip*, *rake*, *magnitude*
- ``"gcmt"`` - global CMT:
  *strike1*, *dip1*, *rake1*, *strike2*, *dip2*, *rake2*, *mantissa*,
  *exponent*
- ``"mt"`` - seismic moment tensor:
  *mrr*, *mtt*, *mff*, *mrt*, *mrf*, *mtf*, *exponent*
- ``"partial"`` - partial focal mechanism:
  *strike1*, *dip1*, *strike2*, *fault_type*, *magnitude*
- ``"principal_axis"`` - principal axis:
  *t_value*, *t_azimuth*, *t_plunge*, *n_value*, *n_azimuth*, *n_plunge*,
  *p_value*, *p_azimuth*, *p_plunge*, *exponent*

The general structure for the input data is:

-  xxx

Please refer also the documentation on how to set up the input data in respect
to the chosen input type and convention.

This tutorial shows how to adjust the display of the beachballs:

- Adjust the outline
- Fill quadrants with colors and patterns
- Highlight the nodal planes
- Offset from event location
- Size-coding and color-coding
- Add a label
"""

# %%
# Import the required packages
import pygmt

# %%
# Set up input data
# -----------------
#
# TODO - consistent with lists in introduction

# Store focal mechanism parameters
# in a 1-D array
fm_sinlge = "xxx"
# in a pandas DataFrame
fm_single = "xxx"
# in a dictionary based on the Aki & Richards convention
fm_single = {"strike": 318, "dip": 89, "rake": -179, "magnitude": 7.75}

# Define the study area: lon_min, lon_max, lat_min, lat_max
# in degrees East or North
study_area = [30, 40, 30, 40]


# %%
# Plot a single beachball
# -----------------------
#
# Required parameters are ``spec``, ``scale``, ``longitude`` and ``latitude``
# (event location)

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=True)

# Plot a single focal mechanism as beachball
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=37.042,  # event longitude
    latitude=37.166,  # event latitude
)

fig.show()


# %%
# Adjust the outline
# ------------------
#
# parameters ``pen`` and ``outline``

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "WSne"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    # Use a 1.5-point thick, red and solid outline
    pen="1.5p,red,solid",
)

# Shift plot origin by the width of the last plot plus 1 centimeter to the right
fig.shift_origin(xshift="+w+1c")

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "wSnE"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    outline="1.5p,red,solid",
)

fig.show()


# %%
# Fill quadrants with colors and patterns
# ---------------------------------------
#
# parameters ``compressionfill`` and ``extensionfill``

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "WSne"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=37.042,
    latitude=37.166,
    compressionfill="darkred",
    extensionfill="gold",
)

fig.shift_origin(xshift="+w+1c")

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "wSnE"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    compressionfill="p8",
    extensionfill="p31",
    outline=True,
)

fig.show()


# %%
# Highlight the nodal planes
# --------------------------
#
# parameter ``nodal``
# Use stacking concept of GMT - plot on top of each other

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "WSne"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=37.042,
    latitude=37.166,
    nodal="0/1p,black,solid",
)

fig.shift_origin(xshift="+w+1c")

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "wSnE"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    compressionfill="lightred",
    outline="1p,red,solid",
)

fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    nodal="1/1p,black,solid",
)

fig.show()


# %%
# Offset from event location
# --------------------------
#
# Parameters ``plot_longitude`` and ``plot_latitude`` as well as ``offset``

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "WSne"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=37.042,
    latitude=37.166,
    plot_longitude=35,
    plot_latitude=38,
    offset=True,
)

fig.shift_origin(xshift="+w+1c")

fig.coast(region=study_area, projection="M10c", land="lightgray", frame=["af", "wSnE"])

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=37.042,
    latitude=37.166,
    plot_longitude=35,
    plot_latitude=38,
    offset="+p1p,red+s0.25c",
    compressionfill="lightred",
)

fig.show()


# %%
# Plot several beachballs
# -----------------------
#
# TODO
# Set up list of four earthquakes:

# - Haiti on 2010/01/12
# - Esmeraldas on 2022/03/27
# - Afghanistan on 2022/06/21
# - Syria / Turkey on 2023/02/06

fm_collection = {
    "strike": [166, 166, 166, 166],
    "dip": [80, 80, 80, 80],
    "rake": [74, 74, 74, 74],
    "magnitude": [7.0, 5.8, 6.0, 7.8],
    "longitude": [-72.53, -79.611, 69.46, 37.032],
    "latitude": [18.46, 0.904, 33.02, 37.166],
    "depth": [13, 26.52, 4, 10],
}

# fixed size via ``scale`` append **+m**

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region="d", projection="N10c", land="lightgray", frame=True)

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c+m",  # in centimeters
)

fig.show()


# %%
# Size-coding and color-coding
# ----------------------------
#
# e.g., by magnitude or hypocentral depth
# Set up colormap and use parameter ``cmap``

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region="d", projection="N10c", land="lightgray", frame=True)

# Set up colormap for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 30, 1])

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c",
    cmap=True,
    outline=True,
)

# Add colorbar
fig.colorbar(frame=["x+lhypocentral depth", "y+lkm"])

fig.show()


# %%
# Add a label
# -----------
#
# ``event_name`` as parameter or as column
# ``labelbox``
# e.g., event date or time
#
# change font size of trailing text ``scale`` **+f**

# Create a new Figure instance
fig = pygmt.Figure()

fig.coast(region="d", projection="N10c", land="lightgray", frame=True)

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c+m+f5p",
    # TODO double check dates
    event_name=["2010/01/12", "2022/03/27", "2022/06/21", "2023/02/06"],
    labelbox="white@30",
)

fig.show()

# sphinx_gallery_thumbnail_number = 7
