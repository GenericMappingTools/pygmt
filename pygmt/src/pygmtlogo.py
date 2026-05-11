"""
pygmtlogo - Plot the PyGMT logo.

The initial design of the logo is kindly provided by `@sfrooti <https://github.com/sfrooti>`_
and consists of a visual and the wordmark "PyGMT".
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
from pygmt._typing import AnchorCode, PathLike
from pygmt.exceptions import GMTValueError
from pygmt.helpers import GMTTempFile, fmt_docstring
from pygmt.params import Box, Position

__doctest_skip__ = ["pygmtlogo"]


def _create_logo(  # noqa: PLR0915
    shape: Literal["circle", "hexagon"] = "circle",
    theme: Literal["light", "dark"] = "light",
    wordmark: Literal["none", "horizontal", "vertical"] = "none",
    color: bool = True,
    figname: PathLike | None = None,
    debug: bool = False,
):
    """
    Create the PyGMT logo using PyGMT.
    """
    from pygmt.figure import Figure  # noqa: PLC0415

    # Helpful definitions
    size = 4
    proj = "x1c"
    region = {
        "horizontal": [-size, size * 8.0, -size, size],
        "vertical": [-size, size, -size * 1.75, size],
        "none": [-size, size, -size, size],
    }[wordmark]

    # Rotation around z-axis by 30 degrees counter-clockwise placed in the center.
    perspective = "30+w0/0"

    # Radii (make sure that r4-r5 == r2-r3)
    r0, r1, r2, r3, r4, r5 = size * np.array([128, 112, 75, 61, 53, 39]) / 128
    # Pen thicknesses
    thick_shape = r0 - r1  # for shape
    thick_gt = r4 - r5  # for letters G and T
    thick_m = r4 / 5  # for letter M
    thick_comp = thick_shape / 3  # for compass lines
    thick_gap = thick_shape / 4

    # Define colors
    color_light = "white"
    color_dark = "gray20"
    # Blue, yellow, and red colors
    blue = "48/105/152"  # Python blue
    yellow = "255/212/59"  # Python yellow
    red = "238/86/52"  # GMT red
    if not color:
        mono = color_dark if theme == "light" else color_light
        blue = yellow = red = mono
    # Background and wordmark
    color_bg, color_py, color_gmt = {
        "light": (color_light, blue, color_dark),
        "dark": (color_dark, yellow, color_light),
    }[theme]

    # Define shape
    match shape:
        case "circle":
            symbol = "c"
            size_shape = r0 + r1
            hex_factor = 1.0
        case "hexagon":
            symbol = "h"
            size_shape = (r0 + 0.34) * 2
            hex_factor = 1.1

    # Define wordmark
    font = "AvantGarde-Book"
    match wordmark:
        case "vertical":
            args_text_wm = {"x": 0, "y": -4.5, "justify": "CT", "font": f"2.4c,{font}"}
        case "horizontal":
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
        """Coordinates for letter T."""
        outer_angles = np.deg2rad(np.arange(240, 300, 0.5))
        inner_angles = outer_angles[::-1]
        arc_outer_x, arc_outer_y = np.cos(outer_angles) * r2, np.sin(outer_angles) * r2
        arc_inner_x, arc_inner_y = np.cos(inner_angles) * r3, np.sin(inner_angles) * r3
        # The arrowhead is an equilateral triangle
        x0 = thick_gt / 2  # Extra half-width for arrow head
        y0 = 1.8 * x0 * np.sqrt(3)  # Height for arrow head
        arrow_x = [-x0, -x0, -x0 * 2.0, 0, x0 * 2.0, x0, x0]
        arrow_y = [-r2, -r0 + y0, -r0 + y0, -r0, -r0 + y0, -r0 + y0, -r2]
        mask_left = arc_outer_x < -x0
        mask_right = arc_outer_x > x0
        t_x = np.concatenate(
            [arc_inner_x, arc_outer_x[mask_left], arrow_x, arc_outer_x[mask_right]]
        )
        t_y = np.concatenate(
            [arc_inner_y, arc_outer_y[mask_left], arrow_y, arc_outer_y[mask_right]]
        )
        # Ensure the same X-coordinate for the right edge of T and the middle of M.
        mask = np.abs(t_x) <= (thick_gap + r4) / 2
        return {"x": t_x[mask], "y": t_y[mask]}

    def _bg_arrow_coords():
        """Coordinates for the background arrow."""
        # x0, y0 is the same as in _letter_t_coords().
        x0 = thick_gt / 2
        y0 = 1.8 * x0 * np.sqrt(3)
        # The background arrow is thick_comp wider than the letter T.
        x1 = x0 + thick_comp / 2.0  # Half-width of the arrow tail
        x2 = 2 * x0 + thick_comp / np.sqrt(3)  # Half-width of the arrow head

        arrow_x = [-x1, -x1, -x2, -(x2 - 2 * x0), (x2 - 2 * x0), x2, x1, x1]
        arrow_y = [r0, -r0 + y0, -r0 + y0, -r0, -r0, -r0 + y0, -r0 + y0, r0]
        return {"x": arrow_x, "y": arrow_y}

    def _compass_lines():
        """Coordinates of compass lines."""
        angle = np.deg2rad(45.0)  # Angle of diagonal compass lines
        sinx, cosx = np.sin(angle), np.cos(angle)

        x1, x2, x3 = r0 * sinx, r3 * sinx, (r2 + (r3 - r4)) * sinx
        y1, y2, y3 = r0 * cosx, r3 * cosx, (r2 + (r3 - r4)) * cosx
        # Coordinates of vectors in the format of (x_start, y_start, x_end, y_end).
        return [
            (-r0 * hex_factor, 0, -r3, 0),  # left horizontal
            (r3, 0, r0 * hex_factor, 0),  # right horizontal
            (-x1, y1, -x2, y2),  # upper left
            (-x1, -y1, -x2, -y2),  # lower left
            (x1, y1, x3, y3),  # upper right
            (x1, -y1, x2, -y2),  # lower right
        ]

    def _vline_coords():
        """
        Coordinates for the vertical line at the top.
        """
        x0 = thick_gt / 2
        return {"x": [-x0, -x0, x0, x0], "y": [r0, r3, r3, r0]}

    fig = Figure()
    fig.basemap(region=region, projection=proj, perspective=perspective, frame="none")

    # Earth - circle / hexagon
    args_shape = {
        "style": f"{symbol}{size_shape}c",
        "perspective": True,
        "no_clip": True,  # Needed for corners of hexagon shape
    }
    # Shape fill
    fig.plot(x=0, y=0, fill=color_bg, **args_shape)

    # Compass lines
    fig.plot(
        data=_compass_lines(),
        pen=f"{thick_comp}c,{yellow}",
        style="v0c+s",
        perspective=True,
        no_clip=True,
    )

    # Shape outline (over ends of compass lines for hexagon shape)
    fig.plot(x=0, y=0, pen=f"{thick_shape}c,{blue}", **args_shape)

    # Arrow in background color (over shape outline but under letters)
    fig.plot(data=_bg_arrow_coords(), fill=color_bg, perspective=True)

    # Letters G, M, and T
    fig.plot(data=_letter_g_coords(), fill=red, perspective=True)
    fig.plot(data=_letter_m_coords(), fill=red, perspective=True)
    fig.plot(data=_letter_t_coords(), fill=red, perspective=True)

    # Upper vertical line
    fig.plot(data=_vline_coords(), fill=red, perspective=True)

    # Outline around the shape for black and white color with dark theme
    if not color and theme == "dark":
        fig.plot(
            x=0,
            y=0,
            style=f"{symbol}{size_shape + thick_shape}c",
            pen=f"{thick_comp / 2.0}c,{color_bg}",
            perspective=True,
            no_clip=True,
        )

    # Add wordmark "PyGMT"
    if wordmark != "none":
        fig.text(text=f"@;{color_py};Py@;;@;{color_gmt};GMT@;;", **args_text_wm)

    # Helpful for implementing the logo; not included in the logo
    if debug:
        from pygmt import config  # noqa: PLC0415

        # Gridlines
        with config(MAP_GRID_PEN="0.1p,gray30"):
            fig.basemap(frame="00g1")
        # Circles for the different radii
        for r in [r0, r1, r2, r3, r4, r5]:
            fig.plot(x=0, y=0, style=f"c{2 * r}c", pen="0.3p,gray30")
        pen = "0.3p,gray30,2_2"
        fig.plot(x=0, y=0, style=f"c{2 * (r2 + (r3 - r4))}c", pen=pen)
        # Lines for letter M
        fig.hlines(y=[r4, r5], xmin=-size, xmax=size, pen=pen, perspective=True)
        m_mid = (thick_gap + r4) / 2
        fig.vlines(x=[r4, m_mid], ymin=size, ymax=size, pen=pen, perspective=True)

    if figname:
        fig.savefig(fname=figname)
        return None
    return fig


@fmt_docstring
def pygmtlogo(  # noqa: PLR0913
    self,
    shape: Literal["circle", "hexagon"] = "circle",
    theme: Literal["light", "dark"] = "light",
    wordmark: Literal["none", "horizontal", "vertical"] = "none",
    color: bool = True,
    width: float | str | None = None,
    height: float | str | None = None,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
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
        ``"dark"`` for dark mode (i.e., a darkgray background).
    wordmark
        Add the wordmark "PyGMT" and adjust its orientation relative to the visual.
        Valid values are:

        - ``"none"``: no wordmark [Default].
        - ``"horizontal"``: wordmark at the right side of the visual.
        - ``"vertical"``: wordmark below the visual.
    color
        ``True`` for a color logo, and ``False`` for a black and white logo.
    position
        Position of the GMT logo on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Bottom Left corner of the plot (position
        ``(0, 0)`` with anchor ``"BL"``).
    width
    height
        Width or height of the PyGMT logo. Since the aspect ratio is fixed, only one of
        the two can be specified. If not specified, the default size of the visual logo
        is set to 2 cm.
    box
        Draw a background box behind the logo. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    $verbose
    $panel
    $perspective
    $transparency

    Examples
    --------
    >>> import pygmt

    The simplest way to plot the PyGMT logo is to call the method without any arguments.

    >>> fig = pygmt.Figure()
    >>> fig.pygmtlogo()
    >>> fig.show()

    Plot the PyGMT logo with the wordmark "PyGMT" with a height of 1 centimeter at the
    right side in the Bottom Right corner on an existing basemap:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[-90, -70, 0, 20], projection="M10c", frame=True)
    >>> fig.pygmtlogo(wordmark="horizontal", position="BR", height="1c")
    >>> fig.show()
    """
    # Set the default size of the visual logo to 2 cm.
    if width is None and height is None:
        match wordmark:
            case "none" | "vertical":
                width = width or "2c"
            case "horizontal":
                height = height or "2c"
            case _:
                raise GMTValueError(
                    wordmark,
                    description="value for wordmark",
                    choices={"none", "horizontal", "vertical"},
                )

    with GMTTempFile(suffix=".eps") as logofile:
        # Create logo file
        _create_logo(
            color=color,
            theme=theme,
            shape=shape,
            wordmark=wordmark,
            figname=logofile.name,
        )

        # Add to existing Figure instance
        self.image(
            imagefile=logofile.name,
            position=position,
            width=width,
            height=height,
            box=box,
            verbose=verbose,
            panel=panel,
            perspective=perspective,
            transparency=transparency,
        )
