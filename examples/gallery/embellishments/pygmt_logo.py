"""
PyGMT logo
==========
Beside the GMT logo, there is a separate PyGMT logo which can be plotted and added
to a figure using :meth:`pygmt.Figure.pygmtlogo`. The design of the logo itself is
kindly provided by `@sfrooti <https://github.com/sfrooti>`_ and consists of a visual
and the wordmark "PyGMT".
The logo is available in circle and hexagon shape. It can be plotted using colors of
Python (blue and yellow) and GMT (red) or in black and white as well as in light or
dark mode. The wordmark can be added at the right side or bottom of the visual.
"""

# %%
import pygmt

# All versions
# modified from
# https://github.com/GenericMappingTools/pygmt/pull/3849#issuecomment-2753372170
# by @seisman
fig = pygmt.Figure()

# Logo without workmark.
fig.basemap(region=[0, 7, 0, 13], projection="x1c", frame=["a1f1g1", "+ggray50"])
for x, y, theme in [(1, 3, "light"), (4, 3, "dark")]:
    for color, shape in [
        (True, "circle"),
        (True, "hexagon"),
        (False, "circle"),
        (False, "hexagon"),
    ]:
        fig.pygmtlogo(
            color=color,
            theme=theme,
            shape=shape,
            wordmark=False,
            position=f"g{x}/{y}+jTL+w2c",
        )
        y += 3  # noqa: PLW2901

fig.shift_origin(xshift=8)

# Logo with vertical wordmark.
fig.basemap(region=[0, 7, 0, 13], projection="x1c", frame=["a1f1g1", "+ggray50"])
for x, y, theme in [(1, 3, "light"), (4, 3, "dark")]:
    for color, shape in [
        (True, "circle"),
        (True, "hexagon"),
        (False, "circle"),
        (False, "hexagon"),
    ]:
        fig.pygmtlogo(
            color=color,
            theme=theme,
            shape=shape,
            wordmark="vertical",
            position=f"g{x}/{y}+jTL+w2c",
        )
        y += 3  # noqa: PLW2901

fig.shift_origin(xshift=8)

# Logo with horizontal wordmark.
fig.basemap(region=[0, 20, 0, 13], projection="x1c", frame=["a1f1g1", "+ggray50"])
for x, y, theme in [(1, 3, "light"), (11, 3, "dark")]:
    for color, shape in [
        (True, "circle"),
        (True, "hexagon"),
        (False, "circle"),
        (False, "hexagon"),
    ]:
        fig.pygmtlogo(
            color=color,
            theme=theme,
            shape=shape,
            wordmark="horizontal",
            position=f"g{x}/{y}+jTL+w0/2c",
        )
        y += 3  # noqa: PLW2901

fig.show(width=1000)


# sphinx_gallery_thumbnail_number = 1
