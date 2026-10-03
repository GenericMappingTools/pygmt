"""
The Perspective class for setting perspective view.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam

__doctest_skip__ = ["Perspective"]


@dataclasses.dataclass(repr=False)
class Perspective(BaseParam):
    """
    Class for setting perspective view.

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Axis, Frame, Perspective
    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 10, 0, 20],
    ...     projection="X3c",
    ...     zsize="3c",
    ...     frame=Frame(axes="WSenZ", title="Perspective View", axis=Axis(grid=True)),
    ...     perspective=Perspective(azimuth=135, elevation=40, level=10),
    ... )
    >>> fig.show()
    """

    #: Azimuth angle of the viewpoint in degrees. Default is 180.0, i.e., looking from
    #: south to north.
    azimuth: float | None = None

    #: Elevation angle of the viewpoint in degrees above the horizon. Default is 90.0,
    #: i.e., looking straight down at nadir.
    elevation: float | None = None

    #: The level at which all 2-D elements, (e.g., the plot frame), are drawn. Only
    #: valid when used together with parameters ``zsize`` or ``zscale``. Default is at
    #: the bottom of the selected axis.
    level: float | None = None

    #: Set which constant-coordinate plane is used as the plotting plane. Use ``"x"``,
    #: ``"y"``, or ``"z"`` for the x-plane, y-plane, or horizontal z-plane,
    #: respectively [Default is ``"z"``].
    plane: Literal["x", "y", "z"] | None = None

    #: Reference point for the perspective view. By default, the view rotates about the
    #: plotting origin. Use ``refpoint`` and ``cstype`` to rotate about a different
    #: point instead. The format of ``refpoint`` depends on the value of ``cstype``:
    #:
    #: - ``cstype="mapcoords"``: (*longitude*, *latitude*) or
    #:   (*longitude*, *latitude*, *z*)
    #: - ``cstype="plotcoords"``: (*x*, *y*)
    refpoint: Sequence[float | str] | None = None

    #: Coordinate system type of ``refpoint``. Valid values are:
    #:
    #: - ``"mapcoords"``: Map/data coordinates
    #: - ``"plotcoords"``: Plot coordinates
    #:
    #: Defaults to ``"mapcoords"``.
    cstype: Literal["mapcoords", "plotcoords"] = "mapcoords"

    def _validate(self):
        """
        Post-initialization processing to validate parameters.
        """
        # azimuth is required, so it must be set to the default if not specified.
        if self.azimuth is None:
            self.azimuth = 180.0  # Default azimuth is 180.0

        # Set default elevation if level is set but elevation is not.
        if self.level is not None and self.elevation is None:
            self.elevation = 90.0  # Default elevation is 90.0

        if self.plane is not None and self.plane not in {"x", "y", "z"}:
            raise GMTValueError(
                self.plane, description="plane", choices={"x", "y", "z"}
            )

        if self.cstype not in {"mapcoords", "plotcoords"}:
            raise GMTValueError(
                self.cstype, description="cstype", choices={"mapcoords", "plotcoords"}
            )

    @property
    def _aliases(self):
        """
        Aliases for the parameters.
        """
        return [
            Alias(self.plane, name="plane"),
            Alias(self.azimuth, name="azimuth"),
            Alias(self.elevation, name="elevation", prefix="/"),
            Alias(self.level, name="level", prefix="/"),
            Alias(
                self.refpoint,
                name="refpoint",
                sep="/",
                prefix={"mapcoords": "+w", "plotcoords": "+v"}[self.cstype],
                size={"mapcoords": {2, 3}, "plotcoords": 2}[self.cstype],
            ),
        ]
