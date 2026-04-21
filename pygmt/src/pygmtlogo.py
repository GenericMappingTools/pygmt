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
    debug: bool = False,
):
    """
    Create the PyGMT logo using PyGMT.
    """

    # Helpful definitions
    size = 4
    region = [-size, size] * 2
    projection = "x1c"

    # Radii (make sure that r4-r5 == r2-r3)
    r0, r1, r2, r3, r4, r5 = size * np.array(
        [1, 224 / 256, 150 / 256, 122 / 256, 106 / 256, 78 / 256]
    )
    # Pen thicknesses
    thick_shape = r0 - r1  # for shape
    thick_gt = r4 - r5  # for letters G and T
    thick_m = r4 / 5  # for letter M
    thick_comp = thick_shape / 3  # for compass lines
    thick_gap = (thick_comp / 4) * 3

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
            vline_y = r0
            arrow_y = -r0
        case "hexagon":
            symbol = "h"  # hexagon
            size_shape = (r0 + 0.3) * 2  # diameter
            size_shape_add = 0.6
            vline_y = r0 * 0.99
            arrow_y = -r0 * 0.99

    # Define wordmark
    font = "AvantGarde-Book"
    match wordmark:
        case "vertical":
            args_text_wm = {"x": 0, "y": -4.5, "justify": "CT", "font": f"2.5c,{font}"}
        case True | "horizontal":
            args_text_wm = {"x": 4.5, "y": 0.8, "justify": "LM", "font": f"8c,{font}"}

    def _letter_g_coords():
        """Coordinates for letter G."""
        outer_angles = np.deg2rad(np.arange(90, 361))
        inner_angles = outer_angles[::-1]
        offset = thick_gt / 2
        # Outer arc (r4)
        arc_outer_x, arc_outer_y = np.cos(outer_angles) * r4, np.sin(outer_angles) * r4
        # Connecting lines
        connector_x, connector_y = [r4, 0, 0, r5], [offset, offset, -offset, -offset]
        # Inner arc (r5)
        arc_inner_x, arc_inner_y = np.cos(inner_angles) * r5, np.sin(inner_angles) * r5
        # Combine all coordinates (outer arc, connectors, inner arc)
        g_x = np.concatenate([arc_outer_x, connector_x, arc_inner_x])
        g_y = np.concatenate([arc_outer_y, connector_y, arc_inner_y])
        return {"x": g_x, "y": g_y}

    def _letter_m_coords():
        """Coordinates for letter M."""
        # X-coordinates from left to right.
        x1 = thick_gap  # Left edge of left vertical line of M.
        x5 = r4  # Right edge of right vertical line of M.
        x2 = x1 + thick_m  # Right edge of left vertical line of M.
        x3 = (x1 + x5) / 2  # The middle of M.
        x4 = x5 - thick_m  # Left edge of right vertical line of M.
        # Y-coordinates from bottom to top.
        y1 = thick_gt / 2 + thick_gap  # Bottom of the letter M.
        y2 = r5 - thick_gt  # Bottom of the middle peak of M.
        y3 = r5  # Top of the middle peak of M.
        y4 = r4  # Top of letter M.
        # X- and Y-coordinates of the letter M, starting from the left edge of the left
        # vertical line and going clockwise.
        m_x = [x1, x1, x2, x3, x4, x5, x5, x4, x4, x3, x2, x2]
        m_y = [y1, y4, y4, y3, y4, y4, y1, y1, y3, y2, y3, y1]
        return {"x": m_x, "y": m_y}

    def _letter_t_coords():
        """Coordinates of the top curved horizontal line for letter T."""
        outer_angles = np.deg2rad(np.arange(150, 210, 0.5))
        inner_angles = outer_angles[::-1]
        t_x = np.concatenate([r2 * np.sin(outer_angles), r3 * np.sin(inner_angles)])
        t_y = np.concatenate([r2 * np.cos(outer_angles), r3 * np.cos(inner_angles)])
        # Ensure the same X-coordinate for the right edge of T and the middle of M.
        mask = np.abs(t_x) <= (thick_gap + r4) / 2
        return {"x": t_x[mask], "y": t_y[mask]}

    def _compass_lines():
        """
        Coordinates of compass lines.
        """
        sqrt2 = np.sqrt(2) / 2
        x1, x2, x3 = r0 * sqrt2, r3 * sqrt2, (r2 + (r3 - r4)) * sqrt2
        # Coordinates of vectors in the format of (x_start, y_start, x_end, y_end).
        return {
            "hline": [(-r0, 0, -r3, 0), (r3, 0, r0, 0)],
            "diagonal": [
                (-x1, x1, -x2, x2),  # upper left
                (-x1, -x1, -x2, -x2),  # lower left
                (x1, x1, x3, x3),  # upper right
                (x1, -x1, x2, -x2),  # lower right
            ],
        }

    def _vline_coords(gap=0):
        """
        Coordinates for vertical lines.
        """
        x0 = (thick_gt + gap) / 2
        return {"x": [-x0, -x0, x0, x0], "y": [vline_y, r3, r3, vline_y]}

    fig = pygmt.Figure()
    fig.basemap(
        region=region, projection=projection, perspective=perspective, frame="none"
    )

    # Earth - circle / hexagon
    args_shape = {
        "x": 0,
        "y": 0,
        "style": f"{symbol}{size_shape}c",
        "perspective": True,
        "no_clip": True,  # Needed for corners of hexagon shape
    }
    # Shape fill
    fig.plot(fill=color_bg, **args_shape)
    # fig.show()

    # Compass - yellow lines
    args_compass = {
        "pen": f"{thick_comp}c,{yellow}",
        "perspective": True,
        "style": "v0c+s",
    }
    compass_lines = _compass_lines()
    fig.plot(data=compass_lines["diagonal"], **args_compass)
    fig.plot(data=compass_lines["hline"], **args_compass)
    # fig.show()

    # Shape outline (over ends of compass lines for hexagon shape)
    fig.plot(pen=f"{thick_shape}c,{blue}", **args_shape)
    # fig.show()

    # Letter G
    fig.plot(data=_letter_g_coords(), fill=red, perspective=True)
    # Letter M
    fig.plot(data=_letter_m_coords(), fill=red, perspective=True)
    # Letter T: red curved horizontal line
    fig.plot(data=_letter_t_coords(), fill=red, perspective=True)

    # Upper vertical lines
    fig.plot(data=_vline_coords(gap=thick_comp), fill=color_bg, perspective=True)
    fig.plot(data=_vline_coords(), fill=red, perspective=True)

    # The arrow
    fig.plot(
        data=[[0, -r2, 0, arrow_y - thick_comp]],
        pen=color_bg,
        style=f"v{thick_shape + thick_comp * 2}c+s+e+h0+a60+g{color_bg}",
        perspective=True,
    )
    # fig.show()
    fig.plot(
        data=[[0, -r3, 0, arrow_y]],
        pen=f"{thick_gt}c,{red}",
        style=f"v{thick_shape + thick_comp}c+s+e+h0+a60+g{red}",
        perspective=True,
    )
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
    if debug:
        # Gridlines
        with pygmt.config(MAP_FRAME_TYPE="inside", MAP_GRID_PEN="0.1p,gray30"):
            fig.basemap(frame="g1")
        # Circles for the different radii
        for r in [r0, r1, r2, r3, r4, r5]:
            fig.plot(x=0, y=0, style=f"c{2 * r}c", pen="0.3p,gray30")
        fig.plot(x=0, y=0, style=f"c{2 * (r2 + (r3 - r4))}c", pen="0.3p,gray30,2_2")
        # Lines for letter M
        fig.hlines(y=[r4, r5], pen="0.3p,gray30,2_2")
        fig.vlines(x=[r4, (thick_gap + r4) / 2], pen="0.3p,gray30,2_2")

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
        visual [Default]. Use ``"vertical"`` to place the wordmark below the visual and
        ``False`` to add no wordmark.
    color
        Set to ``True`` to use colors referring to Python (blue and yellow) and GMT
        (red) [Default]. For ``False``, the logo is drawn in black and white.
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
