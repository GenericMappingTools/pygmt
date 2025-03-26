"""
pygmtlogo - Create and plot the PyGMT logo.
The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_.
"""

from pathlib import Path

import pygmt


def create_logo(  # noqa: PLR0915
    blackwhite=False,
    darkmode=False,
    hexshape=False,
    wordmark=True,
    orientation="horizontal",
):
    """
    Creat the PyGMT logo.
    The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_.

    Parameters
    ----------

    blackwhite : bool
        Draw in black and white. Set to ``True`` for black and white [Default is
        ``False`` and uses colors for Python (blue and yellow) and GMT (red)].
    darkmode : bool
        Use dark mode. Set to``True`` for dark mode [Default is ``False`` for light
        mode].
    hexshape : bool
        Use a hexagon shape. Set to ``True`` for a hexagon shape [Default is `False``
        and uses to a circle shape].
    wordmark : bool, str
        Add the wordmark "PyGMT" and adjust its orientation relative to the visual.
        Set to `True`` or ``"horizontal"``, to add the wordmark at the right side of
        the visual [Default]. Use ``"vertical"`` to place the wordmark below the
        visual and ``False`` to add no wordmark.
    """

    # -----------------------------------------------------------------------------
    # Helpful definitions
    # -----------------------------------------------------------------------------
    size = 4
    region = [-size, size] * 2

    xy_yellow_1 = 2.65
    xy_yellow_2 = 1.3

    no_line = "cyan@100"
    no_fill = f"+g{no_line}"

    # Rotation around z (vertical) axis placed in the center
    # Has to be applied to each plotting command, up on second call set to True
    # Do NOT rotated initial basemap
    angle_rot = 30  # degrees
    perspective = f"{angle_rot}+w0/0"

    # -----------------------------------------------------------------------------
    # Define colors
    # -----------------------------------------------------------------------------
    color_dark = "gray20"
    color_light = "white"

    # visual
    color_blue = "48/105/152"  # Python blue
    color_yellow = "255/212/59"  # Python yellow
    color_red = "238/86/52"  # GMT red
    if blackwhite:
        color_blue = color_yellow = color_red = color_light
        if not darkmode:
            color_blue = color_yellow = color_red = color_dark

    # background and wordmark
    color_bg = color_dark
    color_py = color_yellow
    color_gmt = color_light
    if not darkmode:
        color_bg = color_light
        color_py = color_blue
        color_gmt = color_dark

    # -----------------------------------------------------------------------------
    # Define shape
    # -----------------------------------------------------------------------------
    symbol = "c"  # circle
    diameter = 7.5
    diameter_add = 0.5
    if hexshape:
        symbol = "h"  # hexagon
        diameter = 8.6
        diameter_add = 0.6

    # -----------------------------------------------------------------------------
    # Define wordmark
    # -----------------------------------------------------------------------------
    font = "AvantGarde-Book"
    match orientation:
        case "vertical":
            args_text_wm = {
                "x": 0,
                "y": -5,
                "justify": "CT",
                "font": f"2.5c,{font}",
            }
        case "horizontal":
            args_text_wm = {
                "x": 6,
                "y": 0,
                "justify": "LM",
                "font": f"8c,{font}",
            }

    # -----------------------------------------------------------------------------
    # Start plotting
    # -----------------------------------------------------------------------------
    fig = pygmt.Figure()
    pygmt.config(MAP_FRAME_PEN=no_line)
    fig.basemap(
        region=region,
        projection=f"X{size * 2}c",
        frame=no_fill,
    )

    # .............................................................................
    # blue circle / hexagon for Earth
    # .............................................................................
    fig.plot(
        x=0,
        y=0,
        style=f"{symbol}{diameter}c",
        pen=f"15p,{color_blue}",
        fill=color_bg,
        no_clip=True,
        perspective=perspective,
    )

    # .............................................................................
    # yellow lines for compass
    # .............................................................................
    args_yellow = {"pen": f"5p,{color_yellow}", "perspective": True}
    # horizontal yellow line
    fig.plot(x=[-4, 4], y=[0, 0], no_clip=True, **args_yellow)
    # diagonal yellow lines
    lines_diagonal = [
        ([-xy_yellow_1, -xy_yellow_2], [xy_yellow_1, xy_yellow_2]),  # upper left
        ([xy_yellow_2, xy_yellow_1], [-xy_yellow_2, -xy_yellow_1]),  # lower right
        ([-xy_yellow_1, -xy_yellow_2], [-xy_yellow_1, -xy_yellow_2]),  # lower left
        ([xy_yellow_2, xy_yellow_1], [xy_yellow_2, xy_yellow_1]),  # upper right
    ]
    for x_coords, y_coords in lines_diagonal:
        fig.plot(x=x_coords, y=y_coords, **args_yellow)

    # .............................................................................
    # letter G
    # .............................................................................
    # horizontal red line
    fig.plot(x=[0.1, 1.65], y=[0, 0], pen=f"12p,{color_red}", perspective=True)
    # red ring sector
    fig.plot(x=0, y=0, style="w3.3c/90/0+i2.35c", fill=color_red, perspective=True)
    # space between yellow lines and ring sector
    fig.plot(x=0, y=0, style="w3.7c/0/360+i3.3c", fill=color_bg, perspective=True)
    # vertical yellow line
    fig.plot(x=[0, 0], y=[-4, 4], pen=f"6p,{color_yellow}", perspective=True)
    # cover yellow line in lower part of the ring sector
    fig.plot(x=0, y=0, style="w3.3c/260/-80+i2.35c", fill=color_red, perspective=True)

    # .............................................................................
    # upper vertical red line
    # .............................................................................
    # space between red line and blue circle / hexagon
    fig.plot(x=[0, 0], y=[4, 3.0], pen=f"18p,{color_bg}", perspective=True)
    # red line
    fig.plot(x=[0, 0], y=[4, 1.9], pen=f"12p,{color_red}", perspective=True)

    # .............................................................................
    # letter M
    # .............................................................................
    # space between letter M and yellow line at the right side
    # fig.plot(x=[1.6, 1.6], y=[1.5, 1.775], pen=f"10p,{color_bg}")
    fig.plot(x=[1.6, 1.6], y=[1.5, 2.0], pen=f"10p,{color_bg}", perspective=True)
    # lines with small distance to horizontal line of letter G
    args_m = {"pen": f"10p,{color_red}", "perspective": True}
    lines_m = [
        ([0.33, 0.90], [1.527, 1.00]),  # diagonal left
        ([0.90, 1.43], [1.00, 1.527]),  # diagonal right
        ([0.285, 0.285], [0.30, 1.65]),  # vertical left
        ([1.47, 1.47], [0.30, 1.65]),  # vertical right
    ]
    for x_coords, y_coords in lines_m:
        fig.plot(x=x_coords, y=y_coords, **args_m)
    # middle corner
    fig.plot(x=0.9, y=0.9, style="d0.3c", fill=color_red, perspective=True)

    # .............................................................................
    # letter T
    # .............................................................................
    # red curved horizontal line
    fig.plot(x=0, y=0, style="w4.6c/240/-60+i3.7c", fill=color_red, perspective=True)
    # vertical endings of curved horizontal line
    args_vert = {"y": [-1.5, -2.5], "pen": f"9p,{color_bg}", "perspective": True}
    fig.plot(x=[-1.05, -1.05], **args_vert)
    fig.plot(x=[1.05, 1.05], **args_vert)
    # arrow head as inverse triangle with pen for space to blue circle / hexagon
    fig.plot(
        x=0,
        y=-3.55,
        style="i1.1c",
        fill=color_red,
        pen=f"3p,{color_bg}",
        perspective=True,
    )
    # arrow tail
    fig.plot(x=[0, 0], y=[-2, -3.57], pen=f"12p,{color_red}", perspective=True)

    # margin around shape for blackwhite=True in darkmode=True
    if blackwhite and darkmode:
        fig.plot(
            x=0,
            y=0,
            style=f"{symbol}{diameter + diameter_add}c",
            pen=f"1p,{color_dark}",
            no_clip=True,
            perspective=True,
        )

    # .............................................................................
    # Add wordmark "PyGMT"
    # .............................................................................
    if wordmark:
        text_wm = f"@;{color_py};Py@;;@;{color_gmt};GMT@;;"
        fig.text(text=text_wm, no_clip=True, **args_text_wm)

    # .............................................................................
    # Save
    # .............................................................................
    fig_name_logo = "pygmt_logo"
    fig.savefig(fname=f"{fig_name_logo}.eps")

    return fig_name_logo, color_bg


def pygmtlogo(  # noqa: PLR0913
    self,
    blackwhite=False,
    darkmode=False,
    hexshape=False,
    wordmark=True,
    orientation="horizontal",
    position=None,  # -> use position parameter of Figure.image
    box=None,  # -> use box parameter of Figure.image
    projection=None,
    region=None,
    verbose=None,
    panel=None,
    transparency=None,
):
    """
    Plot the PyGMT logo.
    The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_.
    """

    # -----------------------------------------------------------------------------
    # Create logo file
    # -----------------------------------------------------------------------------
    fig_name_logo, color_bg = create_logo(
        blackwhite=blackwhite,
        darkmode=darkmode,
        hexshape=hexshape,
        wordmark=wordmark,
        orientation=orientation,
    )

    # -----------------------------------------------------------------------------
    # Add box around logo
    # -----------------------------------------------------------------------------
    # if box is None:
    #    box = f"+g{color_bg}"

    # -----------------------------------------------------------------------------
    # Add to existing Figure instance
    # -----------------------------------------------------------------------------
    self.image(
        imagefile=f"{fig_name_logo}.eps",
        position=position,
        box=box,
        projection=projection,
        region=region,
        verbose=verbose,
        panel=panel,
        transparency=transparency,
    )

    Path.unlink(f"{fig_name_logo}.eps")
