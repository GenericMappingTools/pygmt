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
fig.pygmtlogo(darkmode=True, box="+ggray20")
fig.show()

# %%

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=[1, "+gtan"])

fig.pygmtlogo(position="jTL+o0.2c+w4c", box="+gwhite+p1p,gray")
fig.pygmtlogo(hexshape=True, position="jTR+o0.2c+w4c")

fig.pygmtlogo(
    blackwhite=True,
    wordmark=False,
    position="jTL+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(
    blackwhite=True,
    darkmode=True,
    hexshape=True,
    wordmark=False,
    position="jTR+o0.5c/2c+w1.5c",
    box=False,
)
fig.pygmtlogo(wordmark="vertical", position="jMC+w2c")

fig.show()

# %%
# All combinations

i_plot = 0

fig = pygmt.Figure()

for blackwhite in [False, True]:
    for darkmode in [False, True]:
        for hexshape in [False, True]:
            for wordmark in [True, False, "horizontal", "vertical"]:
                for box in [False, True]:
                    if not box:
                        box_used = False
                    elif box:
                        if not darkmode:
                            box_used = "+gwhite"
                        elif darkmode:
                            box_used = "+ggray20"
                    # fig = pygmt.Figure()
                    fig.basemap(
                        region=[-1, 1, -1, 1], projection="X2.5c", frame="+gtan"
                    )
                    # fig.image("@needle.png", position="jMC+w2c", box=box_used)
                    fig.pygmtlogo(
                        blackwhite=blackwhite,
                        darkmode=darkmode,
                        hexshape=hexshape,
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

# sphinx_gallery_thumbnail_number = 3
