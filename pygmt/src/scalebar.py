"""
scalebar - Add a scale bar.
"""

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


# ruff: noqa: ARG001
def scalebar(  # noqa: PLR0913
    self,
    position,
    length,
    label_alignment=None,
    scale_position=None,
    fancy=None,
    justify=None,
    label=None,
    offset=None,
    unit=None,
    vertical=None,
    box=None,
):
    """
    Add a scale bar.

    Parameters
    ----------
    TODO

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.scalebar(
    ...     "g10/10",
    ...     length=1000,
    ...     fancy=True,
    ...     label="Scale",
    ...     unit=True,
    ...     box=Box(pen=0.5, fill="lightblue"),
    ... )
    >>> fig.show()
    """
    alias = AliasSystem(
        L=[
            Alias("position", separator="/", value=position),
            Alias("length", prefix="+w", value=length),
            Alias("label_alignment", prefix="+a", value=label_alignment),
            Alias("scale_position", prefix="+c", separator="/", value=scale_position),
            Alias("fancy", prefix="+f", value=fancy),
            Alias("justify", prefix="+j", value=justify),
            Alias("label", prefix="+l", value=label),
            Alias("offset", prefix="+o", separator="/"),
            Alias("unit", prefix="+u"),
            Alias("vertical", prefix="+v"),
        ],
        F="box",
    )

    self._preprocess()
    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(alias.kwdict))
