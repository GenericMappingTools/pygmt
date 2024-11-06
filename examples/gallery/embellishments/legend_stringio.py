"""
Legend
======

The :meth:`pygmt.Figure.legend` method creates legends, whereby auto-legends as
well as manually created legends are supported
For auto-legends the ``label`` parameter of :meth:`pygmt.Figure.plot` has to be
specified to state the desired text in the legend entery.

Optionally, to adjust the legend, users can append different modifiers. A list
of all available modifiers can be found at :gmt-docs:`gmt.html#l-full`.
To create a multiple-column legend **+N** is used with the desired number of columns;
see also gallery example xyz.

For more complicated legends, users may want to write an ASCII file with
instructions for the layout of the legend items and pass it to the ``spec``
parameter of :meth:`pygmt.Figure.legend`. Beides such an ASCII file PyGMT
allows the provided this information as ``io.StringIO`` object.

The example blow is orientated on the upstream GMT example at
https://docs.generic-mapping-tools.org/dev/legend.html#examples.
"""

# %%
import io

import pygmt

# -----------------------------------------------------------------------------
# Set up io.StringIO object
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

# -----------------------------------------------------------------------------
# Plot legend into a figure
fig = pygmt.Figure()

# Pass io.StringIO object to the spec parameter
fig.legend(spec=spec_io, region=[0, 10] * 2, projection="M10c", position="jMC")

fig.show()
