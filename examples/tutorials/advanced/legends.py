"""
Creating legends
================

The :meth:`pygmt.Figure.legend` method creates legends, whereby auto-legends as well
as manually created legends are supported.
"""

# %%
import io

import pygmt

# %%
# Create an auto-legend
# ---------------------
#
# For auto-legends, the ``label`` parameter of :meth:`pygmt.Figure.plot` has to be
# specified to state the desired text in the legend entry (white spaces are allowed).
# Optionally, to adjust the legend, users can append different modifiers to the string
# passed to ``label``. A list of all available modifiers can be found at
# :gmt-docs:`gmt.html#l-full`. To create a
# :doc:`multiple-column legend </gallery/embellishments/legend>` **+N** is used with
# the desired number of columns. By default, the legend is placed in the Upper Right
# corner with an offset of 0.1 centimeters in both x and y directions and a box with
# a white fill and a 1-point thick, black, solid outline is drawn around the legend.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.plot(x=0, y=0, style="c0.25c", fill="orange", label="orange circle")
fig.legend()

fig.show()


# %%
# Adjust the position
# -------------------
# Use the ``position`` parameter to adjust the position of the legend. For the
# different ways to specify the placement of a plotting element (e.g., legends,
# colorbars) on a plot in GMT, please refer to the Technical Reference TODO (: .
# Add an offset via **+o** for the x and y directions. Additionally append **+w**
# to adjust the ``width`` of the length. Note, no box is drawn by default if
# ``position`` is used.

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.plot(x=0, y=0, style="c0.25c", fill="orange", label="orange circle")
fig.legend(position="jLT+o0.3c/0.2c")

fig.show()


# %%
# Add a box
# ---------
# Use the ``box`` parameter for adjusting the box around the legend. Append **+g**
# to fill the legend with a color (or pattern) [Default is a white fill]. The
# outline of the box can be adjusted by appending **+p**. The default of
# ``position`` is preserved.


fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.plot(x=0, y=0, style="c0.25c", fill="orange", label="orange circle")
fig.legend(position="jTL+o0.3c/0.2c", box=True)

fig.shift_origin(xshift="w+1c")
fig.basemap(region=[-5, 5, -5, 5], projection="X5c", frame=True)

fig.plot(x=0, y=0, style="c0.25c", fill="orange", label="orange circle")
fig.legend(position="jTL+o0.3c/0.2c", box="+p2p,cyan+gblue@70")

fig.show()


# %%
# Create a manual legend
# ----------------------
#
# For more complicated legends in GMT, users need to write an ASCII file with
# instructions for the layout of the legend items. In PyGMT it is additionally
# possible to provide this information as an :class:`io.StringIO` object. Both, the
# ASCII file or the :class:`io.StringIO` object are passed to the ``spec`` parameter
# of :meth:`pygmt.Figure.legend`.
#
# The example below is orientated on the upstream GMT example at
# https://docs.generic-mapping-tools.org/dev/legend.html#examples.


# %%
# First, we set up an :class:`io.StringIO` object.

spec_io = io.StringIO(
    """
G -0.1c
H 24p,Times-Roman My Map Legend
D 0.2c 1p
N 2
V 0 1p
S 0.1c c 0.15c p300/12 0.25p 0.3c This circle is hachured
S 0.1c e 0.15c yellow 0.25p 0.3c This ellipse is yellow
S 0.1c w 0.15c green 0.25p 0.3c This wedge is green
S 0.1c f 0.25c blue 0.25p 0.3c This is a fault
S 0.1c - 0.15c - 0.25p,- 0.3c A contour
S 0.1c v 0.25c magenta 0.5p 0.3c This is a vector
S 0.1c i 0.15c cyan 0.25p 0.3c This triangle is boring
D 0.2c 1p
V 0 1p
N 1
M 5 5 600+u+f
G 0.05c
I @SOEST_block4.png 3i CT
G 0.05c
G 0.05c
L 9p,Times-Roman R Smith et al., @%5%J. Geophys. Res., 99@%%, 2000
G 0.1c
T Let us just try some simple text that can go on a few lines.
T There is no easy way to predetermine how many lines may be required
T so we may have to adjust the height to get the right size box.
"""
)

# %%
# Now, we can add a legend based on this :class:`io.StringIO` object. For
# multi- columns legends, width (**+w**) has to be specified via a the
# ``position`` parameter.

fig = pygmt.Figure()
# Note, that we are now using a Mercator projection
fig.basemap(region=[-5, 5, -5, 5], projection="M10c", frame=True)

# Pass the io.StringIO object to the "spec" parameter
fig.legend(spec=spec_io, position="jMC+w9c", box="+p1p,gray50+ggray95")

fig.show()

# sphinx_gallery_thumbnail_number = 4
