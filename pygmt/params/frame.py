"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses

from pygmt.alias import Alias
from pygmt.exceptions import GMTParameterError
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Axis(BaseParam):
    """
    Class for setting up one axis of a plot.
    """

    # Specify the intervals for annotations, ticks, and gridlines.
    annot: float | None = None
    tick: float | None = None
    grid: float | None = None
    # The label for the axis [Default is no label].
    label: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.annot, name="annot", prefix="a"),
            Alias(self.tick, name="tick", prefix="f"),
            Alias(self.grid, name="grid", prefix="g"),
            Alias(self.label, name="label", prefix="+l"),
        ]


@dataclasses.dataclass(repr=False)
class _Axes(BaseParam):
    """
    A private class to build the Axes part of the Frame class.
    """

    # Refer to the Frame class for full documentation.
    axes: str | None = None
    title: str | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.axes, name="axes"),
            Alias(self.title, name="title", prefix="+t"),
        ]


@dataclasses.dataclass(repr=False)
class Frame(BaseParam):
    """
    Class for setting up the frame of a plot.
    """

    #: Specify which axes to draw and their attributes.
    axes: str | None = None

    #: The title string centered above the plot frame [Default is no title].
    title: str | None = None

    #: Specify the attributes for axes.
    #:
    #: The attributes for each axis can be specified in two ways:
    #: #. specifying the same attributes for all axes using the ``axis`` parameter
    #: #. specifying the attributes for each axis separately using the ``xaxis``,
    #: ``yaxis``, ``zaxis`` parameter for the x-, y, and z-axes, respectively.
    #:
    #: GMT uses the notion of primary (the default) and secondary axes, while secondary
    #: axes are optional and mostly used for time axes annotations. To specify the
    #: attributes for the secondary axes, use the ``xaxis2``, ``yaxis2``, and ``zaxis2``
    #: parameters.
    axis: Axis | None = None
    xaxis: Axis | None = None
    yaxis: Axis | None = None
    zaxis: Axis | None = None
    xaxis2: Axis | None = None
    yaxis2: Axis | None = None
    zaxis2: Axis | None = None

    def _validate(self):
        """
        Validate the parameters of the Frame class.
        """
        if self.axis is not None and any(
            [self.xaxis, self.yaxis, self.zaxis, self.xaxis2, self.yaxis2, self.zaxis2]
        ):
            raise GMTParameterError(
                conflicts_with=(
                    "axis",
                    ["xaxis", "yaxis", "zaxis", "xaxis2", "yaxis2", "zaxis2"],
                ),
                reason="Either 'axis' or the individual axis parameters can be set, but not both.",
            )

    @property
    def _aliases(self):
        return [
            Alias(_Axes(axes=self.axes, title=self.title)),
            Alias(self.axis, name="axis"),
            Alias(self.xaxis, name="xaxis", prefix="px" if self.xaxis2 else "x"),
            Alias(self.yaxis, name="yaxis", prefix="py" if self.yaxis2 else "y"),
            Alias(self.zaxis, name="zaxis", prefix="pz" if self.zaxis2 else "z"),
            Alias(self.xaxis2, name="xaxis2", prefix="sx"),
            Alias(self.yaxis2, name="yaxis2", prefix="sy"),
            Alias(self.zaxis2, name="zaxis2", prefix="sz"),
        ]

    def __iter__(self):
        """
        Iterate over the aliases of the class.

        Yields
        ------
        The value of each alias in the class. None are excluded.
        """
        yield from (alias._value for alias in self._aliases if alias._value is not None)
