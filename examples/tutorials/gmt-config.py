"""
Configuring PyGMT defaults
==========================

Default GMT parameters can be set globally or locally using :class:`pygmt.config`
"""

import pygmt

########################################################################################
# Configuring default GMT parameters
# ----------------------------------
#
# The user can override default parameters either temporarily (locally) or permanently
# (globally) using :meth:`pygmt.config`. The full list of default parameters that can be
# changed can be at :gmt-docs:`gmt.conf.html`.
#
# We demonstrate the usage of :meth:`pygmt.config` by configuring a map plot.

# Start with a basic figure
fig = pygmt.Figure()
fig.basemap(region=[115, 119.5, 4, 7.5], projection="M10c", frame=True)
fig.coast(land="black", water="skyblue")

fig.show()

########################################################################################
# Globally overriding defaults
# ----------------------------
#
# The ``MAP_FRAME_TYPE`` parameter specifies the style of map frame to use, of which there
# are 3 options: ``fancy`` (default, seen above), ``plain``, and ``inside``.
#
# The ``FORMAT_GEO_MAP`` parameter controls the format of geographical tick annotations.
# The default uses degrees and minutes. Here we specify the ticks to be a decimal number
# of degrees.

pygmt.config(MAP_FRAME_TYPE="plain")
pygmt.config(FORMAT_GEO_MAP="ddd.xx")

fig = pygmt.Figure()
fig.basemap(region=[115, 119.5, 4, 7.5], projection="M10c", frame=True)
fig.coast(land="black", water="skyblue")

fig.show()

########################################################################################
# Locally overriding defaults
# ---------------------------
#
# It is also possible to temporarily override the default parameters, which is a very
# useful for limiting the scope of changes to a particular plot. :class:`pygmt.config` is
# implemented as a context manager, which handles the setup and teardown of a GMT
# session. Python users are likely familiar with the `with open(...) as file:` snippet,
# which returns a `file` context manager. An application of `pygmt.config` as a context
# manager is shown below:

# This will have a fancy frame
with pygmt.config(MAP_FRAME_TYPE="fancy"):
    fig = pygmt.Figure()
    fig.basemap(region=[115, 119.5, 4, 7.5], projection="M10c", frame=True)
    fig.coast(land="black", water="skyblue")

# This figure retains the globally set plain frame
fig.basemap(region=[115, 119.5, 4, 7.5], projection="M10c", Y="-10c", frame=True)
fig.coast(land="black", water="skyblue")

fig.show()
