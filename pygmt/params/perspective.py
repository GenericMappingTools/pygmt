"""
The Perspective class for setting perspective view.
"""

import dataclasses
from typing import Literal

from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Perspective(BaseParam):
    """
    Class for setting perspective view.

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Perspective
    >>> fig = pygmt.Figure()
    >>> fig.basemap(
    ...     region=[0, 10, 0, 10, 0, 20],
    ...     projection="X3c",
    ...     zsize="3c",
    ...     frame=["xafg", "yafg", "zafg", "wSEnZ"],
    ...     perspective=Perspective(azimuth=135, elevation=40, level=10),
    ... )
    >>> fig.show()
    """

    #: Azimuth of the viewpoint in degrees. Default is 180.0 (looking from south to
    #: north).
    azimuth: float | None = None

    #: Elevation angle of the viewpoint in degrees. Default is 90.0 (looking straight
    #: down at nadir).
    elevation: float | None = None

    #: The level at which all 2-D material, like the plot frame, is plotted. Only valid
    #: when used together with parameters ``zsize``/``zscale``. Default is at the bottom
    #: of the z-axis.
    level: float | None = None

    #: Set which constant-coordinate plane is used as the plotting plane. Use ``"x"``
    #: for the x-plane, ``"y"`` for the y-plane, or ``"z"`` for the horizontal z-plane
    # [Default is ``"z"``].
    plane: Literal["x", "y", "z"] | None = None

    def __post_init__(self):
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
                self.plane, description="plane", choices=["x", "y", "z"]
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
        ]
