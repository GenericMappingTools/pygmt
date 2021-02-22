"""
Miscellaneous ways to use polar projections
=====
"""

import pygmt

fig = pygmt.Figure()

pygmt.config(FONT_TITLE="14p,Helvetica,black")

# ============
fig.basemap(region=[0, 360, 0, 1], projection="P5c", frame=["xa45f", "+gbisque"])

fig.text(
    x=[270, 270],
    y=[-1.7, -1.5],
    text=["projection = P5c", "region = [0,360,0,1]"],
    no_clip=True,
)
fig.shift_origin(xshift="8c")

# ============
fig.basemap(region=[0, 360, 0, 1], projection="P5c+a", frame=["xa45f", "+gbisque"])

fig.text(
    x=[0, 0],
    y=[1.7, 1.5],
    text=["projection = P5c+a", "region = [0,360,0,1]"],
    no_clip=True,
)
fig.shift_origin(xshift="8c")

# ============
fig.basemap(
    region=[0, 90, 0, 1], projection="P5c+a", frame=["xa45f", "ya0.2", "WNe+gbisque"]
)

fig.text(
    x=[25, 20],
    y=[1.5, 1.33],
    text=["projection = P5c+a", "region = [0,90,0,1]"],
    no_clip=True,
)
fig.shift_origin(xshift="-16c", yshift="-7c")

# ============
fig.basemap(
    region=[0, 90, 0, 1],
    projection="P5c+a+t45",
    frame=["xa45f", "ya0.2", "WNe+gbisque"],
)

fig.text(
    x=[45, 45],
    y=[1.5, 1.35],
    text=["projection = P5c+a+t45", "region = [0,90,0,1]"],
    no_clip=True,
)
fig.shift_origin(xshift="8c", yshift="1.3c")

# ============
fig.basemap(
    region=[0, 90, 3480, 6371],
    projection="P5c+a+t45",
    frame=["xa45f", "ya", "WNse+gbisque"],
)

fig.text(
    x=[45, 45],
    y=[10000, 9000],
    text=["projection = P5c+a+t45", "region = [0,90,3480,6371]"],
    no_clip=True,
)
fig.shift_origin(xshift="8c")

# ============
fig.basemap(
    region=[0, 90, 3480, 6371],
    projection="P5c+a+t45+z",
    frame=["xa45f", "ya", "WNse+gbisque"],
)

fig.text(
    x=[45, 45],
    y=[10000, 9000],
    text=["projection = P5c+a+t45+z", "region = [0,90,3480,6371]"],
    no_clip=True,
)

fig.show()
