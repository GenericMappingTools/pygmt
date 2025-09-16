"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses
from typing import Any, Literal

from pygmt.alias import Alias
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Axes(BaseParam):
    """
    Class for specifying the frame of a plot.

    Attributes
    ----------
    axes
        Specify which axes to draw and their attributes.
    fill
        Fill for the interior of the canvas [Default is no fill]. This also sets fill
        for the two back-walls in 3-D plots.
    title
        The title string centered above the plot frame [Default is no title].
    subtitle
        The subtitle string beneath the title [Default is no subtitle]. This requires
        ``title`` to be set.

    Examples
    --------
    >>> from pygmt.params import Axes
    >>> str(Axes("WSen", title="My Plot Title", fill="lightred"))
    'WSen+glightred+tMy Plot Title'
    """

    axes: str | None = None
    fill: str | None = None
    title: str | None = None
    subtitle: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.axes, name="axes"),
            Alias(self.fill, name="fill", prefix="+g"),
            Alias(self.title, name="title", prefix="+t"),
            Alias(self.subtitle, name="subtitle", prefix="+s"),
        ]


@dataclasses.dataclass(repr=False)
class Axis(BaseParam):
    """
    Class for setting up one axis of a plot.

    Attributes
    ----------
    interval
        Intervals for annotations and major tick spacing, minor tick spacing, and/or
        grid line spacing.
    angle
        Plot slanted annotations (for Cartesian plots only), where *angle* is measured
        with respect to the horizontal and must be in the -90 <= *angle* <= 90 range.
        Default is normal (i.e., ``angle=90``) for y-axis and parallel (i.e.,
        ``angle=0``) for x-axis annotations. These defaults can be changed via
        :gmt-term:`MAP_ANNOT_ORTHO`.
    skip_edge
        Skip annotations that fall exactly at the ends of the axis. Choose from ``left``
        or ``right`` to skip only the lower or upper annotation, respectively, or
        ``True`` to skip both.
    fancy
        Give fancy annotations with W|E|S|N suffixes encoding the sign (for geographic
        axes only).
    label/hlabel
        Add a label to the axis (for Cartesian plots only). The label is placed parallel
        to the axis by default; use **hlabel** to force a horizontal label for y-axis,
        which is useful for very short labels.
    alt_label/alt_hlabel
        Add an alternate label for the right or upper axes. The label is placed parallel
        to the axis by default; use **alt_hlabel** to force a horizontal label for
        y-axis, which is useful for very short labels. [For Cartesian plots only].
    prefix
        Add a leading text prefix for axis annotation (e.g., dollar sign for plots
        related to money) (for Cartesian plots only). For geographic maps the addition
        of degree symbols, etc. is automatic and controlled by
        :gmt-term:`FORMAT_GEO_MAP`.
    unit
        Append a unit to the annotations (for Cartesian plots only). For geographic maps
        the addition of degree symbols, etc. is automatic and controlled by
        :gmt-term:`FORMAT_GEO_MAP`.

    Examples
    --------
    >>> from pygmt.params import Axis
    >>> str(Axis(10, angle=30, label="X axis", unit="km"))
    '10+a30+lX axis+ukm'
    """

    interval: float | str  # How to make it more Pythonic?
    angle: float | None = None
    skip_edge: Literal["left", "right"] | bool = False
    fancy: bool = False
    label: str | None = None
    hlabel: str | None = None
    alt_label: str | None = None
    alt_hlabel: str | None = None
    prefix: str | None = None
    unit: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.interval, name="interval"),
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
            Alias(self.unit, name="unit", prefix="+u"),
        ]


@dataclasses.dataclass(repr=False)
class Frame(BaseParam):
    """
    Class for setting up the frame of a plot.

    >>> from pygmt.alias import AliasSystem, Alias
    >>> from pygmt.params import Frame, Axes, Axis
    >>> frame = Frame(
    ...     axes=Axes("WSen", title="My Plot Title", fill="lightred"),
    ...     xaxis=Axis(10, angle=30, label="X axis", unit="km"),
    ... )
    >>> def func(frame):
    ...     alias = AliasSystem(B=Alias(frame))
    ...     return alias.kwdict
    >>> dict(func(frame))
    {'B': ['WSen+glightred+tMy Plot Title', 'x10+a30+lX axis+ukm']}
    """

    axes: Any = None
    xaxis: Any = None
    yaxis: Any = None
    zaxis: Any = None

    @property
    def _aliases(self):
        return [
            Alias(self.axes),
            Alias(self.xaxis, prefix="x"),
            Alias(self.yaxis, prefix="y"),
            Alias(self.zaxis, prefix="z"),
        ]

    def __iter__(self):
        """
        Iterate over the aliases of the class.

        Yields
        ------
        The value of each alias in the class. None are excluded.
        """
        yield from (alias._value for alias in self._aliases if alias._value is not None)
