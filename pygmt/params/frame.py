"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses
from pygmt.alias import Alias
from pygmt.params.base import BaseParam
from typing import Any


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

    Examples
    --------
    >>> from pygmt.params import Axis
    >>> str(Axis(10, angle=30, label="X axis", unit="km"))
    '10+a30+lX axis+ukm'
    """

    interval: float | str
    angle: float | str | None = None
    label: str | None = None
    unit: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.interval),
            Alias(self.angle, prefix="+a"),
            Alias(self.label, prefix="+l"),
            Alias(self.unit, prefix="+u"),
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
