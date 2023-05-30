"""
Plotting focal mechanisms
=========================
Focal mechanisms can be plotted with the :meth:`pygmt.Figure.meca` method.

Beside an external file containing the input data, PyGMT allows for different
input types:

- 1-D (single event) and 2-D array (multiple events)
- dictionary
- pandas DataFrame

Different conventions are supported:

- Aki & Richards - ``"aki"``:
  *strike*, *dip*, *rake*, *magnitude*
- Global CMT - ``"gcmt"``:
  *strike1*, *dip1*, *rake1*, *strike2*, *dip2*, *rake2*, *mantissa*,
  *exponent*
- Seismic moment tensor - ``"mt"``:
  *mrr*, *mtt*, *mff*, *mrt*, *mrf*, *mtf*, *exponent*
- Partial focal mechanism - ``"partial"``:
  *strike1*, *dip1*, *strike2*, *fault_type*, *magnitude*
- Principal axis - ``"principal_axis"``:
  *t_value*, *t_azimuth*, *t_plunge*, *n_value*, *n_azimuth*, *n_plunge*,
  *p_value*, *p_azimuth*, *p_plunge*, *exponent*

Please refer also the documentation on how to set up the input data in respect
to the chosen input type and convention.

This tutorial shows how to adjust the display of the beachballs:

- Adjust outline
- Fill quadrants with colors and patterns
- Highlight nodal plane
- Offset from event location
- Size-coding and color-coding
- Add label
"""

# sphinx_gallery_thumbnail_number = 6


# Import the required packages
import pygmt

###############################################################################
# Set up input data
# -----------------
#
# Define study area: lon_min, lon_max, lat_min, lat_max
# in degrees Eath or North
study_area = [-84, -76, -4, 4]

# Store focal mechanism parameters in a dictionary based on the Aki & Richards
# convention
fm_single = dict(strike=166, dip=80, rake=74, magnitude=5.8)


###############################################################################
# Plot a single beachball
# -----------------------
# Required parameters are ``spec``, ``scale``, ``longitude`` and ``latitude``
# (event location)

fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=True,
)

# Pass the focal mechanism data through the spec parameter
# additionally scale and event location are required
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,
    latitude=0.904,
)

fig.show()


###############################################################################
# Adjust outline
# --------------
# parameters ``pen`` and **L** -> ``outline``

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",  # Mercator projection with width 10 centimeters
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "WSne"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,  # event longitude
    latitude=0.904,  # event latitude
    pen="1p,blue,solid",
)

# Shift plot origin 11 centimeters to the right
fig.shift_origin(xshift="11c")

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "wSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,
    latitude=0.904,
    L="1p,red,solid",
)

fig.show()


###############################################################################
# Fill quadrants with colors and patterns
# ---------------------------------------
# parameters ``compressionfill`` and ``extensionfill``

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "WSne"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,
    latitude=0.904,
    compressionfill="lightred",
    extensionfill="cornsilk",
)

# Shift plot origin 11 centimeters to the right
fig.shift_origin(xshift="11c")

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "wSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=-79.611,
    latitude=0.904,
    compressionfill="p8",
    extensionfill="p31",
    L=True,
)

fig.show()


###############################################################################
# Highlight nodal planes
# ----------------------
# parameter **T** -> ``nodal``
# Use stacking concept of GMT - plot on top of each other

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "WSne"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,
    latitude=0.904,
    T="0/1p,black,solid",
)

# Shift plot origin 11 centimeters to the right
fig.shift_origin(xshift="11c")

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "wSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=-79.611,
    latitude=0.904,
    compressionfill="darkgray",
    L="1p,red,solid",
)

fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=-79.611,
    latitude=0.904,
    T="1/1p,black,solid",
)

fig.show()


###############################################################################
# Offset from event location
# --------------------------
# Prameters ``plot_longitude`` and ``plot_latitude`` as well as ``offset``

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "WSne"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",  # in centimeters
    longitude=-79.611,
    latitude=0.904,
    plot_longitude=-78,
    plot_latitude=0,
    offset=True,
)

# Shift plot origin 11 centimeters to the right
fig.shift_origin(xshift="11c")

# Create basic map of study area
fig.coast(
    region=study_area,
    projection="M10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.5p,darkgray",
    borders="1/0.5p,darkred",
    frame=["af", "wSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_single,
    scale="1c",
    longitude=-79.611,
    latitude=0.904,
    plot_longitude=-78,
    plot_latitude=0,
    offset="+p1p,red+s0.25c",
    compressionfill="lightred",
)

fig.show()


###############################################################################
# Plot several beachballs
# -----------------------
# TODO
# Set up list of four earthquakes:
# - Haiti on 2010/01/12
# - Esmeraldas on 2022/03/27
# - Afghanistan on 2022/06/21
# - Syria / Turkey on 2023/02/06
fm_collection = dict(
    strike=[166, 166, 166, 166],
    dip=[80, 80, 80, 80],
    rake=[74, 74, 74, 74],
    magnitude=[7.0, 5.8, 6.0, 7.8],
    longitude=[-72.53, -79.611, 69.46, 37.032],
    latitude=[18.46, 0.904, 33.02, 37.166],
    depth=[13, 26.52, 4, 10],
)

# fixed size via ``scale`` append **+m**

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region="d",
    projection="N10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.1p,darkgray",
    frame=["af", "WSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c+m",  # in centimeters
)

fig.show()


###############################################################################
# Size-coding and color-coding
# ----------------------------
# e.g., by magnitude or hypocentral depth
# Set up colormap and use parameter ``cmap``

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region="d",
    projection="N10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.1p,darkgray",
    frame=["af", "WsNE"],
)

# Set up colormap for hypocentral depth
pygmt.makecpt(
    cmap="lajolla",
    series=[0, 30, 1],
)

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c",
    cmap=True,
    L=True,
)

# Add colorbar
fig.colorbar(frame=["x+lhpyocentral depth", "y+lkm"])

fig.show()


###############################################################################
# Add label
# ---------
# ``event_name`` as parameter or as column
# **Fr** -> ``box``
# e.g., event date or time
#
# TODO figure out how to change font size of trailing text -> ``scale``  **+f**

# Create new figure instance
fig = pygmt.Figure()

# Create basic map of study area
fig.coast(
    region="d",
    projection="N10c",
    land="lightgray",
    water="lightblue",
    shorelines="1/0.1p,darkgray",
    frame=["af", "WSnE"],
)

# Plot focal mechanism
fig.meca(
    spec=fm_collection,
    scale="0.3c+m+f5p",  # in centimeters
    # TODO double check dates
    event_name=["2010/01/12", "2022/03/27", "2022/06/21", "2023/02/06"],
    Fr="white@30",
)

fig.show()
