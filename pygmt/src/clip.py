"""
clip - Clip a path and only plot data inside or outside.
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
    is_nonstr_iter,
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
    # Activate the clipping context.
    figure._activate_figure()
    activate()

    try:
        yield
    finally:
        # Deactivate the clipping context.
        figure._activate_figure()
        deactivate()


class ClipAccessor:
    """
    Accessor for different clip methods.
    """

    def __init__(self, figure):
        """
        Initialize the ClipAccessor.
        """
        self._figure = figure  # The parent Figure object.

    # @staticmethod
    # def _validate_disallowed_parameters(parameters, kwargs, *, aliases=()):
    #     """
    #     Reject parameters that are incompatible with a clipping accessor method.
    #     """
    #     disallowed_parameters = set(parameters) | set(aliases)
    #     disallowed = [
    #         parameter for parameter in kwargs if parameter in disallowed_parameters
    #     ]
    #     if disallowed:
    #         names = ", ".join(repr(parameter) for parameter in disallowed)
    #         raise GMTParameterError(
    #             reason=f"Figure.clip does not support the parameter(s) {names} here."
    #         )

    # def land(self, **kwargs):
    #     """
    #     Clip the land area (i.e., "dry" areas) and only plot data inside.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the land areas.

    #     Parameters
    #     ----------
    #     kwargs
    #         Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
    #         See :meth:`pygmt.Figure.coast` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="W15c", frame=True)
    #     >>> with fig.clip.land():
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: self._figure.coast(land=True, **kwargs),
    #         deactivate=lambda: self._figure.coast(Q=True),
    #     )

    # def water(self, **kwargs):
    #     """
    #     Clip the water areas (i.e., "wet" areas such as oceans and lakes) and only plot
    #     data inside.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the water areas.

    #     Parameters
    #     ----------
    #     kwargs
    #         Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
    #         See :meth:`pygmt.Figure.coast` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="W15c", frame=True)
    #     >>> with fig.clip.water():
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: self._figure.coast(water=True, **kwargs),
    #         deactivate=lambda: self._figure.coast(Q=True),
    #     )

    # def dcw(self, code: str | Sequence[str], **kwargs):
    #     """
    #     Clip based on the Digital Chart of the World.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the region defined by the codes.

    #     Parameters
    #     ----------
    #     code
    #         The Digital Chart of the World codes of the region to clip to.
    #     kwargs
    #         Additional keyword arguments passed to :meth:`pygmt.Figure.coast`.
    #         See :meth:`pygmt.Figure.coast` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="W15c", frame=True)
    #     >>> with fig.clip.dcw(code="JP"):
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     self._validate_disallowed_parameters({"dcw"}, kwargs, aliases=("E",))
    #     _code = ",".join(code) if is_nonstr_iter(code) else code
    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: self._figure.coast(dcw=f"{_code}+c", **kwargs),
    #         deactivate=lambda: self._figure.coast(Q=True),
    #     )

    # def solar(self, invert: bool = False, **kwargs):
    #     """
    #     Clip the data to the solar terminator.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the solar terminator.

    #     Parameters
    #     ----------
    #     invert
    #         Invert the sense of what is inside and outside the terminator.
    #     kwargs
    #         Additional keyword arguments passed to :meth:`pygmt.Figure.solar`.
    #         Parameters ``frame`` and ``fill`` are not allowed here. See
    #         :meth:`pygmt.Figure.solar` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="W15c", frame=True)
    #     >>> with fig.clip.solar(terminator="civil"):
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     self._validate_disallowed_parameters(
    #         {"fill", "frame"}, kwargs, aliases=("B", "G")
    #     )
    #     solar_kwargs = kwargs.copy()
    #     if invert:
    #         solar_kwargs["N"] = True
    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: self._figure.solar(fill=True, **solar_kwargs),
    #         deactivate=lambda: _call_module("clip", {"C": True}),
    #     )

    # @fmt_docstring
    # def polygon(
    #     self,
    #     data=None,
    #     x=None,
    #     y=None,
    #     region: Sequence[float | str] | str | None = None,
    #     projection: str | None = None,
    #     frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    #     verbose: Literal[
    #         "quiet", "error", "warning", "timing", "info", "compat", "debug"
    #     ]
    #     | bool = False,
    #     straight_line: bool | Literal["x", "y"] = False,
    #     invert: bool = False,
    #     pen: str | None = None,
    #     **kwargs,
    # ):
    #     """
    #     Clip polygonal paths.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the polygons.

    #     **Aliases**
    #     .. hlist::
    #        :columns: 3

    #        - A = straight_line
    #        - B = frame
    #        - J = projection
    #        - N = invert
    #        - R = region
    #        - V = verbose
    #        - W = pen

    #     Parameters
    #     ----------
    #     data
    #         Either a file name to an ASCII data table, a 2-D {table-classes}.
    #     x/y
    #         X and Y coordinates of the polygon.
    #     straight_line
    #         Control how line segments are connected.
    #     invert
    #         Invert the sense of what is inside and outside.
    #     pen
    #         Draw outline of clip path using given pen attributes before clipping is
    #         initiated.
    #     kwargs
    #         Additional keyword arguments passed to the GMT ``clip`` module.
    #         See :gmt-docs:`clip.html` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="W15c", frame=True)
    #     >>> with fig.clip.polygon(x=[-10, 10, 10, -10], y=[-10, -10, 10, 10]):
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     aliasdict = AliasSystem(
    #         A=Alias(straight_line, name="straight_line"),
    #         N=Alias(invert, name="invert"),
    #         W=Alias(pen, name="pen"),
    #     ).add_common(
    #         B=frame,
    #         J=projection,
    #         R=region,
    #         V=verbose,
    #     )
    #     aliasdict.merge(kwargs)
    #     _validate_data_input(data=data, x=x, y=y)

    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: _call_module("clip", aliasdict, data=data, x=x, y=y),
    #         deactivate=lambda: _call_module("clip", {"C": True}),
    #     )

    # @fmt_docstring
    # def mask(
    #     self,
    #     data=None,
    #     x=None,
    #     y=None,
    #     region=None,
    #     spacing=None,
    #     invert: bool = False,
    #     radius=None,
    #     **kwargs,
    # ):
    #     """
    #     Clip the data to a mask.

    #     Must be used as a context manager. Any plotting operations within the context
    #     manager will be clipped to the mask.

    #     **Aliases**
    #     .. hlist::
    #        :columns: 3

    #        - I = spacing
    #        - N = invert
    #        - R = region
    #        - S = radius

    #     Parameters
    #     ----------
    #     data
    #         Either a file name to an ASCII data table, a 2-D {table-classes}.
    #     x/y
    #         X and Y coordinates of the mask.
    #     spacing
    #         The mask spacing passed to the GMT ``mask`` module.
    #     invert
    #         Invert the sense of what is inside and outside.
    #     radius
    #         Set the search radius passed to the GMT ``mask`` module.
    #     kwargs
    #         Additional keyword arguments passed to the GMT ``mask`` module.
    #         See :gmt-docs:`mask.html` for the full parameter documentation.

    #     Examples
    #     --------
    #     >>> import numpy as np
    #     >>> from pygmt import Figure
    #     >>> from pygmt.datasets import load_earth_relief
    #     >>>
    #     >>> grid = load_earth_relief()
    #     >>> fig = Figure()
    #     >>> fig.basemap(region="g", projection="Q15c", frame=True)
    #     >>> with fig.clip.mask(
    #     ...     x=[180] * 16, y=np.arange(-80, 80, 10), spacing="30m", radius="5d"
    #     ... ):
    #     ...     fig.grdimage(grid, cmap="geo")
    #     >>> fig.show()
    #     """
    #     aliasdict = AliasSystem(
    #         I=Alias(spacing, name="spacing"),
    #         N=Alias(invert, name="invert"),
    #         S=Alias(radius, name="radius"),
    #     ).add_common(
    #         R=region,
    #     )
    #     aliasdict.merge(kwargs)
    #     _validate_data_input(data=data, x=x, y=y)

    #     return _clip_context(
    #         self._figure,
    #         activate=lambda: _call_module("mask", aliasdict, data=data, x=x, y=y),
    #         deactivate=lambda: _call_module("mask", {"C": True}),
    #     )
