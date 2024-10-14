"""
Plotting focal mechanisms
=========================

Focal mechanisms can be plotted as beachballs with the :meth:`pygmt.Figure.meca`
method. The input data can be provided in different ways:

- a string containing path and name of an external file
- a 1-D (single event) or 2-D (multiple events) ``numpy.array``
- a dictionary
- a ``pandas.DataFrame``

Different conventions to define the focal mechanism are supported. For providing
a dictionary or a ``pandas.DataFrame`` the listed keys or column names are required:

- ``"aki"`` - Aki & Richards:
  *strike*, *dip*, *rake*, *magnitude*
- ``"gcmt"`` - global CMT:
  *strike1*, *dip1*, *rake1*, *strike2*, *dip2*, *rake2*, *mantissa*, *exponent*
- ``"mt"`` - seismic moment tensor:
  *mrr*, *mtt*, *mff*, *mrt*, *mrf*, *mtf*, *exponent*
- ``"partial"`` - partial focal mechanism:
  *strike1*, *dip1*, *strike2*, *fault_type*, *magnitude*
- ``"principal_axis"`` - principal axis:
  *t_value*, *t_azimuth*, *t_plunge*, *n_value*, *n_azimuth*, *n_plunge*,
  *p_value*, *p_azimuth*, *p_plunge*, *exponent*

Please also refer also the documentation on how to set up the input data in
respect to the chosen input type and convention.

This tutorial shows how to adjust the display of the beachballs:

- Filling the quadrants
- Adjusting the outlines
- Highlighting the nodal planes
- Adding offset from the event location
- Adding a label
- Using size-coding and color-coding
"""

# %%
import pandas as pd
import pygmt

# %%
# Set up input data
# -----------------
# Store focal mechanism parameters for one event in a dictionary based on the

# moment tensor convention
mt_dict_single = mt_virginia = {
    "mrr": 4.71,
    "mtt": 0.0381,
    "mff": -4.74,
    "mrt": 0.399,
    "mrf": -0.805,
    "mtf": -1.23,
    "exponent": 24,
}
# Aki & Richards convention
aki_dict_single = {"strike": 318, "dip": 89, "rake": -179, "magnitude": 7.75}

# Set up arguments for basemap
size = 5
projection = "X10c/4c"
frame = ["af", "+ggray80"]


# %%
# Plotting a single beachball
# ---------------------------
#
# Required parameters are ``spec``, ``scale``, ``longitude`` and ``latitude``
# (event location). (and ``convention`` depending on the input format, not needed
# for dictionary and ``pandas.Dataframe``.)

fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=projection, frame=frame)

fig.meca(spec=mt_dict_single, scale="1c", longitude=0, latitude=0)

fig.show()


# %%
# Filling the quadrants
# ---------------------
#
# Use the parameters ``compressionfill`` and ``extensionfill`` to fill the
# quadrants with colors or patterns.
# details on pattern gallery example and techenical reference

fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=projection, frame=frame)

fig.meca(
    spec=mt_dict_single,
    scale="1c",
    longitude=-2,
    latitude=0,
    compressionfill="darkorange",
    extensionfill="cornsilk",
)

fig.meca(
    spec=mt_dict_single,
    scale="1c",
    longitude=2,
    latitude=0,
    compressionfill="p8",
    extensionfill="p31",
    outline=True,
)

fig.show()


# %%
# Adjusting the outlines
# ----------------------
#
# Use the parameters ``pen`` for the outer border of the beachball and ``outline``
# for all lines (also the borders between the nodal planes)

fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=projection, frame=frame)

fig.meca(
    spec=mt_dict_single,
    scale="1c",
    longitude=-2,
    latitude=0,
    # Use a 1-point thick, darkorange and solid outline
    pen="1p,darkorange,solid",
)

fig.meca(
    spec=mt_dict_single,
    scale="1c",
    longitude=2,
    latitude=0,
    outline="1p,darkorange,solid",
)

fig.show()


# %%
# Highlighting the nodal planes
# -----------------------------
#
# Use the parameter ``nodal``
# whereby ``"0"`` both, ``"1"`` first, ``"2"`` second
# only lines not fill i.e. transparent
# Make use of the stacking concept of GMT and plot on top of each other
# behaviour somehow strange

fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=projection, frame=frame)

fig.meca(
    spec=aki_dict_single,
    scale="1c",
    longitude=-2,
    latitude=0,
    nodal="0/1p,black,solid",
)

fig.meca(
    spec=aki_dict_single,
    scale="1c",
    longitude=2,
    latitude=0,
    compressionfill="lightorange",
    outline="1p,darkorange,solid",
)
fig.meca(
    spec=aki_dict_single,
    scale="1c",
    longitude=2,
    latitude=0,
    nodal="1/1p,black,solid",
)

fig.show()


# %%
# Adding offset from event location
# ---------------------------------
#
# Specify the optional parameters ``plot_longitude`` and ``plot_latitude``.
# Additional the parameter ``offset`` as to be set. Besides just drawing a line
# between the beachball and the event location, a small circle can be plotted
# at the event location by appending **+s** and the descired circle size. The
# connecting line as well as the outline of the circle are plotted with the
# setting of pen, or can be adjusted separately. The fill of the small circle
# corresponds to the fill for the compressive quadrantes.

fig = pygmt.Figure()
fig.basemap(region=[-size, size] * 2, projection=projection, frame=frame)

fig.meca(
    spec=aki_dict_single,
    scale="1c",
    longitude=-1,
    latitude=0,
    plot_longitude=-3,
    plot_latitude=2,
    offset=True,
)

fig.meca(
    spec=aki_dict_single,
    scale="1c",
    longitude=3,
    latitude=0,
    plot_longitude=1,
    plot_latitude=2,
    offset="+p1p,darkorange+s0.25c",
    compressionfill="lightorange",
)

fig.show()


# %%
# Plotting multiple beachballs
# ----------------------------
#
# Data of four earthquakes taken from USGS.
# Provide lists.

# Set up a dictionary
aki_dict_multiple = {
    "strike": [255, 173, 295, 318],
    "dip": [70, 68, 79, 89],
    "rake": [20, 83, -177, -179],
    "magnitude": [7.0, 5.8, 6.0, 7.8],
    "longitude": [-72.53, -79.61, 69.46, 37.01],
    "latitude": [18.44, 0.90, 33.02, 37.23],
    "depth": [13, 19, 4, 10],
    "plot_longitude": [-70, -110, 100, 0],
    "plot_latitude": [40, 10, 50, 55],
    "event_name": [
        "Haiti - 2010/01/12",
        "Esmeraldas - 2022/03/27",
        "Afghanistan - 2022/06/21",
        "Syria/Turkey - 2023/02/06",
    ],
}
# Convert to a pandas.DataFrame
aki_df_multiple = pd.DataFrame(aki_dict_multiple)


# %%
# Adding a label
# --------------
#
# Use the optional parameter ``event_name`` to add a label above the beachball,
# e.g., event name or event date and time. Change the font size of the the label
# text by appending **+f** and the desired font size to the ``scale`` parameter.
# Add a colored box behind the label via the label ``labelbox``.
# Force a fixed size of the beachball by appending **+m** to the argument
# passed to ``scale``.

fig = pygmt.Figure()
fig.coast(region="d", projection="N10c", land="lightgray", frame=True)

fig.meca(spec=aki_df_multiple, scale="0.4c+m+f5p", labelbox="white@30", offset="+s0.1c")

fig.show()


# %%
# Using size-coding and color-coding
# ----------------------------------
#
# The beachball can be sized and colored by a different quantities, e.g., by
# magnitude or hypocentral depth, respectively. Use the parameter ``cmap`` to
# pass the descired colormap.

fig = pygmt.Figure()
fig.coast(region="d", projection="N10c", land="lightgray", frame=True)

# Set up colormap and colorbar for hypocentral depth
pygmt.makecpt(cmap="lajolla", series=[0, 20])
fig.colorbar(frame=["x+lhypocentral depth", "y+lkm"])

fig.meca(
    spec=aki_df_multiple,
    scale="0.4c+f5p",
    offset="0.2p,gray30+s0.1c",
    labelbox="white@30",
    cmap=True,
    outline="0.2p,gray30",
)

fig.show()

# sphinx_gallery_thumbnail_number = 7
