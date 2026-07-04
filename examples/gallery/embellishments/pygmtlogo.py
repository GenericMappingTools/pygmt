"""
PyGMT logo
==========
Beside the GMT logo, there is a separate PyGMT logo which can be plotted and added to a
figure using :meth:`pygmt.Figure.pygmtlogo`. The design of the logo itself is kindly
provided by `@sfrooti <https://github.com/sfrooti>`_ and consists of a visual and the
wordmark "PyGMT".

The PyGMT logo is available in circle and hexagon shapes. It can be plotted using colors
of Python (blue and yellow) and GMT (red) or in black and white as well as in light or
dark mode. The wordmark can be added on the right side or at the bottom of the visual.
"""

# %%
import pygmt

# %%
# Plot the PyGMT logo without any arguments:

fig = pygmt.Figure()
fig.pygmtlogo()
fig.show()


# %%
# Via the ``color``, ``theme``, ``shape`` parameters the appereance of the logo can be
# changed:

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/10c", frame=True)

fig.pygmtlogo(color=False, position="TL")

fig.pygmtlogo(theme="dark", position="TR")

fig.pygmtlogo(color=False, theme="dark", position="BL")

fig.pygmtlogo(shape="hexagon", position="BR")

fig.show()


# %%
# Via the ``wordamrk`` parameter the text "PyGMT" can be added on the right side
# or at the bottom of the visual:

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/10c", frame=True)

fig.pygmtlogo(wordmark="horizontal", position="ML")

fig.pygmtlogo(wordmark="vertical", position="MR")

fig.show()


# sphinx_gallery_thumbnail_number = 1
