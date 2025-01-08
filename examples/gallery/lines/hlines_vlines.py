"""
Horizontal and vertical lines
=============================

The :meth:`pygmt.Figure.hlines` and :meth:`pygmt.Figure.vlines`
methods allow to plot horizontal and vertical lines in
Cartesian, Geographic and Polar projections.
"""

# %%
# In Cartesian projections lines are plotted as straight lines.

import pygmt

fig = pygmt.Figure()

fig.basemap(
    region=[0, 10, 0, 10], projection="X10c/10c", frame=["+thlines Cartesian", "af"]
)

# add a red horizontal line at y=9 without specifying x limits
fig.hlines(y=9, pen="1.5p,red3", label="Line 1")
# add a gray dashed horizontal line at y=8 with x limits at 2 and 8
fig.hlines(y=8, xmin=2, xmax=8, pen="1.5p,gray30,-", label="Line 2")
# add two salmon-colored horizontal lines at y=6 and y=7 both with x limits at 3 and 7
fig.hlines(y=[6, 7], xmin=3, xmax=7, pen="1.5p,salmon", label="Lines 3 & 4")
# add two black dotted horizontal lines at y=4 and y=5 both with x limits at 4 and 9
fig.hlines(y=[4, 5], xmin=4, xmax=9, pen="1.5p,black,.", label="Lines 5 & 6")
# add two blue horizontal lines at y=2 and y=3 with different x limits
fig.hlines(
    y=[2, 3], xmin=[0, 1], xmax=[7, 7.5], pen="1.5p,dodgerblue3", label="Lines 7 & 8"
)
fig.legend(position="JBR+jBR+o0.2c", box="+gwhite+p1p")

fig.shift_origin(xshift="w+2c")

fig.basemap(
    region=[0, 10, 0, 10], projection="X10c/10c", frame=["+tvlines Cartesian", "af"]
)
# add a red vertical line at x=1 without specifying y limits
fig.vlines(x=1, pen="1.5p,red3", label="Line 1")
# add a gray dashed vertical line at x=2 with y limits at 2 and 8
fig.vlines(x=2, ymin=2, ymax=8, pen="1.5p,gray30,-", label="Line 2")
# add two salmon-colored vertical lines at x=3 and x=4 both with y limits at 3 and 7
fig.vlines(x=[3, 4], ymin=3, ymax=7, pen="1.5p,salmon", label="Lines 3 & 4")
# add two black dotted vertical lines at x=5 and x=6 both with y limits at 4 and 9
fig.vlines(x=[5, 6], ymin=4, ymax=9, pen="1.5p,black,.", label="Lines 5 & 6")
# add two blue vertical lines at x=7 and x=8 with different y limits
fig.vlines(
    x=[7, 8], ymin=[0, 1], ymax=[7, 7.5], pen="1.5p,dodgerblue3", label="Lines 7 & 8"
)
fig.legend()

fig.show()

# %%
# The same can be done for Geographic projections where horizontal means
# the lines are plotted as parallels along constant latitude and vertical
# lines are plotted as parallels along constant longitude.

fig = pygmt.Figure()

fig.basemap(region="g", projection="R15c", frame=["+thlines Geographic", "af"])
# add a red horizontal line at a latitude of 70°N without specifying longitude limits
fig.hlines(y=70, xmin=0, xmax=360, pen="1.5p,red3", label="Line 1")
# add a blue line at a latitude of 50°N with longitude limits at 20°E and 160°E
fig.hlines(y=50, xmin=20, xmax=160, pen="1.5p,dodgerblue3", label="Line 2")
# add a gray dashed horizontal line at a latitude of 30°S with longitude limits at 60°E
# and 270°E
fig.hlines(y=-30, xmin=60, xmax=270, pen="1.5p,gray30,-", label="Line 3")
fig.legend()

fig.shift_origin(xshift="w+2c")

fig.basemap(region="g", projection="R15c", frame=["+tvlines Geographic", "af"])
# add a red vertical line at a longitude of 70°E without specifying latitude limits
fig.vlines(x=70, ymin=-90, ymax=90, pen="1.5p,red3", label="Line 1")
# add a blue vertical line at a longitude of 120°E with latitude limits at 50°S and 70°N
fig.vlines(x=120, ymin=-50, ymax=70, pen="1.5p,dodgerblue3", label="Line 2")
# add a gray dashed vertical line at a longitude of 230°E with latitude limits at 70°S
# and 80°N
fig.vlines(x=230, ymin=-70, ymax=80, pen="1.5p,gray30,-", label="Line 3")
fig.legend()

fig.show()

# %%
# When using Polar projections horizontal means lines are plotted as
# arcs along a constant radius while vertical lines are plotted as
# straight lines along radius at a specified azimuth.

fig = pygmt.Figure()

fig.basemap(region=[0, 360, 0, 1], projection="P10c", frame=["+thlines Polar", "af"])
# add a red horizontal line along a radius of 0.8 without specifying azimuth limits
fig.hlines(y=0.8, pen="1.5p,red3", label="Line 1")
# add a blue horizontal line along a radius of 0.5 with azimuth limits at 30° and 160°
fig.hlines(y=0.5, xmin=30, xmax=160, pen="1.5p,dodgerblue3", label="Line 2")
# add a gray dashed horizontal line along a radius of 0.25 with azimuth limits at 60°
# and 270°
fig.hlines(y=0.25, xmin=60, xmax=270, pen="1.5p,gray30,-", label="Line 3")
fig.legend()

fig.shift_origin(xshift="w+2c")

fig.basemap(region=[0, 360, 0, 1], projection="P10c", frame=["+tvlines Polar", "af"])
# add a red vertical line along at an azimuth of 120° without specifying radius limits
fig.vlines(x=120, pen="1.5p,red3", label="Line 1")
# add a blue vertical line along at an azimuth of 190° with radius limits at 0.2 and 0.8
fig.vlines(x=190, ymin=0.2, ymax=0.8, pen="1.5p,dodgerblue3", label="Line 2")
# add a gray dashed vertical line along at an azimuth of 320° with radius limits at 0.5
# and 0.9
fig.vlines(x=320, ymin=0.5, ymax=0.9, pen="1.5p,gray30,-", label="Line 3")
fig.legend()

fig.show()
