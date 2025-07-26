"""
scalebar - Add a scale bar.
"""

from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def scalebar(  # noqa: PLR0913
    self,
    position,
    length,
    position_type: Literal[
        "user", "justify", "mirror", "normalize", "plot", None
    ] = None,
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
    self._preprocess()

    aliasdict = AliasSystem(
        L=[
            Alias(
                position_type,
                name="position_type",
                mapping={
                    "user": "g",
                    "justify": "j",
                    "mirror": "J",
                    "normalize": "n",
                    "plot": "x",
                },
            ),
            Alias(position, name="position", separator="/"),
            Alias(length, name="length", prefix="+w"),
            Alias(label_alignment, name="label_alignment", prefix="+a"),
            Alias(scale_position, name="scale_position", prefix="+c", separator="/"),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(label, name="label", prefix="+l"),
            Alias(offset, name="offset", prefix="+o", separator="/"),
            Alias(unit, name="unit", prefix="+u"),
            Alias(vertical, name="vertical", prefix="+v"),
        ],
        F=Alias(box, name="box"),
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
