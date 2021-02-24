"""
Miscellaneous ways to use polar projections
=====
"""

import pygmt

fig = pygmt.Figure()

pygmt.config(FONT_TITLE="14p,Helvetica,black")

# ============
fig.basemap(region=[0, 360, 0, 1], projection="P5c", frame=["xa45f", "+gbisque"])

fig.text(position="TC", text="projection='P5c'", offset="0/2.0c", no_clip=True)

fig.text(position="TC", text="region=[0, 360, 0, 1]", offset="0/1.5c", no_clip=True)

fig.shift_origin(xshift="8c")

# ============
fig.basemap(region=[0, 360, 0, 1], projection="P5c+a", frame=["xa45f", "+gbisque"])

fig.text(position="TC", text="projection='P5c+a'", offset="0/2.0c", no_clip=True)

fig.text(position="TC", text="region=[0, 360, 0, 1]", offset="0/1.5c", no_clip=True)

fig.shift_origin(xshift="8c")

# ============
fig.basemap(
    region=[0, 90, 0, 1], projection="P5c+a", frame=["xa45f", "ya0.2", "WNe+gbisque"]
)

fig.text(position="TC", text="projection='P5c+a'", offset="0/2.0c", no_clip=True)

fig.text(position="TC", text="region=[0, 90, 0, 1]", offset="0/1.5c", no_clip=True)

fig.shift_origin(xshift="-16c", yshift="-7c")

# ============
fig.basemap(
    region=[0, 90, 0, 1],
    projection="P5c+a+t45",
    frame=["xa45f", "ya0.2", "WNe+gbisque"],
)

fig.text(position="TC", text="projection='P5c+a+t45'", offset="0/2.0c", no_clip=True)

fig.text(position="TC", text="region=[0, 90, 0, 1]", offset="0/1.5c", no_clip=True)

fig.shift_origin(xshift="8c", yshift="1.3c")

# ============
fig.basemap(
    region=[0, 90, 3480, 6371],
    projection="P5c+a+t45",
    frame=["xa45f", "ya", "WNse+gbisque"],
)

fig.text(position="TC", text="projection='P5c+a+t45'", offset="0/2.0c", no_clip=True)

fig.text(
    position="TC", text="region=[0, 90, 3480, 6371]", offset="0/1.5c", no_clip=True
)

fig.shift_origin(xshift="8c")

# ============
fig.basemap(
    region=[0, 90, 3480, 6371],
    projection="P5c+a+t45+z",
    frame=["xa45f", "ya", "WNse+gbisque"],
)

fig.text(position="TC", text="projection='P5c+a+t45+z'", offset="0/2.0c", no_clip=True)

fig.text(
    position="TC", text="region=[0, 90, 3480, 6371]", offset="0/1.5c", no_clip=True
)

fig.show()
