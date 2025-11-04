"""
pygmtlogo - Create and plot the PyGMT logo.
The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
and consists of a visual and the wordmark "PyGMT".
"""

from pathlib import Path

import numpy as np
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
        Use ``"light"`` for light mode (i.e., a white background) [Default] and
        ``"dark"`` for dark mode (i.e., a darkgray [gray20] background).
    shape : str
        Shape of the visual. Use ``"circle"`` for a circle shape [Default] or
        ``"hexagon"`` for a hexagon shape.
    wordmark : bool, str
        Add the wordmark "PyGMT" and adjust its orientation relative to the visual. Set
        to ``True`` or ``"horizontal"``, to add the wordmark at the right side of the
        visual [Default]. Use ``"vertical"`` to place the wordmark below the visual
        and ``False`` to add no wordmark.
    """

    # Helpful definitions
    size = 4
    region = [-size, size] * 2
    projection = "x1c"

    # Radii
    r0, r1, r2, r3, r4 = size * np.array([1.0, 0.875, 0.4625, 0.4125, 0.29375])

    # Rotation around z (vertical) axis placed in the center
    # Has to be applied to each plotting command, up on second call set to True
    perspective = "30+w0/0"  # Rotation by 30 degrees

    # Define colors
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

    # Define shape
    match shape:
        case "circle":
            symbol = "c"  # circle
            diameter = 7.5
            diameter_add = 0.5
        case "hexagon":
            symbol = "h"  # hexagon
            diameter = 8.6
            diameter_add = 0.6

    # Define wordmark
    font = "AvantGarde-Book"
    match wordmark:
        case "vertical":
            args_text_wm = {"x": 0, "y": -5, "justify": "CT", "font": f"2.5c,{font}"}
        case True | "horizontal":
            args_text_wm = {"x": 6, "y": 0, "justify": "LM", "font": f"8c,{font}"}

    fig = pygmt.Figure()
    fig.basemap(
        region=region,
        projection=projection,
        perspective=perspective,
        frame="+n",  # Change it to `frame="afg"` for debugging.
    )

    # blue circle / hexagon for Earth
    fig.plot(
        x=0,
        y=0,
        style=f"{symbol}{diameter}c",
        pen=f"0.5c,{color_blue}",
        fill=color_bg,
        perspective=True,
        no_clip=True,  # needed for corners of hexagon shape
    )

    # Compass
    x1, x2 = r1 * 0.7071, r2 * 0.7071  # sqrt(2)/2 = 0.7071
    lines_compass = [
        ([-r0, -r2], [0, 0]),  # horizontal lines
        ([-r4, 0], [0, 0]),
        ([r2, r0], [0, 0]),
        ([0, 0], [-r0, r0]),  # vertical line
        ([-x1, -x2], [x1, x2]),  # upper left
        ([-x1, -x2], [-x1, -x2]),  # lower left
        ([x1, x2], [x1, x2]),  # upper right
        ([x1, x2], [-x1, -x2]),  # lower right
    ]
    for x, y in lines_compass:
        fig.plot(x=x, y=y, pen=f"5p,{color_yellow}", perspective=True)

    # Letter G
    angles = np.deg2rad(np.arange(90, 361, 1.0))
    x = np.concatenate(
        [np.cos(angles) * r3, [r3, 0, 0, r4], np.cos(np.flip(angles)) * r4]
    )
    y = np.concatenate(
        [
            np.sin(angles) * r3,
            [(r3 - r4) / 2.0, (r3 - r4) / 2.0, -(r3 - r4) / 2.0, -(r3 - r4) / 2.0],
            np.sin(np.flip(angles)) * r4,
        ]
    )
    fig.plot(x=x, y=y, fill=color_red, perspective=True)

    # upper vertical red line
    # space between red line and blue circle / hexagon
    fig.plot(x=[0, 0], y=[r0, r2], pen=f"18p,{color_bg}", perspective=True)
    # red line
    fig.plot(x=[0, 0], y=[r0, r2], pen=f"12p,{color_red}", perspective=True)

    # letter M
    # space between letter M and yellow line at the right side
    # fig.plot(x=[1.6, 1.6], y=[1.5, 1.775], pen=f"10p,{color_bg}")
    fig.plot(x=[1.6, 1.6], y=[1.5, 2.0], pen=f"10p,{color_bg}", perspective=True)

    # polygon with small distance to horizontal line of letter G
    # starting point: lower right corner of the left vertical line of letter M
    # direction: clockwise
    m_x1 = 5 / 2.0 / 72 * 2.54  # Half of the pen thickness of compass lines.
    m_x2 = r3
    m_x = [
        m_x1 + m_x2 / 5,  # vertical left upwards
        m_x1,
        m_x1,
        m_x1 + m_x2 / 5,
        m_x1 + (m_x2 - m_x1) / 2,  # mid pick above
        m_x2 - m_x2 / 5,  # vertical right downwards
        m_x2,
        m_x2,
        m_x2 - m_x2 / 5,
        m_x2 - m_x2 / 5,  # right pick below
        m_x1 + (m_x2 - m_x1) / 2,  # mid pick below
        m_x1 + m_x2 / 5,  # left pick below
    ]
    m_y1 = (r3 - r4) / 2.0 * 1.2
    m_y2 = r3
    m_y = [
        m_y1,  # vertical left upwards
        m_y1,
        m_y2,
        m_y2,
        m_y2 - m_y2 / 4,  # mid pick above
        m_y2,  # vertical right downwards
        m_y2,
        m_y1,
        m_y1,
        m_y2 - m_y2 / 3,  # right pick below
        m_y2 - m_y2 / 2 - m_y2 / 18,  # mid pick below
        m_y2 - m_y2 / 3,  # left pick below
    ]
    fig.plot(x=m_x, y=m_y, close=True, fill=color_red, perspective=True)

    # Letter T
    # Red curved horizontal line
    angles = np.deg2rad(np.arange(150, 210, 0.1))
    t_x = np.concatenate(
        [r2 * np.sin(angles), (r2 + (r3 - r4)) * np.sin(np.flip(angles))]
    )
    t_y = np.concatenate(
        [r2 * np.cos(angles), (r2 + (r3 - r4)) * np.cos(np.flip(angles))]
    )
    # Ensure the same X coordinate for the right edge of T and the middle of M.
    mask = np.abs(t_x) <= (m_x1 + (m_x2 - m_x1) / 2.0)
    fig.plot(x=t_x[mask], y=t_y[mask], fill=color_red, perspective=True)
    # The arrow
    fig.plot(
        data=[[0, -r2, 0, -r0 * 1.05]],
        pen=color_bg,
        style=f"v0.8c+s+e+h0+a60+g{color_bg}",
        perspective=True,
    )
    fig.plot(
        data=[[0, -r2, 0, -r0]],
        pen=f"12p,{color_red}",
        style=f"v0.75c+s+e+h0+a60+g{color_red}",
        perspective=True,
    )

    # Extra vertical compass line above letters "G" and "M".
    fig.plot(x=[0, 0], y=[-r4 * 0.9, r2], pen=f"5p,{color_yellow}", perspective=True)

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

    # Add wordmark "PyGMT"
    if wordmark:
        text_wm = f"@;{color_py};Py@;;@;{color_gmt};GMT@;;"
        fig.text(text=text_wm, no_clip=True, **args_text_wm)

    fig_name_logo = "pygmt_logo"
    fig.savefig(fname=f"{fig_name_logo}.eps")

    return fig_name_logo


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
    fig_name_logo = create_logo(
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
