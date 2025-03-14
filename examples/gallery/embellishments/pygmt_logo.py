"""
PyGMT logo
==========
The PyGMT logo coded in Python using PyGMT. The design of the logo is kindly provided
by `@sfrooti <https://github.com/sfrooti>`_. The logo consists of a visual and the
wordmark "PyGMT". There are different versions available:

- ``color_concept``: colors of the visual and workmark.
  Select between ``"colors"`` (colors for Python (blue and yellow) and GMT (red)) and
  ``"bw"`` for black and white.
  [Default is ``"color"``].
- ``bg_concept``: color of the background.
  Select between ``"light"`` (white) and ``"dark"`` (darkgray / gray20).
  [Default is ``"dark"``].
- ``shape``: shape of the visual.
  Select between ``"circle"`` and ``"hexagon"``.
  [Default is ``"circle"``].
- ``wordmark``: add the wordmark "PyGMT".
  ``True`` or ``False``.
  [Default is ``True``].
- ``orientation``: orientation of the wordmark.
  Select between ``"vertical"`` (at the bottom) and ``"horizontal"`` (at the right).
  [Default is ``"vertical"``].
- ``bg_transparent``: make visual transparent outside of the circle or hexagon.
  ``True`` or ``False``.
  Only available for PNG format. Not supported for adding a wordmark.
  [Default is ``False``].
"""

# %%
from pathlib import Path

import pygmt


def pygmtlogo(
    color_concept="color",  # "color" | "bw"
    bg_concept="dark",  # "light" | "dark"
    shape="circle",  # "circle" | "hexagon"
    wordmark=True,  # True | False
    orientation="horizontal",  # "horizontal" | "vertical"
    bg_transparent=False,  # True | False
    position="jRT+o0.1c+w4c",  # -> use position parameter of Figure.image
    box=False,  # True | False  # -> use box parameter of Figure.image
):
    """
    Docstrings
    """

    # -----------------------------------------------------------------------------
    # Define colors (-> can be discussed)
    # -----------------------------------------------------------------------------
    if color_concept == "color":
        color_blue = "48/105/152"  # Python blue
        color_yellow = "255/212/59"  # Python yellow
        color_red = "238/86/52"  # GMT red
    elif color_concept == "bw" and bg_concept == "light":
        color_blue = color_yellow = color_red = "gray20"
    elif color_concept == "bw" and bg_concept == "dark":
        color_blue = color_yellow = color_red = "white"

    match bg_concept:
        case "light":
            color_bg = "white"
            color_py = color_blue
            color_gmt = "gray20"
        case "dark":
            color_bg = "gray20"
            color_py = color_yellow
            color_gmt = "white"

    # Start of subfunction

    def create_logo(
        color_concept=color_concept,
        bg_concept=bg_concept,
        shape=shape,
        wordmark=wordmark,
        orientation=orientation,
        bg_transparent=bg_transparent,
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
        match shape:
            case "circle":
                diameter = 7.5
                diameter_add = 0.5
                symbol = "c"
                margin = -1.2
            case "hexagon":
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

        # margin around shape with slight overplotting for clean borders
        color_margin = color_bg
        if (color_concept == "color" and bg_transparent and not wordmark) or (
            color_concept == "bw"
            and bg_transparent
            and not wordmark
            and bg_concept == "light"
        ):
            color_margin = "white@100"
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
        fig_name = f"pygmt_logo_{shape}_{color_concept}_{bg_concept}"
        fig.savefig(fname=f"{fig_name}.eps")
        # print(fig_name)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Replot and apply rotation
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        fig = pygmt.Figure()
        pygmt.config(MAP_FRAME_PEN="cyan@100")

        bg_alpha = 100 if bg_transparent is True else 0
        fig.basemap(
            region=region,
            projection=f"X{(size + 0.3) * 2}c",
            frame=f"+g{color_bg}@{bg_alpha}",
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
                    args_cover = {"x": -2.2, "y": -2.8}
                case "horizontal":
                    projection = f"X{size * 2}c/{size - 2}c"
                    position = f"jLM+o0.2c/0c+w{size - 2.3}c"
                    args_text = {"x": -1.7, "y": 0, "justify": "LM"}
                    args_cover = {"x": -0.8, "y": 0}

            fig = pygmt.Figure()
            pygmt.config(MAP_FRAME_PEN="cyan@100")
            fig.basemap(region=region, projection=projection, frame=f"+g{color_bg}")

            fig.image(imagefile=f"{fig_name_rot}.eps", position=position)

            fig.text(text="PyGMT", font=f"45p,AvantGarde-Book,{color_gmt}", **args_text)
            fig.plot(style="s2.6c", fill=color_bg, **args_cover)
            fig.text(text="Py", font=f"45p,AvantGarde-Book,{color_py}", **args_text)

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

    # Use parameters of Figure.image
    fig.image(imagefile=f"{fig_name_logo}.eps", position=position, box=box)

    Path.unlink(f"{fig_name_logo}.eps")


# %%
# Plot logo in an existing PyGMT Figure instance
#
# Limitations: works only for a PyGMT Figure instance named "fig"


fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame="+gcyan@100")

pygmtlogo(bg_concept="dark", position="jMC+w10c", wordmark=False, bg_transparent=True)

fig.show()

# %%

fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/2c", frame="+gcyan@100")

pygmtlogo(bg_concept="light", position="jMC+w10c")

fig.show()

# %%

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c", frame=[1, "+gtan"])

pygmtlogo()
pygmtlogo(bg_concept="light", shape="hexagon", position="jTL+o0.1c+w4c")

pygmtlogo(shape="circle", wordmark=False, position="jML+w2c", box=True)
pygmtlogo(
    bg_concept="light",
    wordmark=False,
    bg_transparent=True,
    position="jBL+w2c",
    box=True,
)
pygmtlogo(
    color_concept="bw",
    orientation="vertical",
    bg_transparent=True,
    position="jMC+w2c",
    box="+p1p,blue+gcyan",
)
pygmtlogo(
    color_concept="bw",
    shape="hexagon",
    orientation="vertical",
    position="jBC+w2c",
    box="+ggray20",
)
pygmtlogo(shape="hexagon", wordmark=False, position="jMR+w2c")
pygmtlogo(bg_concept="light", shape="hexagon", wordmark=False, position="jBR+w2c")

pygmtlogo(
    color_concept="bw",
    bg_concept="light",
    wordmark=False,
    bg_transparent=True,
    position="jTL+o0c/1.5c+w2c",
)
pygmtlogo(
    color_concept="bw",
    shape="hexagon",
    wordmark=False,
    bg_transparent=True,
    position="jTR+o0c/1.5c+w2c",
)

fig.show()
