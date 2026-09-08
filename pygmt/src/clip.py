"""
clip - Clip plotting to selected areas.
"""

from collections.abc import Sequence
from contextlib import contextmanager
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import (
    _validate_data_input,
    build_arg_list,
    fmt_docstring,
    sequence_join,
)
from pygmt.params import Axis, Frame


def _call_module(module, kwargs=None, *, data=None, x=None, y=None):
    """
    Call a GMT module with optional tabular input.
    """
    with Session() as lib:
        if data is not None or (x is not None and y is not None):
            with lib.virtualfile_in(data=data, x=x, y=y) as vintbl:
                lib.call_module(
                    module=module,
                    args=build_arg_list(kwargs, infile=vintbl),
                )
        else:
            lib.call_module(module=module, args=build_arg_list(kwargs))


@contextmanager
def _clip_context(figure, activate, deactivate):
    """
    Context manager to activate and deactivate clipping for a figure.
    """
    figure._activate_figure()
    activate()

    try:
        yield
    finally:
        figure._activate_figure()
        deactivate()


def _reject_kwargs(method: str, kwargs: dict, names: Sequence[str]) -> None:
    """
    Raise an error when users pass parameters owned by a clip helper.
    """
    invalid = sorted(set(kwargs) & set(names))
    if invalid:
        raise GMTParameterError(
            reason=(
                f"Figure.{method} does not support parameter(s) "
                f"{', '.join(repr(name) for name in invalid)}."
            )
        )


def clip_land(self, **kwargs):
    """
    Clip plotting to land areas.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the land areas.

    Parameters
    ----------
    kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
        Parameters ``land`` and ``G`` are not allowed here because they are set
        internally to activate land clipping. See :meth:`pygmt.Figure.coast` for the
        full parameter documentation.

    Examples
    --------
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="W15c", frame=True)
    >>> with fig.clip_land():
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    _reject_kwargs("clip_land", kwargs, ["land", "G"])
    return _clip_context(
        self,
        activate=lambda: self.coast(land=True, **kwargs),
        deactivate=lambda: self.coast(Q=True),
    )


def clip_water(self, **kwargs):
    """
    Clip plotting to water areas.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the water areas.

    Parameters
    ----------
    kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
        Parameters ``water`` and ``S`` are not allowed here because they are set
        internally to activate water clipping. See :meth:`pygmt.Figure.coast` for the
        full parameter documentation.

    Examples
    --------
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="W15c", frame=True)
    >>> with fig.clip_water():
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    _reject_kwargs("clip_water", kwargs, ["water", "S"])
    return _clip_context(
        self,
        activate=lambda: self.coast(water=True, **kwargs),
        deactivate=lambda: self.coast(Q=True),
    )


def clip_dcw(self, code: str | Sequence[str], **kwargs):
    """
    Clip plotting to Digital Chart of the World polygons.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the regions defined by the Digital Chart of the World
    codes.

    Parameters
    ----------
    code
        The Digital Chart of the World codes of the regions to clip to.
    kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
        Parameters ``dcw`` and ``E`` are not allowed here because they are set
        internally to activate clipping. See :meth:`pygmt.Figure.coast` for the full
        parameter documentation.

    Examples
    --------
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="W15c", frame=True)
    >>> with fig.clip_dcw(code="JP"):
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    _reject_kwargs("clip_dcw", kwargs, ["dcw", "E"])
    codes = sequence_join(code, sep=",")
    return _clip_context(
        self,
        activate=lambda: self.coast(E=f"{codes}+c", **kwargs),
        deactivate=lambda: self.coast(Q=True),
    )


def clip_solar(self, invert: bool = False, **kwargs):
    """
    Clip plotting to the solar terminator.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the solar terminator.

    Parameters
    ----------
    invert
        Invert the sense of what is inside and outside the terminator.
    kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.solar`.
        Parameters ``fill``, ``G``, ``frame``, and ``B`` are not allowed here because
        they are controlled internally to activate clipping. See
        :meth:`pygmt.Figure.solar` for the full parameter documentation.

    Examples
    --------
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="W15c", frame=True)
    >>> with fig.clip_solar(terminator="civil"):
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    _reject_kwargs("clip_solar", kwargs, ["fill", "G", "frame", "B"])
    kwargs = kwargs | {"fill": True, "N": invert}
    return _clip_context(
        self,
        activate=lambda: self.solar(**kwargs),
        deactivate=lambda: _call_module("clip", {"C": True}),
    )


@fmt_docstring
def clip_polygon(
    self,
    data=None,
    x=None,
    y=None,
    region: Sequence[float | str] | str | None = None,
    projection: str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    straight_line: bool | Literal["x", "y"] = False,
    invert: bool = False,
    pen: str | None = None,
    **kwargs,
):
    """
    Clip plotting to polygonal paths.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the polygons.

    **Aliases**

    .. hlist::
       :columns: 3

       - A = straight_line
       - B = frame
       - J = projection
       - N = invert
       - R = region
       - V = verbose
       - W = pen

    Parameters
    ----------
    data
        Either a file name to an ASCII data table, a 2-D {table-classes}.
    x/y
        X and Y coordinates of the polygon.
    straight_line
        Control how line segments are connected.
    invert
        Invert the sense of what is inside and outside.
    pen
        Draw outline of clip path using given pen attributes before clipping is
        initiated.
    kwargs
        Additional keyword arguments passed to the GMT ``clip`` module. See
        :gmt-docs:`clip.html` for the full parameter documentation.

    Examples
    --------
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="W15c", frame=True)
    >>> with fig.clip_polygon(x=[-10, 10, 10, -10], y=[-10, -10, 10, 10]):
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    aliasdict = AliasSystem(
        A=Alias(straight_line, name="straight_line"),
        N=Alias(invert, name="invert"),
        W=Alias(pen, name="pen"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)
    _validate_data_input(data=data, x=x, y=y)
    return _clip_context(
        self,
        activate=lambda: _call_module("clip", aliasdict, data=data, x=x, y=y),
        deactivate=lambda: _call_module("clip", {"C": True}),
    )


@fmt_docstring
def clip_mask(
    self,
    data=None,
    x=None,
    y=None,
    region: Sequence[float | str] | str | None = None,
    spacing=None,
    invert: bool = False,
    radius=None,
    **kwargs,
):
    """
    Clip plotting to a mask.

    Must be used as a context manager. Any plotting operations within the context
    manager will be clipped to the mask.

    **Aliases**

    .. hlist::
       :columns: 3

       - I = spacing
       - N = invert
       - R = region
       - S = radius

    Parameters
    ----------
    data
        Either a file name to an ASCII data table, a 2-D {table-classes}.
    x/y
        X and Y coordinates of the mask.
    spacing
        The mask spacing passed to the GMT ``mask`` module.
    invert
        Invert the sense of what is inside and outside.
    radius
        Set the search radius passed to the GMT ``mask`` module.
    kwargs
        Additional keyword arguments passed to the GMT ``mask`` module. See
        :gmt-docs:`mask.html` for the full parameter documentation.

    Examples
    --------
    >>> import numpy as np
    >>> import pygmt
    >>>
    >>> grid = pygmt.datasets.load_earth_relief()
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="g", projection="Q15c", frame=True)
    >>> with fig.clip_mask(
    ...     x=[180] * 16, y=np.arange(-80, 80, 10), spacing="30m", radius="5d"
    ... ):
    ...     fig.grdimage(grid, cmap="geo")
    >>> fig.show()
    """
    aliasdict = AliasSystem(
        I=Alias(spacing, name="spacing"),
        N=Alias(invert, name="invert"),
        S=Alias(radius, name="radius"),
    ).add_common(
        R=region,
    )
    aliasdict.merge(kwargs)
    _validate_data_input(data=data, x=x, y=y)
    return _clip_context(
        self,
        activate=lambda: _call_module("mask", aliasdict, data=data, x=x, y=y),
        deactivate=lambda: _call_module("mask", {"C": True}),
    )
