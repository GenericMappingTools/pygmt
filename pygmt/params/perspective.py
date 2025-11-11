"""
The Perspective class for setting perspective view.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias
from pygmt.exceptions import GMTInvalidInput
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Perspective(BaseParam):
    """
    Class for setting perspective view.
    """

    #: Azimuth of the viewpoint in degress. Default is 180.0 (looking from south to
    #: north).
    azimuth: float

    #: Elevation angle of the viewpoint in degrees. Default is 90.0 (looking from
    #: directly above).
    elevation: float | None = None

    #: The z-level at which all 2D material, like the plot frame, is plotted (only valid
    #: when used in consort with ``zsize``/``zscale`` [Default is at the bottom of the
    #: z-axis].
    zlevel: float | None = None

    #: The plane to plot against the “wall” x = level (using x) or y = level (using y)
    #: or the horizontal plain (using z) [default is z].
    plane: Literal["x", "y", "z"] | None = None

    #: For frames used for animation, the center of the data domain is fixed. Specify
    #: another center using one of the following parameters:

    #: (*lon0*, *lat0*) or (*lon0*, *lat0*, *z0*).
    #: Project the specified coordinate to the center of the page size.
    center: Sequence[float] | None = None

    #: (*x0*, *y0*). Specify the center in the projected coordinate system.
    viewpoint: Sequence[float] | None = None

    def __post_init__(self):
        """
        Post-initialization processing to validate parameters.
        """
        if self.center is not None and self.viewpoint is not None:
            msg = "Parameters 'center' and 'viewpoint' are mutually exclusive."
            raise GMTInvalidInput(msg)

    @property
    def _aliases(self):
        """
        Aliases for the parameters.
        """
        return [
            Alias(self.plane, name="plane"),
            Alias(self.azimuth, name="azimuth"),
            Alias(self.elevation, name="elevation", prefix="/"),
            Alias(self.zlevel, name="zlevel", prefix="/"),
            Alias(self.center, name="center", prefix="+w", sep="/", size={2, 3}),
            Alias(self.viewpoint, name="viewpoint", prefix="+v", sep="/", size=2),
        ]
