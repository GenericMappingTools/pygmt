"""
grdhisteq - Perform histogram equalization for a grid.
"""

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)
from pygmt.io import load_dataarray

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
        G="outgrid",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
        h="header",
    )
    @kwargs_to_strings(R="sequence")
    def equalize_grid(grid, **kwargs):
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
        ret: xarray.DataArray or None
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
        with GMTTempFile(suffix=".nc") as tmpfile:
            with Session() as lib:
                with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
                    if (outgrid := kwargs.get("G")) is None:
                        kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                    lib.call_module(
                        module="grdhisteq", args=build_arg_string(kwargs, infile=vingrd)
                    )
            return load_dataarray(outgrid) if outgrid == tmpfile.name else None

    @staticmethod
    @fmt_docstring
    @use_alias(
        C="divisions",
        D="outfile",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
        h="header",
    )
    @kwargs_to_strings(R="sequence")
    def compute_bins(grid, output_type="pandas", **kwargs):
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
        outfile : str or bool or None
            The name of the output ASCII file to store the results of the
            histogram equalization in.
        output_type : str
            Determine the format the xyz data will be returned in [Default is
            ``pandas``]:

                - ``numpy`` - :class:`numpy.ndarray`
                - ``pandas``- :class:`pandas.DataFrame`
                - ``file`` - ASCII file (requires ``outfile``)
        divisions : int
            Set the number of divisions of the data range.
        quadratic : bool
            Perform quadratic equalization [Default is linear].
        {region}
        {verbose}
        {header}

        Returns
        -------
        ret : pandas.DataFrame or numpy.ndarray or None
            Return type depends on ``outfile`` and ``output_type``:

            - None if ``outfile`` is set (output will be stored in file set by
              ``outfile``)
            - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if
              ``outfile`` is not set (depends on ``output_type``)

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
        outfile = kwargs.get("D")
        output_type = validate_output_table_type(output_type, outfile=outfile)

        if kwargs.get("h") is not None and output_type != "file":
            raise GMTInvalidInput("'header' is only allowed with output_type='file'.")

        with GMTTempFile(suffix=".txt") as tmpfile:
            with Session() as lib:
                with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
                    if outfile is None:
                        kwargs["D"] = outfile = tmpfile.name  # output to tmpfile
                    lib.call_module(
                        module="grdhisteq", args=build_arg_string(kwargs, infile=vingrd)
                    )

            if outfile == tmpfile.name:
                # if user did not set outfile, return pd.DataFrame
                result = pd.read_csv(
                    filepath_or_buffer=outfile,
                    sep="\t",
                    header=None,
                    names=["start", "stop", "bin_id"],
                    dtype={
                        "start": np.float32,
                        "stop": np.float32,
                        "bin_id": np.uint32,
                    },
                )
            elif outfile != tmpfile.name:
                # return None if outfile set, output in outfile
                return None

            if output_type == "numpy":
                return result.to_numpy()

            return result.set_index("bin_id")
