r"""
Miscellaneous ways to use polar projections
===========================================

Using this projection allows to plot polar coordinate data (e.g. angle
:math:`\theta` and radius *r*).

x inputs are the theta values for a polar plot.
y inputs are the radius values for a polar plot.
The region values are theta-min/theta-max/radius-min/radius-max.

The following options are available:

- **+a**: by default, :math:`\theta` refers to the angle that is equivalent to
  a counterclockwise rotation with respect to the east direction (standard
  definition); **+a** indicates that the input data is rotated clockwise relative
  to the north direction (geographical azimuth angle)

- **+r**\ *offset*: represents the offset of the r axis. This options allows
  you to put the center of the circle not to r=0

- **+t**: sets the angle corresponding to the east direction which is
  equivalent to rotating the entire coordinate axis clockwise; if the **+a** option
  is used, setting the angle corresponding to the north direction is equivalent to
  rotating the entire coordinate axis counterclockwise.

- **+f**: sets ...
- **+z**: use radius instead of depth ?

The lower-case version **p** is similar to **P** but expects a scale instead of
a width.


"""

import pygmt

fig = pygmt.Figure()

pygmt.config(FONT_TITLE="14p,Helvetica,black")

# ============
# The region values are theta-min/theta-max/radius-min/radius-max.
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

fig.text(position="TC", text="projection='P5c+a\+t45'", offset="0/2.0c", no_clip=True)

fig.text(position="TC", text="region=[0, 90, 0, 1]", offset="0/1.5c", no_clip=True)

fig.shift_origin(xshift="8c", yshift="1.3c")

# ============
fig.basemap(
    region=[0, 90, 3480, 6371],
    projection="P5c+a+t45",
    frame=["xa45f", "ya", "WNse+gbisque"],
)

fig.text(position="TC", text="projection='P5c+a\+t45'", offset="0/2.0c", no_clip=True)

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

fig.text(position="TC", text="projection='P5c+a\+t45+z'", offset="0/2.0c", no_clip=True)

fig.text(
    position="TC", text="region=[0, 90, 3480, 6371]", offset="0/1.5c", no_clip=True
)

fig.show()
