"""
The Axes, Axis, and Frame classes for specifying the frame.
"""

import dataclasses

from pygmt.alias import Alias
from pygmt.exceptions import GMTParameterError
from pygmt.params.base import BaseParam

__doctest_skip__ = ["Axis", "Frame"]


@dataclasses.dataclass(repr=False)
class Axis(BaseParam):
    """
    Class for setting up one axis of a plot.

    Examples
    --------
    To specify the same attributes for all axes, with intervals of 4 for annotations,
    2 for ticks, and 1 for gridlines:

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 20],
    ...     projection="X10c/10c",
    ...     frame=Axis(annot=4, tick=2, grid=1),
    ... )
    >>> fig.show()
    """

    #: Specify the interval for annoations. It can be ``True`` to let GMT decide the
    #: interval automatically; or a value to set a specific interval in the format of
    #: *stride*\ [±\ *phase*][*unit*], where, *stride* is the interval, *phase* is the
    #: offset to shift the annotations by that amount, and *unit* is one of the
    #: :gmt-docs:`18 supported unit codes <reference/options.html#tbl-units>` related to
    #: time intervals.
    annot: float | bool = False

    #: Specify the interval for ticks. Same format as ``annot``.
    tick: float | bool = False

    #: Specify the interval for gridlines. Same format as ``annot``.
    grid: float | bool = False

    #: Label for the axis [Default is no label].
    label: str | None = None

    #: A leading text prefix for the axis annotations (e.g., dollar sign for plots
    #: related to money) [For Cartesian plots only].
    prefix: str | None = None

    #: Unix to append to the axis annotations [For Cartesian plots only].
    unit: str | None = None

    #: Angle of the axis annotations.
    angle: float | None = None

    @property
    def _aliases(self):
        return [
            Alias(self.annot, name="annot", prefix="a"),
            Alias(self.tick, name="tick", prefix="f"),
            Alias(self.grid, name="grid", prefix="g"),
            Alias(self.label, name="label", prefix="+l"),
            Alias(self.angle, name="angle", prefix="+a"),
            Alias(self.prefix, name="prefix", prefix="+p"),
            Alias(self.unit, name="unit", prefix="+u"),
        ]


@dataclasses.dataclass(repr=False)
class _Axes(BaseParam):
    """
    A private class to build the Axes part of the Frame class.
    """

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
    Class for setting up the frame and axes of a plot.

    Examples
    --------
    To specify the west and south axes with both tick marks and annotations, draw the
    east and north axes with tick marks but without annotations:

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 20], projection="X10c/10c", frame=Frame(axes="WSen")
    ... )
    >>> fig.show()

    To specify the same attributes for all axes, with intervals of 4 for annotations,
    2 for ticks, and 1 for gridlines:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 20],
    ...     projection="X10c/10c",
    ...     frame=Frame(axes="WSrt", axis=Axis(annot=4, tick=2, grid=1)),
    ... )
    >>> fig.show()

    To specify the attributes for each axis separately:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 20],
    ...     projection="X10c/10c",
    ...     frame=Frame(
    ...         axes="WSrt",
    ...         xaxis=Axis(annot=4, tick=2, grid=1, label="X Label"),
    ...         yaxis=Axis(annot=5, tick=2.5, grid=1, label="Y Label"),
    ...     ),
    ... )
    >>> fig.show()
    """

    #: Controls which axes are drawn and whether they are annotated, using a combination
    #: of the codes below. Axis ommitted from the set will not be drawn.
    #:
    #: For a 2-D plot, there are four axes: west, east, south, and north (or left,
    #: right, bottom, top if you prefer); For a 3-D plot, there is an extra Z-axis.
    #: They can be denoted by the following codes:
    #:
    #: - **W** (west), **E** (east), **S** (south), **N** (north), **Z**: Draw axes with
    #:   both tick marks and annotations.
    #: - **w** (west), **e** (east), **s** (south), **n** (north), **z**: Draw axes with
    #:   tick marks but without annotations.
    #: - **l** (left), **r** (right), **b** (bottom), **t** (top), **u** (up): Draw axes
    #:   without tick marks or annotations.
    #:
    #: For examples:
    #:
    #: - ``"WS"``: Draw the west and south axes with both tick marks and annotations,
    #:   but do not draw the east and north axes.
    #: - ``"WSen"``: Draw the west and south axes with both tick marks and annotations,
    #:   draw the east and north axes with tick marks but without annotations.
    #: - ``"WSrt"``: Draw the west and south axes with both tick marks and annotations,
    #:   draw the east and north axes without tick marks or annotations.
    #: - ``"WSrtZ"``: Draw the west and south axes with both tick marks and annotations,
    #:   draw the east and north axes without tick marks or annotations, and draw the
    #:   z-axis with both tick marks and annotations.
    #:
    #: For a 3-D plot, if the z-axis code is specified, a single vertical axis will be
    #: drawn at the most suitable corner by default. Append any combination of the
    #: corner IDs from 1 to 4 to draw one or more vertical axes at the corresponding
    #: corners (e.g., ``"WSrtZ1234"``):
    #:
    #: - **1**: the south-western (lower-left) corner
    #: - **2**: the south-eastern (lower-right) corner
    #: - **3**: the north-eastern (upper-right) corner
    #: - **4**: the north-western (upper-left) corner
    axes: str | None = None

    #: The title string centered above the plot frame [Default is no title].
    title: str | None = None

    #: Specify the attributes for axes by an :class:`Axis` object.
    #:
    #: The attributes for each axis can be specified in two ways: (1) specifying the
    #: same attributes for all axes using the ``axis`` parameter; (2) specifying the
    #: attributes for each axis separately using the ``xaxis``, ``yaxis``, ``zaxis``
    #: parameter for the x-, y, and z-axes, respectively.
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
        # _Axes() maps to an empty string, which becomes '-B' without arguments and is
        # invalid when combined with individual axis settings (e.g., '-B -Bxaf -Byaf').
        frame_settings = _Axes(axes=self.axes, title=self.title)
        return [
            Alias(frame_settings) if str(frame_settings) else Alias(None),
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
