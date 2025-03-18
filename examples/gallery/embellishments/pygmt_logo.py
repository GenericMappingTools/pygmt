"""
PyGMT logo
==========
The PyGMT logo coded in Python using PyGMT. The design of the logo is kindly provided
by `@sfrooti <https://github.com/sfrooti>`_. The logo consists of a visual and the
wordmark "PyGMT".
"""

import pygmt

fig = pygmt.Figure()
fig.pygmtlogo()
fig.show()

# %%

fig = pygmt.Figure()
fig.pygmtlogo(darkmode=False)
fig.show()

# %%

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=[1, "+gtan"])

fig.logo()  # GMT logo

fig.pygmtlogo()
fig.pygmtlogo(darkmode=False, hexshape=True, position="jTL+o0.1c+w4c", box=False)
fig.pygmtlogo(darkmode=False, position="jTC+o0c/2c+w5c", box="+p1p,black")

fig.pygmtlogo(
    blackwhite=True,
    darkmode=False,
    wordmark=False,
    position="jTL+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(
    blackwhite=True,
    hexshape=True,
    wordmark=False,
    position="jTR+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(blackwhite=True, orientation="vertical", position="jMC+w2c")

fig.show()

# sphinx_gallery_thumbnail_number = 3
