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

import pygmt

fig = pygmt.Figure()
fig.pygmtlogo()
fig.show()

# %%

fig = pygmt.Figure()
fig.pygmtlogo(theme="dark", box="+ggray20")
fig.show()

# %%

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=[1, "+gtan"])

fig.pygmtlogo(position="jTL+o0.2c+w4c", box="+gwhite+p1p,gray")
fig.pygmtlogo(shape="hexagon", position="jTR+o0.2c+w4c")

fig.pygmtlogo(color=False, wordmark=False, position="jTL+o0.5c/2c+w1.5c", box=False)
fig.pygmtlogo(
    color=False,
    theme="dark",
    shape="hexagon",
    wordmark=False,
    position="jTR+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(wordmark="vertical", position="jMC+w2c", box="+gwhite")

fig.show()

# %%
# All combinations

i_plot = 0

fig = pygmt.Figure()

for color in [True, False]:
    for theme in ["light", "dark"]:
        for shape in ["circle", "hexagon"]:
            for wordmark in [False, True, "horizontal", "vertical"]:
                for box in [False, True]:
                    if not box:
                        box_used = False
                    elif box:
                        if theme == "light":
                            box_used = "+gwhite"
                        elif theme == "dark":
                            box_used = "+ggray20"
                    # fig = pygmt.Figure()
                    fig.basemap(
                        region=[-1, 1, -1, 1], projection="X2.5c/3.5c", frame="+gtan"
                    )
                    # fig.image("@needle.png", position="jMC+w2c", box=box_used)
                    fig.pygmtlogo(
                        color=color,
                        theme=theme,
                        shape=shape,
                        wordmark=wordmark,
                        position="jMC+w2c",
                        box=box_used,
                    )

                    fig.shift_origin(xshift="+w+0.5c")
                    n_hor = 8
                    if i_plot in range(n_hor - 1, 100, n_hor):
                        fig.shift_origin(
                            xshift=f"-{(n_hor * 2.5 + n_hor * 0.5)}c",
                            yshift="-h-0.5c",
                        )  # n_hor*width + n_hor*xshift

                    i_plot = i_plot + 1
fig.show()


# ##
# All versions
# modified from
# https://github.com/GenericMappingTools/pygmt/pull/3849#issuecomment-2753372170
# by @seisman

fig = pygmt.Figure()

# Logo without workmark.
fig.basemap(region=[0, 7, 0, 13], projection="x1c", frame="a1f1g1")
for x, y, theme in [(1, 3, "light"), (4, 3, "dark")]:
    for color, shape in [(True, "circle"), (False, "hexagon")]:
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
fig.basemap(region=[0, 7, 0, 13], projection="x1c", frame="a1f1g1")
for x, y, theme in [(1, 3, "light"), (4, 3, "dark")]:
    for color, shape in [(True, "circle"), (False, "hexagon")]:
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
fig.basemap(region=[0, 20, 0, 13], projection="x1c", frame="a1f1g1")
for x, y, theme in [(1, 3, "light"), (11, 3, "dark")]:
    for color, shape in [(True, "circle"), (False, "hexagon")]:
        fig.pygmtlogo(
            color=color,
            theme=theme,
            shape=shape,
            wordmark="horizontal",
            position=f"g{x}/{y}+jTL+w0/2c",
        )
        y += 3  # noqa: PLW2901

fig.show(width=1000)


# sphinx_gallery_thumbnail_number = 3
