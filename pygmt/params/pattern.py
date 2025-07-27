"""
The Pattern class for specifying GMT filling patterns.
"""

import dataclasses

from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Pattern(BaseParam):
    """

    Examples
    --------
    >>> from pygmt.params import Pattern
    >>> str(Pattern(id=1))
    'p1'
    >>> str(Pattern(id=1, bgcolor="red", fgcolor="blue"))
    'p1+bred+fblue'
    >>> str(Pattern(id=1, bgcolor="red", fgcolor="blue", dpi=300))
    'p1+bred+fblue+r300'
    >>> str(Pattern(id="my_pattern.png"))
    'pmy_pattern.png'
    >>> str(Pattern(id=2, reversed=True))
    'P2'
    >>> str(Pattern(id=100))
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid pattern id: 100...
    """

    id: int | str
    reversed: bool = False
    bgcolor: str | None = None
    fgcolor: str | None = None
    dpi: int | None = None

    def __post_init__(self):
        """
        Validate the id and set the reversed flag.
        """
        if isinstance(self.id, int) and not (1 <= self.id <= 90):
            raise GMTValueError(
                self.id,
                description="pattern id",
                reason=(
                    "Pattern id must be an integer in the range 1-90 "
                    "or the name of a 1-, 8-, or 24-bit image raster file"
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
