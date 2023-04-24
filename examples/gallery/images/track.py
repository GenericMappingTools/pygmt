r"""
Cross-section along a transect
==============================
:func:`pygmt.project` and :func:`pygmt.grdtrack` can be used to estimate
a quantity along a track.
In this example, the elevation is extracted from a gird provided via
:func:`pygmt.datasets.load_earth_relief`.

*The example is orientated on
https://docs.gmt-china.org/latest/examples/ex026/.*
TODO
"""

import pygmt

region_map = [122, 149, 30, 49]

fig = pygmt.Figure()

# ----------------------------------------------------------------------------
# Bottom: Map

fig.basemap(
    region=region_map,
    projection="M12c",
    frame="af",
)

grid_map = pygmt.datasets.load_earth_relief(
    resolution="10m",
    region=region_map,
)

fig.grdimage(grid=grid_map, cmap="oleron")

fig.plot(
    x=[126, 146],
    y=[42, 40],
    pen="2p,red,--",
)

fig.text(
    x=[126, 146],
    y=[42, 40],
    text=["A", "B"],
    offset="0c/0.2c",
    font="15p",
)

fig.colorbar(
    position="jBR+o0.7c/0.8c+h+w5c/0.3c+ml",
    box="+gwhite@30+p0.8p,black",
    frame=["x+lElevation", "y+lm"],
)

# ----------------------------------------------------------------------------
# Top: Profil

fig.shift_origin(yshift="12.5c")

fig.basemap(
    region=[0, 15, -8000, 6000],
    projection="X12/3c",
    frame=["WSrt", "xa2f1+lDistance+u@.", "ya4000+lElevation / m"],
)

fig.text(
    x=[0, 15],
    y=[7000, 7000],
    text=["A", "B"],
    no_clip=True,
    font="10p",
)

track_df = pygmt.project(
    center="126/42",
    endpoint="146/40",
    generate="0.1",
)

grid_track = pygmt.datasets.load_earth_relief(
    resolution="04m",
    region=region_map,
)

track_df = pygmt.grdtrack(
    grid=grid_track,
    points=track_df,
    newcolname="elevation",
)

fig.plot(
    x=[0, 15],
    y=[0, 0],
    fill="lightblue",
    pen="0.25p,black,solid",
    close="+y-8000",
)

fig.plot(
    data=track_df,
    fill="gray",
    pen="1p,black,solid",
    close="+y-8000",
    incols=[2, 3],
)

fig.show()
