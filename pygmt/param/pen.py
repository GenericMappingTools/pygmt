"""
Define the Pen class for specifying pen attributes (width, color, style).
"""
from dataclasses import dataclass


@dataclass
class Pen:
    """
    A GMT pen specified from three attributes: *width*, *color* and *style*.

    See also :gmt-docs:`cookbook/features.html#specifying-pen-attributes`
    """

    width: str = None
    color: str = None
    style: str = None

    def __str__(self):
        return ",".join(
            str(attr or "") for attr in (self.width, self.color, self.style)
        )
