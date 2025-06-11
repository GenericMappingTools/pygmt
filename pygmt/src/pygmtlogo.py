"""
pygmtlogo - Create and plot the PyGMT logo.
The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
and consists of a visual and the wordmark "PyGMT".
"""

from pathlib import Path

import pygmt


def create_logo(color=True, theme="light", shape="circle", wordmark=True):  # noqa: PLR0915
    """
    Create the PyGMT logo using PyGMT.
    The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
    and consists of a visual and the wordmark "PyGMT".

    Parameters
    ----------

    color : bool
        Set to ``True`` to use colors referring to Python (blue and yellow) and GMT
        (red) [Default]. For ``False``, the logo is drawn in black and white.
    theme : str
        Use ``"light"`` for light mode (i.e., white background) [Default] and ``"dark"``
        for dark mode (i.e., darkgray [gray20] background).
    shape : str
        Shape of the visual. Use ``"circle"`` for a circle shape [Default] or
        ``"hexagon"`` for a hexagon shape.
    wordmark : bool, str
        Add the wordmark "PyGMT" and adjust its orientation relative to the visual.
        Set to ``True`` or ``"horizontal"``, to add the wordmark at the right side of
        the visual [Default]. Use ``"vertical"`` to place the wordmark below the
        visual and ``False`` to add no wordmark.
    """

    # -----------------------------------------------------------------------------
    # Helpful definitions
    # -----------------------------------------------------------------------------
    size = 4
    region = [-size, size] * 2
    projection = "x1c"

    # Outer and inner radii of compass lines
    r1, r2 = size * 0.625, size * 0.325

    # Rotation around z (vertical) axis placed in the center
    # Has to be applied to each plotting command, up on second call set to True
    perspective = "30+w0/0"  # Rotation by 30 degrees

    # -----------------------------------------------------------------------------
    # Define colors
    # -----------------------------------------------------------------------------
    color_light = "white"
    color_dark = "gray20"

    # visual
    color_blue = "48/105/152"  # Python blue
    color_yellow = "255/212/59"  # Python yellow
    color_red = "238/86/52"  # GMT red
    if not color:
        color_blue = color_yellow = color_red = color_dark
        if theme == "dark":
            color_blue = color_yellow = color_red = color_light

    # background and wordmark
    match theme:
        case "light":
            color_bg = color_light
            color_py = color_blue
            color_gmt = color_dark
        case "dark":
            color_bg = color_dark
            color_py = color_yellow
            color_gmt = color_light

    # -----------------------------------------------------------------------------
    # Define shape
    # -----------------------------------------------------------------------------
    match shape:
        case "circle":
            symbol = "c"  # circle
            diameter = 7.5
            diameter_add = 0.5
        case "hexagon":
            symbol = "h"  # hexagon
            diameter = 8.6
            diameter_add = 0.6

    # -----------------------------------------------------------------------------
    # Define wordmark
    # -----------------------------------------------------------------------------
    font = "AvantGarde-Book"
    match wordmark:
        case "vertical":
            args_text_wm = {
                "x": 0,
                "y": -5,
                "justify": "CT",
                "font": f"2.5c,{font}",
            }
        case True | "horizontal":
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

    # .............................................................................
    # blue circle / hexagon for Earth
    # .............................................................................
    fig.plot(
        x=0,
        y=0,
        region=region,
        projection=projection,
        style=f"{symbol}{diameter}c",
        pen=f"0.5c,{color_blue}",
        fill=color_bg,
        perspective=perspective,
        no_clip=True,  # needed for corners of hexagon shape
    )

    # .............................................................................
    # yellow lines for compass
    # .............................................................................
    lines_yellow = [
        ([-size, size], [0, 0]),  # horizontal line
        ([-r1, -r2], [r1, r2]),  # upper left
        ([-r1, -r2], [-r1, -r2]),  # lower left
        ([r1, r2], [r1, r2]),  # upper right
        ([r1, r2], [-r1, -r2]),  # lower right
    ]
    for x, y in lines_yellow:
        fig.plot(x=x, y=y, pen=f"5p,{color_yellow}", perspective=True)

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

    # polygon with small distance to horizontal line of letter G
    # starting point: lower right corner of the left vertical line of letter M
    # direction: clockwise
    m_x1 = 0.33 - 0.33 / 2 - 0.06
    m_x2 = 1.54 + 0.33 / 2 - 0.06  # outer radius of letter G
    m_x = [
        m_x1 + m_x2 / 5,  # vertical left upwarts
        m_x1,
        m_x1,
        m_x1 + m_x2 / 5,
        m_x1 + (m_x2 - m_x1) / 2,  # mid pick above
        m_x2 - m_x2 / 5,  # vertical right downwarts
        m_x2,
        m_x2,
        m_x2 - m_x2 / 5,
        m_x2 - m_x2 / 5,  # right pick below
        m_x1 + (m_x2 - m_x1) / 2,  # mid pick below
        m_x1 + m_x2 / 5,  # left pick below
    ]
    m_y1 = 0.3
    m_y2 = 1.65  # outer radius of letter G
    m_y = [
        m_y1,  # vertical left upwarts
        m_y1,
        m_y2,
        m_y2,
        m_y2 - m_y2 / 4,  # mid pick above
        m_y2,  # vertical right downwarts
        m_y2,
        m_y1,
        m_y1,
        m_y2 - m_y2 / 3,  # right pick below
        m_y2 - m_y2 / 2 - m_y2 / 18,  # mid pick below
        m_y2 - m_y2 / 3,  # left pick below
    ]
    fig.plot(x=m_x, y=m_y, close=True, fill=color_red)

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

    # outline around the shape for black and white color with dark theme
    if not color and theme == "dark":
        fig.plot(
            x=0,
            y=0,
            style=f"{symbol}{diameter + diameter_add}c",
            pen=f"1p,{color_dark}",
            perspective=True,
            no_clip=True,
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
    color=True,
    theme="light",
    shape="circle",
    wordmark=True,
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
    """

    # -----------------------------------------------------------------------------
    # Create logo file
    # -----------------------------------------------------------------------------
    fig_name_logo, color_bg = create_logo(
        color=color, theme=theme, shape=shape, wordmark=wordmark
    )

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
