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

# %%
from pathlib import Path

import pygmt


def pygmtlogo(
    black_white=False,
    dark_mode=True,
    hex_shape=False,
    wordmark=True,
    orientation="horizontal",  # "horizontal" | "vertical"
    position="jRT+o0.1c+w4c",  # -> use position parameter of Figure.image
    box=None,  # -> use box parameter of Figure.image
):
    """
    Docstrings
    """

    # -----------------------------------------------------------------------------
    # Define colors (-> can be discussed)
    # -----------------------------------------------------------------------------
    color_dark = "gray20"
    color_light = "white"

    if not black_white:
        color_blue = "48/105/152"  # Python blue
        color_yellow = "255/212/59"  # Python yellow
        color_red = "238/86/52"  # GMT red
    elif black_white:
        color_blue = color_yellow = color_red = color_light
        if not dark_mode:
            color_blue = color_yellow = color_red = color_dark

    match dark_mode:
        case False:
            color_bg = color_light
            color_py = color_blue
            color_gmt = color_dark
        case True:
            color_bg = color_dark
            color_py = color_yellow
            color_gmt = color_light

    if box is None:
        box = f"+g{color_dark}"
        if not dark_mode:
            box = f"+g{color_light}"

    # Start of subfunction

    def create_logo(
        hex_shape=hex_shape,
        wordmark=wordmark,
        orientation=orientation,
    ):
        # -----------------------------------------------------------------------------
        # Not-changebale settings
        # -----------------------------------------------------------------------------
        size = 4
        region = [-size, size] * 2

        xy_yellow_1 = 2.65
        xy_yellow_2 = 1.3

        pen_yellow = f"5p,{color_yellow}"
        pen_red = f"10p,{color_red}"

        angle_rot = 30  # degrees

        # -----------------------------------------------------------------------------
        # Start plotting
        # -----------------------------------------------------------------------------

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Creating the visual
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        fig = pygmt.Figure()
        pygmt.config(MAP_FRAME_PEN="cyan@100")
        fig.basemap(region=region, projection=f"X{size * 2}c", frame="+gcyan@100")

        # .............................................................................
        # blue circle / hexagon for Earth
        # .............................................................................
        match hex_shape:
            case False:
                diameter = 7.5
                diameter_add = 0.5
                symbol = "c"
                margin = -1.2
            case True:
                diameter = 8.6
                diameter_add = 0.6
                symbol = "h"
                margin = -0.5
        fig.plot(
            x=0,
            y=0,
            style=f"{symbol}{diameter}c",
            pen=f"15p,{color_blue}",
            fill=color_bg,
            no_clip=True,
        )

        # .............................................................................
        # yellow lines for compass
        # .............................................................................
        # horizontal yellow line
        fig.plot(x=[-4, 4], y=[0, 0], pen=pen_yellow, no_clip=True)
        # diagonal yellow lines
        # upper left
        fig.plot(
            x=[-xy_yellow_1, -xy_yellow_2], y=[xy_yellow_1, xy_yellow_2], pen=pen_yellow
        )
        # lower right
        fig.plot(
            x=[xy_yellow_2, xy_yellow_1], y=[-xy_yellow_2, -xy_yellow_1], pen=pen_yellow
        )
        # lower left
        fig.plot(
            x=[-xy_yellow_1, -xy_yellow_2],
            y=[-xy_yellow_1, -xy_yellow_2],
            pen=pen_yellow,
        )
        # upper right
        fig.plot(
            x=[xy_yellow_2, xy_yellow_1], y=[xy_yellow_2, xy_yellow_1], pen=pen_yellow
        )

        # .............................................................................
        # letter G
        # .............................................................................
        # horizontal red line
        fig.plot(x=[0.1, 1.65], y=[0, 0], pen=f"12p,{color_red}")
        # red ring sector
        fig.plot(x=0, y=0, style="w3.3c/90/0+i2.35c", fill=color_red)
        # space between yellow lines and ring sector
        fig.plot(x=0, y=0, style="w3.7c/0/360+i3.3c", fill=color_bg)
        # vertical yellow line
        fig.plot(x=[0, 0], y=[-4, 4], pen=f"6p,{color_yellow}")
        # cover yellow line in lower part of the ring sector
        fig.plot(x=0, y=0, style="w3.3c/260/-80+i2.35c", fill=color_red)

        # .............................................................................
        # upper vertical red line
        # .............................................................................
        # space between red line and blue circle / hexagon
        fig.plot(x=[0, 0], y=[4, 3.0], pen=f"18p,{color_bg}")
        # red line
        fig.plot(x=[0, 0], y=[4, 1.9], pen=f"12p,{color_red}")

        # .............................................................................
        # letter M
        # .............................................................................
        # space between letter M and yellow line at the right side
        # fig.plot(x=[1.6, 1.6], y=[1.5, 1.775], pen=f"10p,{color_bg}")
        fig.plot(x=[1.6, 1.6], y=[1.5, 2.0], pen=f"10p,{color_bg}")
        # diagonal lines
        fig.plot(x=[0.33, 0.90], y=[1.527, 1.00], pen=pen_red)
        fig.plot(x=[0.90, 1.43], y=[1.00, 1.527], pen=pen_red)
        # middle pick
        fig.plot(x=0.9, y=0.9, style="d0.3c", fill=color_red)
        # vertical lines with small distance to horizontal line of letter G
        fig.plot(x=[0.285, 0.285], y=[0.30, 1.65], pen=pen_red)
        fig.plot(x=[1.47, 1.47], y=[0.30, 1.65], pen=pen_red)

        # .............................................................................
        # letter T
        # .............................................................................
        # red curved horizontal line
        fig.plot(x=0, y=0, style="w4.6c/240/-60+i3.7c", fill=color_red)
        # vertical endings of curved horizontal line
        fig.plot(x=[-1.05, -1.05], y=[-1.5, -2.5], pen=f"9p,{color_bg}")
        fig.plot(x=[1.05, 1.05], y=[-1.5, -2.5], pen=f"9p,{color_bg}")
        # arrow head as inverse triangle with pen for space to blue circle / hexagon
        fig.plot(x=0, y=-3.55, style="i1.1c", fill=color_red, pen=f"3p,{color_bg}")
        # arrow tail
        fig.plot(x=[0, 0], y=[-2, -3.57], pen=f"12p,{color_red}")

        # margin around shape for black_white in dark_mode
        # Needed ???
        if black_white and dark_mode:
            color_margin = color_dark
            fig.plot(
                x=0,
                y=0,
                style=f"{symbol}{diameter + diameter_add}c",
                pen=f"1p,{color_margin}",
                no_clip=True,
            )

        # .............................................................................
        # Save
        # .............................................................................
        # fig.show()
        fig_name = "pygmt_logo"
        fig.savefig(fname=f"{fig_name}.eps")
        # print(fig_name)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Replot and apply rotation
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        fig = pygmt.Figure()
        pygmt.config(MAP_FRAME_PEN="cyan@100")

        fig.basemap(
            region=region, projection=f"X{(size + 0.3) * 2}c", frame="+gcyan@100"
        )

        fig.image(
            imagefile=f"{fig_name}.eps",
            position=f"jMC+w{size * 2}c",
            # Rotation around z (vertical) axis placed in the center
            perspective=f"{angle_rot}+w0/0",
        )

        # .............................................................................
        # Save
        # .............................................................................
        # fig.show()
        fig_name_rot = fig_name_logo = f"{fig_name}_rot{angle_rot}deg"
        fig.savefig(fname=f"{fig_name_rot}.eps", resize=f"+m{margin}c")
        # print(fig_name_rot)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Replot and add wordmark "PyGMT"
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if wordmark is True:
            match orientation:
                case "vertical":
                    projection = f"X{size * 2 - 1.5}c/{size * 2}c"
                    position = f"jTC+o0c/0.2c+w{size * 2 - 2.3}c"
                    args_text = {"x": -3.2, "y": -2.8, "justify": "LM"}
                case "horizontal":
                    projection = f"X{size * 2}c/{size - 2}c"
                    position = f"jLM+o0.2c/0c+w{size - 2.3}c"
                    args_text = {"x": -1.7, "y": 0, "justify": "LM"}

            fig = pygmt.Figure()
            pygmt.config(MAP_FRAME_PEN="cyan@100")
            fig.basemap(region=region, projection=projection, frame="+gcyan@100")

            fig.image(imagefile=f"{fig_name_rot}.eps", position=position)

            # Try GMT color setting to avoid re / overplotting
            text_wordmark = f"@;{color_py};Py@;;@;{color_gmt};GMT@;;"
            fig.text(text=text_wordmark, font="45p,AvantGarde-Book", **args_text)

            # .........................................................................
            # Save
            # .........................................................................
            fig_name_rot_text = fig_name_logo = f"{fig_name_rot}_wordmark_{orientation}"
            fig.savefig(fname=f"{fig_name_rot_text}.eps")
            # print(fig_name_rot_text)
            Path.unlink(f"{fig_name_rot}.eps")

        # fig.show()
        Path.unlink(f"{fig_name}.eps")

        return fig_name_logo

    # End of subfunction

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Replot and add to existing Figure instance (-> requires Figure instance named fig)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    fig_name_logo = create_logo()

    # Use parameters of pygmt.Figure.image
    fig.image(imagefile=f"{fig_name_logo}.eps", position=position, box=box)

    Path.unlink(f"{fig_name_logo}.eps")


# %%
# Plot logo in an existing PyGMT Figure instance
#
# Limitations: works only for a PyGMT Figure instance named "fig"


fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame="+gcyan@100")

pygmtlogo(position="jMC+w10c", wordmark=False, box=False)

fig.show()

# %%

fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/2c", frame="+gcyan@100")

pygmtlogo(dark_mode=False, position="jMC+w10c")

fig.show()

# %%

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=[1, "+gtan"])

pygmtlogo()
pygmtlogo(dark_mode=False, hex_shape=True, position="jTL+o0.1c+w4c", box=False)
pygmtlogo(position="jTC+o0c/1.5c+w4c", box="+p1p,black")


# """
pygmtlogo(wordmark=False, position="jML+w2c", box=True)
pygmtlogo(
    dark_mode=False,
    wordmark=False,
    position="jBL+w2c",
    box="+p1p,black",
)
pygmtlogo(
    black_white=True,
    orientation="vertical",
    position="jMC+w2c",
    box="+p1p,blue+gcyan",
)
pygmtlogo(
    black_white=True,
    hex_shape=True,
    orientation="vertical",
    position="jBC+w2c",
    box="+ggray20",
)
pygmtlogo(hex_shape=True, wordmark=False, position="jMR+w2c")
pygmtlogo(dark_mode=False, hex_shape=True, wordmark=False, position="jBR+w2c")

pygmtlogo(
    black_white=True,
    dark_mode=False,
    wordmark=False,
    position="jTL+o0c/1.5c+w2c",
    box=False,
)
pygmtlogo(
    black_white=True,
    hex_shape=True,
    wordmark=False,
    position="jTR+o0c/1.5c+w2c",
    box=False,
)

# """

fig.show()
