"""
PyGMT logo
==========
The PyGMT logo coded in Python using PyGMT. The design of the logo is kindly provided
by `@sfrooti <https://github.com/sfrooti>`_. The logo consists of a visual and the
wordmark "PyGMT". There are different versions available:

- ``black_white``: draw in black and white.
  ``False`` colors for Python (blue and yellow) and GMT (red) [Default] or ``True``
  for black and white.
- ``dark_mode``: use dark background.
  ``False`` white or ``True`` darkgray / gray20 [Default].
- ``hex_shape``: use hexagon shape.
  ``False`` circle [Default] or ``True`` hexagon.
- ``wordmark``: add the wordmark "PyGMT".
  ``True`` with wordmark [Default] or ``False`` without wordmark.
- ``orientation``: orientation of the wordmark.
  ``"horizontal"`` at the right [Default] or ``"vertical"`` at the bottom.
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
fig.pygmtlogo(dark_mode=False, hex_shape=True, position="jTL+o0.1c+w4c", box=False)
fig.pygmtlogo(dark_mode=False, position="jTC+o0c/2c+w5c", box="+p1p,black")

fig.pygmtlogo(
    black_white=True,
    dark_mode=False,
    wordmark=False,
    position="jTL+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(
    black_white=True,
    hex_shape=True,
    wordmark=False,
    position="jTR+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(black_white=True, orientation="vertical", position="jMC+w2c")

"""
fig.pygmtlogo(wordmark=False, position="jML+w2c", box=True)
fig.pygmtlogo(
    dark_mode=False,
    wordmark=False,
    position="jBL+w2c",
    box="+p1p,black",
)
fig.pygmtlogo(
    black_white=True,
    orientation="vertical",
    position="jMC+w2c",
    box="+p1p,blue+gcyan",
)
fig.pygmtlogo(
    black_white=True,
    hex_shape=True,
    orientation="vertical",
    position="jBC+w2c",
    box="+ggray20",
)
fig.pygmtlogo(hex_shape=True, wordmark=False, position="jMR+w2c")
fig.pygmtlogo(dark_mode=False, hex_shape=True, wordmark=False, position="jBR+w2c")
"""

fig.show()
