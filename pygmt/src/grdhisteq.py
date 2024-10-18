"""
grdhisteq - Perform histogram equalization for a grid.
"""

from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)

__doctest_skip__ = ["grdhisteq.*"]


class grdhisteq:  # noqa: N801
    r"""
    Perform histogram equalization for a grid.

    Two common use cases of :class:`pygmt.grdhisteq` are to find data values
    that divide a grid into patches of equal area
    (:meth:`pygmt.grdhisteq.compute_bins`) or to write a grid with
    statistics based on some kind of cumulative distribution function
    (:meth:`pygmt.grdhisteq.equalize_grid`).

    Histogram equalization provides a way to highlight data that has most
    values clustered in a small portion of the dynamic range, such as a
    grid of flat topography with a mountain in the middle. Ordinary gray
    shading of this grid (using :meth:`pygmt.Figure.grdimage` or
    :meth:`pygmt.Figure.grdview`) with a linear mapping from topography to
    graytone will result in most of the image being very dark gray, with the
    mountain being almost white. :meth:`pygmt.grdhisteq.compute_bins` can
    provide a list of data values that divide the data range into divisions
    which have an equal area in the image [Default is 16 if ``divisions`` is
    not set]. The :class:`pandas.DataFrame` or ASCII file output can be used to
    make a colormap with :func:`pygmt.makecpt` and an image with
    :meth:`pygmt.Figure.grdimage` that has all levels of gray occurring
    equally.

    :meth:`pygmt.grdhisteq.equalize_grid` provides a way to write a grid with
    statistics based on a cumulative distribution function. In this
    application, the ``outgrid`` has relative highs and lows in the same
    (x,y) locations as the ``grid``, but the values are changed to reflect
    their place in the cumulative distribution.
    """

    @staticmethod
    @fmt_docstring
    @use_alias(
        C="divisions",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
        h="header",
    )
    @kwargs_to_strings(R="sequence")
    def equalize_grid(
        grid, outgrid: str | None = None, **kwargs
    ) -> xr.DataArray | None:
        r"""
        Perform histogram equalization for a grid.

        :meth:`pygmt.grdhisteq.equalize_grid` provides a way to write a grid
        with statistics based on a cumulative distribution function. The
        ``outgrid`` has relative highs and lows in the same (x,y) locations as
        the ``grid``, but the values are changed to reflect their place in the
        cumulative distribution.

        Full option list at :gmt-docs:`grdhisteq.html`

        {aliases}

        Parameters
        ----------
        {grid}
        {outgrid}
        divisions : int
            Set the number of divisions of the data range.
        gaussian : bool or int or float
            *norm*.
            Produce an output grid with standard normal scores using
            ``gaussian=True`` or force the scores to fall in the ±\ *norm*
            range.
        quadratic: bool
            Perform quadratic equalization [Default is linear].
        {region}
        {verbose}

        Returns
        -------
        ret
            Return type depends on the ``outgrid`` parameter:

            - xarray.DataArray if ``outgrid`` is None
            - None if ``outgrid`` is a str (grid output is stored in
              ``outgrid``)

        Example
        -------
        >>> import pygmt
        >>> # Load a grid of @earth_relief_30m data, with a longitude range
        >>> # of 10°E to 30°E, and a latitude range of 15°N to 25°N
        >>> grid = pygmt.datasets.load_earth_relief(
        ...     resolution="30m", region=[10, 30, 15, 25]
        ... )
        >>> # Create a new grid with a Gaussian data distribution
        >>> grid = pygmt.grdhisteq.equalize_grid(grid=grid, gaussian=True)

        See Also
        --------
        :func:`pygmt.grd2cpt`

        Note
        ----
        This method does a weighted histogram equalization for geographic
        grids to account for node area varying with latitude.
        """
        with Session() as lib:
            with (
                lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
                lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
            ):
                kwargs["G"] = voutgrd
                lib.call_module(
                    module="grdhisteq", args=build_arg_list(kwargs, infile=vingrd)
                )
                return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)

    @staticmethod
    @fmt_docstring
    @use_alias(
        C="divisions",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
        h="header",
    )
    @kwargs_to_strings(R="sequence")
    def compute_bins(
        grid,
        output_type: Literal["pandas", "numpy", "file"] = "pandas",
        outfile: str | None = None,
        **kwargs,
    ) -> pd.DataFrame | np.ndarray | None:
        r"""
        Perform histogram equalization for a grid.

        Histogram equalization provides a way to highlight data that has most
        values clustered in a small portion of the dynamic range, such as a
        grid of flat topography with a mountain in the middle. Ordinary gray
        shading of this grid (using :meth:`pygmt.Figure.grdimage` or
        :meth:`pygmt.Figure.grdview`) with a linear mapping from topography to
        graytone will result in most of the image being very dark gray, with
        the mountain being almost white. :meth:`pygmt.grdhisteq.compute_bins`
        can provide a list of data values that divide the data range into
        divisions which have an equal area in the image [Default is 16 if
        ``divisions`` is not set]. The :class:`pandas.DataFrame` or ASCII file
        output can be used to make a colormap with :func:`pygmt.makecpt` and an
        image with :meth:`pygmt.Figure.grdimage` that has all levels of gray
        occurring equally.

        Full option list at :gmt-docs:`grdhisteq.html`

        {aliases}

        Parameters
        ----------
        {grid}
        {output_type}
        {outfile}
        divisions : int
            Set the number of divisions of the data range.
        quadratic : bool
            Perform quadratic equalization [Default is linear].
        {region}
        {verbose}
        {header}

        Returns
        -------
        ret
            Return type depends on ``outfile`` and ``output_type``:

            - ``None`` if ``outfile`` is set (output will be stored in file set by
              ``outfile``)
            - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not
              set (depends on ``output_type``)

        Example
        -------
        >>> import pygmt
        >>> # Load a grid of @earth_relief_30m data, with a longitude range of
        >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
        >>> grid = pygmt.datasets.load_earth_relief(
        ...     resolution="30m", region=[10, 30, 15, 25]
        ... )
        >>> # Find elevation intervals that split the data range into 5
        >>> # divisions, each of which have an equal area in the original grid.
        >>> bins = pygmt.grdhisteq.compute_bins(grid=grid, divisions=5)
        >>> print(bins)
                start    stop
        bin_id
        0       183.5   395.0
        1       395.0   472.0
        2       472.0   575.0
        3       575.0   709.5
        4       709.5  1807.0

        See Also
        --------
        :func:`pygmt.grd2cpt`

        Note
        ----
        This method does a weighted histogram equalization for geographic
        grids to account for node area varying with latitude.
        """
        output_type = validate_output_table_type(output_type, outfile=outfile)

        if kwargs.get("h") is not None and output_type != "file":
            raise GMTInvalidInput("'header' is only allowed with output_type='file'.")

        with Session() as lib:
            with (
                lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
                lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
            ):
                kwargs["D"] = vouttbl  # -D for output file name
                lib.call_module(
                    module="grdhisteq", args=build_arg_list(kwargs, infile=vingrd)
                )

            return lib.virtualfile_to_dataset(
                vfname=vouttbl,
                output_type=output_type,
                column_names=["start", "stop", "bin_id"],
                dtype={
                    "start": np.float32,
                    "stop": np.float32,
                    "bin_id": np.uint32,
                },
                index_col="bin_id" if output_type == "pandas" else None,
            )
