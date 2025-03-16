"""
PyGMT logo
==========
The PyGMT logo coded in Python using PyGMT. The design of the logo is kindly provided
by `@sfrooti <https://github.com/sfrooti>`_. The logo consists of a visual and the
wordmark "PyGMT".
"""

import pygmt

fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame="+gcyan@100")

fig.pygmtlogo(position="jMC+w10c", wordmark=False, box=False)

fig.show()

# %%

fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/2c", frame="+gcyan@100")

fig.pygmtlogo(dark_mode=False, position="jMC+w10c")

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

"""
fig.pygmtlogo(wordmark=False, position="jML+w2c", box=True)
fig.pygmtlogo(
    darkmode=False,
    wordmark=False,
    position="jBL+w2c",
    box="+p1p,black",
)
fig.pygmtlogo(
    blackwhite=True,
    orientation="vertical",
    position="jMC+w2c",
    box="+p1p,blue+gcyan",
)
fig.pygmtlogo(
    blackwhite=True,
    hexshape=True,
    orientation="vertical",
    position="jBC+w2c",
    box="+ggray20",
)
fig.pygmtlogo(hexshape=True, wordmark=False, position="jMR+w2c")
fig.pygmtlogo(darkmode=False, hexshape=True, wordmark=False, position="jBR+w2c")
"""

fig.show()
