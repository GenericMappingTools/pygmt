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
    inverted.

    GMT provides 90 predefined patterns that can be used in PyGMT. The patterns are
    numbered from 1 to 90, and shown below:

    .. figure:: https://docs.generic-mapping-tools.org/6.5/_images/GMT_App_E.png
       :alt: The 90 predefined bit-patterns provided with GMT
       :width: 75%
       :align: center

    Parameters
    ----------
    pattern
        The pattern to use. It can be specified in two forms:

        - An integer in the range of 1-90, corresponding to one of 90 predefined 64x64
          bit-patterns. [Default is 1].
        - Name of a 1-, 8-, or 24-bit image raster file, to create customized, repeating
          images using image raster files.
    dpi
        Resolution of the pattern in dots per inch (DPI) [Default is 300].
    bgcolor/fgcolor
        The background/foreground color for predefined bit-patterns or 1-bit images.
        Setting either to an empty string will yield a transparent background/foreground
        where only the foreground/background pixels will be painted. [Default is white
        for background and black for foreground].
    invert
        If ``True``, the pattern will be bit-inverted, i.e., white and black areas will
        be interchanged (only applies to predefined bit-patterns or 1-bit images).

    Examples
    --------
    Draw a global map with land areas filled with pattern 15 in a light red background
    and 200 dpi resolution:

    >>> import pygmt
    >>> from pygmt.params import Pattern
    >>> fig = pygmt.Figure()
    >>> fig.coast(
    ...     region="g",
    ...     projection="H10c",
    ...     frame=True,
    ...     land=Pattern(15, bgcolor="lightred", dpi=200),
    ...     shorelines=True,
    ... )
    >>> fig.show()
    """

    pattern: int | PathLike = 1
    dpi: int | None = None
    bgcolor: str | None = None
    fgcolor: str | None = None
    invert: bool = False

    def _validate(self):
        """
        Validate the parameters.
        """
        # Integer pattern number must be in the range 1-90.
        if not (
            isinstance(self.pattern, PathLike)
            or (isinstance(self.pattern, int) and 1 <= self.pattern <= 90)
        ):
            raise GMTValueError(
                self.pattern,
                description="pattern number",
                reason=(
                    "Parameter 'pattern' must be an integer in the range 1-90 "
                    "or the name of a 1-, 8-, or 24-bit image raster file."
                ),
            )
        # fgcolor and bgcolor cannot both be empty.
        if self.fgcolor == "" and self.bgcolor == "":
            _value = f"{self.fgcolor=}, {self.bgcolor=}"
            raise GMTValueError(
                _value,
                description="fgcolor and bgcolor",
                reason="fgcolor and bgcolor cannot both be empty.",
            )

    @property
    def _aliases(self):
        """
        Aliases for the Pattern class.
        """
        return [
            Alias(self.pattern, name="pattern", prefix="P" if self.invert else "p"),
            Alias(self.bgcolor, name="bgcolor", prefix="+b"),
            Alias(self.fgcolor, name="fgcolor", prefix="+f"),
            Alias(self.dpi, name="dpi", prefix="+r"),
        ]
