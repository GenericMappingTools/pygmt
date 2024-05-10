"""
The box parameter.
"""

from dataclasses import dataclass
from typing import Any, ClassVar

from pygmt.alias import Alias
from pygmt.params.base import BaseParam


@dataclass(repr=False)
class Axes(BaseParam):
    """
    Examples
    --------
    >>> from pygmt.params import Axes
    >>> str(Axes("WSen", title="My Plot Title", fill="lightred"))
    'WSen+glightred+tMy Plot Title'
    """

    axes: Any = None
    fill: Any = None
    title: Any = None

    _aliases: ClassVar = [
        Alias("axes"),
        Alias("fill", prefix="+g"),
        Alias("title", prefix="+t"),
    ]


@dataclass(repr=False)
class Axis(BaseParam):
    """
    >>> from pygmt.params import Axis
    >>> str(Axis(10, angle=30, label="X axis", unit="km"))
    '10+a30+lX axis+ukm'
    """

    interval: float | str
    angle: float | str | None = None
    label: str | None = None
    unit: str | None = None

    _aliases: ClassVar = [
        Alias("interval"),
        Alias("angle", prefix="+a"),
        Alias("label", prefix="+l"),
        Alias("unit", prefix="+u"),
    ]


@dataclass(repr=False)
class Frame(BaseParam):
    """
    >>> from pygmt.alias import AliasSystem, Alias
    >>> from pygmt.params import Frame, Axes, Axis
    >>> frame = Frame(
    ...     axes=Axes("WSen", title="My Plot Title", fill="lightred"),
    ...     xaxis=Axis(10, angle=30, label="X axis", unit="km"),
    ... )
    >>> def func(frame):
    ...     alias = AliasSystem(B="frame")
    ...     return alias.kwdict
    >>> dict(func(frame))
    {'B': ['WSen+glightred+tMy Plot Title', 'x10+a30+lX axis+ukm']}
    """

    axes: Any = None
    xaxis: Any = None
    yaxis: Any = None
    zaxis: Any = None

    _aliases: ClassVar = [
        Alias("axes"),
        Alias("xaxis", prefix="x"),
        Alias("yaxis", prefix="y"),
        Alias("zaxis", prefix="z"),
    ]

    def __iter__(self):
        """
        Iterate over the aliases of the class.

        Yields
        ------
        The value of each alias in the class. None are excluded.
        """
        for alias in self._aliases:
            alias.value = getattr(self, alias.name)
            if alias.value is not None:
                yield alias.value
