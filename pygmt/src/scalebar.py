"""
scalebar - Add a scale bar.
"""

from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


# ruff: noqa: ARG001
def scalebar(  # noqa: PLR0913
    self,
    position,
    length,
    position_type: Literal["g", "j", "J", "n", "x"] = "g",
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
    ...     position=(10, 10),
    ...     position_type="g",
    ...     length=1000,
    ...     fancy=True,
    ...     label="Scale",
    ...     unit=True,
    ...     box=Box(pen=0.5, fill="lightblue"),
    ... )
    >>> fig.show()
    """
    kwdict = AliasSystem(
        L=[
            Alias(position, separator="/", prefix=position_type),
            Alias(length, prefix="+w"),
            Alias(label_alignment, prefix="+a"),
            Alias(scale_position, prefix="+c", separator="/"),
            Alias(fancy, prefix="+f"),
            Alias(justify, prefix="+j"),
            Alias(label, prefix="+l"),
            Alias(offset, prefix="+o", separator="/"),
            Alias(unit, prefix="+u"),
            Alias(vertical, prefix="+v"),
        ],
        F=Alias(box),
    ).kwdict

    self._preprocess()
    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(kwdict))
