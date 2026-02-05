"""
pygmtlogo - Create and plot the PyGMT logo.
The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
and consists of a visual and the wordmark "PyGMT".
"""

from pathlib import Path
from typing import Literal

import numpy as np
import pygmt


def create_logo(  # noqa: PLR0915
    shape: Literal["circle", "hexagon"] = "circle",
    theme: Literal["light", "dark"] = "light",
    wordmark: Literal["horizontal", "vertical"] | bool = True,
    color: bool = True,
):
    """
    Create the PyGMT logo using PyGMT.
    The design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
    and consists of a visual and the wordmark "PyGMT".

    Parameters
    ----------

    shape
        Shape of the visual logo. Use ``"circle"`` for a circle shape [Default] or
        ``"hexagon"`` for a hexagon shape.
    theme
        Use ``"light"`` for light mode (i.e., a white background) [Default] and
        ``"dark"`` for dark mode (i.e., a darkgray [gray20] background).
    wordmark
        Add the wordmark "PyGMT" and adjust its orientation relative to the visual. Set
        to ``True`` or ``"horizontal"``, to add the wordmark at the right side of the
        visual [Default]. Use ``"vertical"`` to place the wordmark below the visual
        and ``False`` to add no wordmark.
    color
        Set to ``True`` to use colors referring to Python (blue and yellow) and GMT
        (red) [Default]. For ``False``, the logo is drawn in black and white.

    """

    # Helpful definitions
    size = 4
    region = [-size, size] * 2
    projection = "x1c"

    # Radii
    r0, r1, r2, r3, r4, r5 = size * np.array(
        [1, 0.875, 0.58125, 0.4625, 0.4125, 0.29375]
    )
    thick = r0 - r1  # thick pen in centimeters
    thin = thick / 3  # thin pen in centimeters

    # Rotation around z (vertical) axis placed in the center
    # Has to be applied to each plotting command, up on second call set to True
    perspective = "30+w0/0"  # by 30 degrees counter-clockwise

    # Define colors
    color_light = "white"
    color_dark = "gray20"

    blue = "48/105/152"  # Python blue
    yellow = "255/212/59"  # Python yellow
    red = "238/86/52"  # GMT red
    if not color:
        blue = yellow = red = color_dark
        if theme == "dark":
            blue = yellow = red = color_light

    # Background and wordmark
    match theme:
        case "light":
            color_bg = color_light
            color_py = blue
            color_gmt = color_dark
        case "dark":
            color_bg = color_dark
            color_py = yellow
            color_gmt = color_light

    # Define shape
    match shape:
        case "circle":
            symbol = "c"  # circle
            size_shape = r0 + r1  # radius
            size_shape_add = r0 - r1
            hex_factor = 1
            y_vertline = r0
            y_arrow = -r0
        case "hexagon":
            symbol = "h"  # hexagon
            size_shape = (r0 - 0.3) * 2  # diameter
            size_shape_add = 0.6
            hex_factor = 0.98
            y_vertline = r1 * 0.99
            y_arrow = -r1 * 0.99

    # Define wordmark
    font = "AvantGarde-Book"
    match wordmark:
        case "vertical":
            args_text_wm = {"x": 0, "y": -4.5, "justify": "CT", "font": f"2.5c,{font}"}
        case True | "horizontal":
            args_text_wm = {"x": 4.5, "y": 0.8, "justify": "LM", "font": f"8c,{font}"}

    fig = pygmt.Figure()
    fig.basemap(
        region=region, projection=projection, perspective=perspective, frame="+n"
    )

    args_shape = {
        "x": 0,
        "y": 0,
        "style": f"{symbol}{size_shape}c",
        "perspective": True,
        "no_clip": True,  # Needed for corners of hexagon shape
    }
    # White filled circle / hexagon for Earth
    fig.plot(fill=color_bg, **args_shape)
    # fig.show()

    # Compass (plot vertical line on top of letters G and M again at the end)
    x1, x2 = r1 * 0.7071, r3 * 0.7071  # sqrt(2)/2 = 0.7071
    lines_compass = [
        ([-r0 * hex_factor, -r3], [0, 0]),  # horizontal lines
        ([-r5, 0], [0, 0]),
        ([r3, r0 * hex_factor], [0, 0]),
        ([0, 0], [-r3, 0]),  # vertical line
        ([-x1, -x2], [x1, x2]),  # upper left
        ([-x1, -x2], [-x1, -x2]),  # lower left
        ([x1, x2 + (r4 - r5)], [x1, x2 + (r4 - r5)]),  # upper right
        ([x1, x2], [-x1, -x2]),  # lower right
    ]
    # Non-horizontal compass lines
    for x, y in lines_compass[4 : len(lines_compass)]:
        fig.plot(x=x, y=y, pen=f"{thin}c,{yellow}", perspective=True)
        # fig.show()

    # Blue outlined circle / hexagon for Earth
    fig.plot(pen=f"{thick}c,{blue}", **args_shape)
    # fig.show()
    # Horizontal compass lines
    for x, y in lines_compass[0:4]:
        fig.plot(x=x, y=y, pen=f"{thin}c,{yellow}", perspective=True)
        # fig.show()

    # Letter G
    angles = np.deg2rad(np.arange(90, 361, 1))
    x = np.concatenate(
        [np.cos(angles) * r4, [r4, 0, 0, r5], np.cos(np.flip(angles)) * r5]
    )
    y = np.concatenate(
        [
            np.sin(angles) * r4,
            [(r4 - r5) / 2, (r4 - r5) / 2, -(r4 - r5) / 2, -(r4 - r5) / 2],
            np.sin(np.flip(angles)) * r5,
        ]
    )
    fig.plot(x=x, y=y, fill=red, perspective=True)
    # fig.show()

    # Upper vertical red line
    # Space between red line and blue circle / hexagon
    fig.plot(
        x=[0, 0], y=[y_vertline, r3], pen=f"{thick * 1.5}c,{color_bg}", perspective=True
    )
    # fig.show()
    # red line
    fig.plot(x=[0, 0], y=[y_vertline, r3], pen=f"{thick}c,{red}", perspective=True)
    # fig.show()

    # Letter M
    # Polygon with small distance to horizontal line of letter G
    # Starting point: lower right corner of the left vertical line of letter M
    # Direction: clockwise
    m_x1 = thin / 2  # Half of the pen thickness of compass lines.
    m_x2 = r4
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
    m_y1 = (r4 - r5) / 2 * 1.2
    m_y2 = r4
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
    fig.plot(x=m_x, y=m_y, close=True, fill=red, perspective=True)
    # fig.show()

    # Letter T
    # Red curved horizontal line
    angles = np.deg2rad(np.arange(150, 210, 0.1))
    t_x = np.concatenate([r3 * np.sin(angles), r2 * np.sin(np.flip(angles))])
    t_y = np.concatenate([r3 * np.cos(angles), r2 * np.cos(np.flip(angles))])
    # Ensure the same X coordinate for the right edge of T and the middle of M.
    mask = np.abs(t_x) <= (m_x1 + (m_x2 - m_x1) / 2)
    fig.plot(x=t_x[mask], y=t_y[mask], fill=red, perspective=True)
    # fig.show()
    # The arrow
    fig.plot(
        data=[[0, -r2, 0, y_arrow * 1.05]],
        pen=color_bg,
        style=f"v{thick * 1.6}c+s+e+h0+a60+g{color_bg}",
        perspective=True,
    )
    # fig.show()
    fig.plot(
        data=[[0, -r3, 0, y_arrow]],
        pen=f"{thick}c,{red}",
        style=f"v{thick * 1.4}c+s+e+h0+a60+g{red}",
        perspective=True,
    )
    # fig.show()

    # Extra vertical compass line above letters G and M.
    fig.plot(x=[0, 0], y=[-r5 * 0.9, r3], pen=f"5p,{yellow}", perspective=True)
    # fig.show()

    # Outline around the shape for black and white color with dark theme
    if not color and theme == "dark":
        fig.plot(
            x=0,
            y=0,
            style=f"{symbol}{size_shape + size_shape_add}c",
            pen=f"1p,{color_dark}",
            perspective=True,
            no_clip=True,
        )
        # fig.show()

    # Add wordmark "PyGMT"
    if wordmark:
        text_wm = f"@;{color_py};Py@;;@;{color_gmt};GMT@;;"
        fig.text(text=text_wm, no_clip=True, **args_text_wm)
        # fig.show()

    # Helpful for implementing the logo; not included in the logo
    # Circles for the different radii
    # for r in [r0, r1, r2, r3, r4, r5, r2 + (r3 - r4)]:
    #     fig.plot(x=0, y=0, style=f"c{2 * r}c", pen="0.8p,black,dashed")
    # Map frame with annotations, tick marks, and gridlines
    # with pygmt.config(MAP_FRAME_TYPE="inside"):
    #     fig.basemap(frame="a1g1")

    # fig.show()
    fig_name_logo = "pygmt_logo"
    fig.savefig(fname=f"{fig_name_logo}.eps")

    return fig_name_logo


def pygmtlogo(  # noqa: PLR0913
    self,
    color=True,
    theme="light",
    shape="circle",
    wordmark=True,
    position=None,  # -> Use position parameter of Figure.image
    box=None,  # -> Use box parameter of Figure.image
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
