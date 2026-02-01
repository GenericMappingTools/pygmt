"""
Magnetic rose
=============

The method :meth:`pygmt.Figure.magnetic_rose` can be used to add a magnetic rose
to a map or plot. This example shows how such a magnetic rose can be customized.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.basemap(region=[-8, 8, -7, 7], projection="M10c", frame=True)

# Add a magnetic rose.
# By default, it's placed in the lower left corner.
fig.magnetic_rose()

# Add a magnetic rose with several adjustments
with pygmt.config(
    MAP_TICK_PEN_SECONDARY="orange",
    MAP_TICK_PEN_PRIMARY="cyan",
    MAP_DEFAULT_PEN="brown",
    FONT_TITLE="purple",
):
    fig.magnetic_rose(
        declination=14.3,
        # declination_label="14.3 N°E",  # white spaces are not supported
        position="MC",
        width="4.5c",
        labels=["W", "E", "South", "*"],
        outer_pen="1p,red",
        inner_pen="1p,blue",
    )

fig.show()
