"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias
from pygmt.exceptions import GMTInvalidInput
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Axis(BaseParam):
    """
    Class for setting up one axis of a plot.
    """

    #: Intervals for annotations, ticks and grid lines.
    annotation: float | None = None
    tick: float | None = None
    grid: float | None = None

    #: Plot slanted annotations (for Cartesian plots only), where *angle* is measured
    #: with respect to the horizontal and must be in the -90 <= *angle* <= 90 range.
    #: Default is normal (i.e., ``angle=90``) for y-axis and parallel (i.e.,
    #: ``angle=0``) for x-axis annotations. These defaults can be changed via
    #: :gmt-term:`MAP_ANNOT_ORTHO`.
    angle: float | None = None

    #: Skip annotations that fall exactly at the ends of the axis. Choose from ``left``
    #: or ``right`` to skip only the lower or upper annotation, respectively, or
    #: ``True`` to skip both.
    skip_edge: Literal["left", "right"] | bool = False

    #: Give fancy annotations with W|E|S|N suffixes encoding the sign (for geographic
    #: axes only).
    fancy: bool = False

    #: Add a label to the axis (for Cartesian plots only). The label is placed parallel
    #: to the axis by default; use **hlabel** to force a horizontal label for y-axis,
    #: which is useful for very short labels.
    label: str | None = None
    hlabel: str | None = None

    #: Add an alternate label for the right or upper axes. The label is placed parallel
    #: to the axis by default; use **alt_hlabel** to force a horizontal label for
    #: y-axis, which is useful for very short labels. [For Cartesian plots only].
    alt_label: str | None = None
    alt_hlabel: str | None = None

    #: Add a leading text prefix for axis annotation (e.g., dollar sign for plots
    #: related to money) (for Cartesian plots only). For geographic maps the addition
    #: of degree symbols is automatic and controlled by :gmt-term:`FORMAT_GEO_MAP`.
    prefix: str | None = None

    #: Append a unit to the annotations (for Cartesian plots only). For geographic maps
    #: the addition of degree symbols, etc. is automatic and controlled by
    #: :gmt-term:`FORMAT_GEO_MAP`.
    unit: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.annotation, name="annotation", prefix="a"),
            Alias(self.tick, name="tick", prefix="f"),
            Alias(self.grid, name="grid", prefix="g"),
            Alias(self.angle, name="angle", prefix="+a"),
            Alias(
                self.skip_edge,
                name="skip_edge",
                prefix="+e",
                mapping={True: True, "left": "l", "right": "r"},
            ),
            Alias(self.fancy, name="fancy", prefix="+f"),
            Alias(self.label, name="label", prefix="+l"),
            Alias(self.hlabel, name="hlabel", prefix="+L"),
            Alias(self.alt_label, name="alt_label", prefix="+s"),
            Alias(self.alt_hlabel, name="alt_hlabel", prefix="+S"),
            Alias(self.prefix, name="prefix", prefix="+p"),
            Alias(self.unit, name="unit", prefix="+u"),
        ]


@dataclasses.dataclass(repr=False)
class _Axes(BaseParam):
    """
    A private class to build the Axes part of the Frame class.
    """

    # Refer to the Frame class for full documentation.
    axes: str | None = None
    fill: str | None = None
    title: str | None = None
    subtitle: str | None = None
    box: bool = False
    pen: str | bool = False
    yzfill: str | None = None
    xzfill: str | None = None
    xyfill: str | None = None
    pole: Sequence[float | str] | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.axes, name="axes"),
            Alias(self.fill, name="fill", prefix="+g"),
            Alias(self.title, name="title", prefix="+t"),
            Alias(self.subtitle, name="subtitle", prefix="+s"),
            Alias(self.box, name="box", prefix="+b"),
            Alias(self.pen, name="pen", prefix="+w"),
            Alias(self.yzfill, name="yzfill", prefix="+y"),
            Alias(self.xzfill, name="xzfill", prefix="+x"),
            Alias(self.xyfill, name="xyfill", prefix="+z"),
            Alias(self.pole, name="pole", prefix="+o", sep="/", size=2),
        ]


@dataclasses.dataclass(repr=False)
class Frame(BaseParam):
    """
    Class for setting up the frame of a plot.
    """

    #: Specify the attributes for each axis.
    #:
    #: ``axis`` means specifying the same attributes for all axes.
    #: ``x``, ``y``, ``z`` mean specifying attributes for the x-, y-, and z-axes,
    #: respectively, while ``xp``, ``yp``, ``zp`` mean specifying attributes for the
    #: x-, y-, and z-axes' primary axes, and ``xs``, ``ys``, ``zs`` mean specifying
    #: attributes for the x-, y-, and z-axes' secondary axes.
    axis: Axis | None = None
    x: Axis | None = None
    y: Axis | None = None
    z: Axis | None = None
    xp: Axis | None = None
    yp: Axis | None = None
    zp: Axis | None = None
    xs: Axis | None = None
    ys: Axis | None = None
    zs: Axis | None = None

    #: Specify which axes to draw and their attributes.
    axes: str | None = None

    #: Fill for the interior of the canvas [Default is no fill]. This also sets fill
    #: for the two back-walls in 3-D plots.
    fill: str | None = None

    #: The title string centered above the plot frame [Default is no title].
    title: str | None = None

    #: The subtitle string beneath the title [Default is no subtitle]. This requires
    #: ``title`` to be set.
    subtitle: str | None = None

    #: [For 3-D plots only] Draw the foreground lines of the 3-D cube .
    box: bool = False

    #: [For 3-D plots only] If ``True``, draw the outlines of the x-z and y-z planes.
    #: Set pen to specify different pen attributes [default is
    #: :gmt-term:`MAP_GRID_PEN_PRIMARY`].
    pen: str | bool = False

    #: Fill the y-z plane with specified color/pattern.
    yzfill: str | None = None

    #: Fill the x-z plane with specified color/pattern.
    xzfill: str | None = None

    #: Fill the x-y plane with specified color/pattern.
    xyfill: str | None = None

    #: Specify another pole (*lon*, *lat*) to produce oblique gridlines about the
    #: specified pole rather than the default [default references to the North pole].
    #: Ignored if no gridlines are requested. Note: One cannot specify oblique gridlines
    #: for non-geographic projections as well as the oblique Mercator projection.
    pole: Sequence[float | str] | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        # Can't specify both axis and individual axes.
        if self.axis is not None and any(
            getattr(self, k) is not None
            for k in [
                "x",
                "y",
                "z",
                "xp",
                "yp",
                "zp",
                "xs",
                "ys",
                "zs",
            ]
        ):
            msg = (
                "Cannot specify both 'axis' and individual axes ('x', 'y', 'z', etc.)."
            )
            raise GMTInvalidInput(msg)
        if self.x is not None and (self.xp is not None or self.xs is not None):
            msg = "Cannot specify both 'x' and 'xp'/'xs'."
            raise GMTInvalidInput(msg)
        if self.y is not None and (self.yp is not None or self.ys is not None):
            msg = "Cannot specify both 'y' and 'yp'/'ys'."
            raise GMTInvalidInput(msg)
        if self.z is not None and (self.zp is not None or self.zs is not None):
            msg = "Cannot specify both 'z' and 'zp'/'zs'."
            raise GMTInvalidInput(msg)

    @property
    def _aliases(self):
        return [
            Alias(self.axis, name="axis"),
            Alias(self.x, prefix="x"),
            Alias(self.y, prefix="y"),
            Alias(self.z, prefix="z"),
            Alias(self.xp, prefix="px"),
            Alias(self.yp, prefix="py"),
            Alias(self.zp, prefix="pz"),
            Alias(self.xs, prefix="sx"),
            Alias(self.ys, prefix="sy"),
            Alias(self.zs, prefix="sz"),
            Alias(
                _Axes(
                    axes=self.axes,
                    fill=self.fill,
                    title=self.title,
                    subtitle=self.subtitle,
                    box=self.box,
                    pen=self.pen,
                    yzfill=self.yzfill,
                    xzfill=self.xzfill,
                    xyfill=self.xyfill,
                    pole=self.pole,
                )
            ),
        ]

    def __iter__(self):
        """
        Iterate over the aliases of the class.

        Yields
        ------
        The value of each alias in the class. None are excluded.
        """
        yield from (alias._value for alias in self._aliases if alias._value is not None)
