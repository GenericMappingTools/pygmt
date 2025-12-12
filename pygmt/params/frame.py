"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses
from typing import Any, Literal

from pygmt.alias import Alias
from pygmt.exceptions import GMTInvalidInput
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Axis(BaseParam):
    """
    Class for setting up one axis of a plot.
    """

    #: Specify annotation for the axis. Provide a specific interval with an optional
    #: unit. Set to ``True`` to use default interval.
    annotation: float | str | bool = False

    #: Specify ticks for the axis. Provide a specific interval with an optional unit.
    #: Set to ``True`` to use default interval.
    tick: float | str | bool = False

    #: Specify grid lines for the axis. Provide a specific interval with an optional
    #: unit. Set to ``True`` to use default interval.
    grid: float | str | bool = False

    #: Plot slanted annotations (for Cartesian plots only), where *angle* is measured
    #: with respect to the horizontal and must be in the -90 <= *angle* <= 90 range.
    #: Default is normal (i.e., ``angle=90``) for y-axis and parallel (i.e.,
    #: ``angle=0``) for x-axis annotations. These defaults can be changed via
    #: :gmt-term:`MAP_ANNOT_ORTHO`.
    angle: float | None = None

    #: Skip annotations that fall exactly at the ends of the axis. Choose from ``lower``
    #: or ``upper`` to skip only the lower or upper annotation, respectively, or
    #: ``True`` to skip both.
    skip_edge: Literal["lower", "upper"] | bool = False

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
    #: of degree symbols, etc. is automatic and controlled by
    #: :gmt-term:`FORMAT_GEO_MAP`.
    prefix: str | None = None

    #: Append a unit to the annotations (for Cartesian plots only). For geographic maps
    #: the addition of degree symbols, etc. is automatic and controlled by
    #: :gmt-term:`FORMAT_GEO_MAP`.
    unit: str | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        if self.label is not None and self.hlabel is not None:
            msg = "Parameters 'label' and 'hlabel' cannot be both set."
            raise GMTInvalidInput(msg)
        if self.alt_label is not None and self.alt_hlabel is not None:
            msg = "Parameters 'alt_label' and 'alt_hlabel' cannot be both set."
            raise GMTInvalidInput(msg)

    @property
    def _aliases(self):
        return [
            Alias(self.annotation, name="annotation", prefix="a"),
            Alias(self.tick, name="tick", prefix="f"),
            Alias(self.grid, name="grid", prefix="g"),
            Alias(
                self.angle,
                name="angle",
                prefix="+a",
                mapping={"normal": "n", "parallel": "p"}
                if isinstance(self.angle, str)
                else None,
            ),
            Alias(
                self.skip_edge,
                name="skip_edge",
                prefix="+e",
                mapping={True: True, "lower": "l", "upper": "u"},
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
class Axes(BaseParam):
    """
    Class for specifying the frame of a plot.
    """

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

    @property
    def _aliases(self):
        return [
            Alias(self.axes, name="axes"),
            Alias(self.fill, name="fill", prefix="+g"),
            Alias(self.title, name="title", prefix="+t"),
            Alias(self.subtitle, name="subtitle", prefix="+s"),
        ]


@dataclasses.dataclass(repr=False)
class Frame(BaseParam):
    """
    Class for setting up the frame of a plot.
    """

    axes: Any = None
    axis: Any = None
    xaxis: Any = None
    yaxis: Any = None
    zaxis: Any = None
    xaxis_secondary: Any = None
    yaxis_secondary: Any = None
    zaxis_secondary: Any = None

    @property
    def _aliases(self):
        return [
            Alias(self.axes),
            Alias(self.axis),
            Alias(self.xaxis, prefix="x"),
            Alias(self.yaxis, prefix="y"),
            Alias(self.zaxis, prefix="z"),
            Alias(self.xaxis_secondary, prefix="sx"),
            Alias(self.yaxis_secondary, prefix="sy"),
            Alias(self.zaxis_secondary, prefix="sz"),
        ]

    def __iter__(self):
        """
        Iterate over the aliases of the class.

        Yields
        ------
        The value of each alias in the class. None are excluded.
        """
        yield from (alias._value for alias in self._aliases if alias._value is not None)
