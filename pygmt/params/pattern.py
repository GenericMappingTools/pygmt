"""
The Pattern class for specifying bit and hachure patterns.
"""

import dataclasses

from pygmt._typing import PathLike
from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam

__doctest_skip__ = ["Pattern"]


@dataclasses.dataclass(repr=False)
class Pattern(BaseParam):
    """
    Class for specifying bit and hachure patterns.

    This class allows users to specify predefined bit-patterns or custom 1-, 8-, or
    24-bit image raster files to fill symbols and polygons in various PyGMT plotting
    methods. The patterns can be customized with different resolution and different
    foreground and background colors. The foreground and background colors can also be
    reversed.

    GMT provides 90 predefined patterns that can be used in PyGMT. The patterns are
    numbered from 1 to 90, and shown below:

    .. figure:: https://docs.generic-mapping-tools.org/6.5/_images/GMT_App_E.png
       :alt: The 90 predefined bit-patterns provided with GMT
       :width: 75%
       :align: center

    Parameters
    ----------
    id
        The pattern ID. It can be specified in two forms:

        - An integer in the range of 1-90, corresponding to one of 90 predefined 64x64
          bit-patterns
        - Name of a 1-, 8-, or 24-bit image raster file, to create customized, repeating
          images using image raster files.
    dpi
        Resolution of the pattern in dots per inch (DPI) [Default is 1200].
    bgcolor/fgcolor
        The background/foreground color for predefined bit-patterns or 1-bit images.
        [Default is white for background and black for foreground]. Setting either to
        an empty string will yield a transparent background/foreground where only the
        foreground or background pixels will be painted.
    reversed
        If True, the pattern will be bit-reversed, i.e., white and black areas will be
        interchanged (only applies to predefined bit-patterns or 1-bit images).

    Examples
    --------
    Draw a global map with land areas filled with pattern 15 in a light red background
    and 300 dpi resolution:

    >>> import pygmt
    >>> from pygmt.params import Pattern
    >>> fig = pygmt.Figure()
    >>> fig.coast(
    ...     region="g",
    ...     projection="H10c",
    ...     frame=True,
    ...     land=Pattern(15, bgcolor="lightred", dpi=300),
    ...     shorelines=True,
    ... )
    >>> fig.show()
    """

    id: int | PathLike
    dpi: int | None = None
    bgcolor: str | None = None
    fgcolor: str | None = None
    reversed: bool = False

    def _validate(self):
        """
        Validate the parameters.
        """
        # Integer pattern id must be in the range 1-90.
        if isinstance(self.id, int) and not (1 <= self.id <= 90):
            raise GMTValueError(
                self.id,
                description="pattern id",
                reason=(
                    "Pattern id must be an integer in the range 1-90 "
                    "or the name of a 1-, 8-, or 24-bit image raster file."
                ),
            )

    @property
    def _aliases(self):
        """
        Aliases for the Pattern class.
        """
        return [
            Alias(self.id, name="id", prefix="P" if self.reversed else "p"),
            Alias(self.bgcolor, name="bgcolor", prefix="+b"),
            Alias(self.fgcolor, name="fgcolor", prefix="+f"),
            Alias(self.dpi, name="dpi", prefix="+r"),
        ]
