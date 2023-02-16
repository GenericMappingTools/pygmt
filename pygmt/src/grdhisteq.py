"""
grdhisteq - Perform histogram equalization for a grid.
"""
import warnings

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
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdhisteq.*"]


class grdhisteq:  # pylint: disable=invalid-name
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
        D="outfile",
        G="outgrid",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
        h="header",
    )
    @kwargs_to_strings(R="sequence")
    def _grdhisteq(grid, output_type, **kwargs):
        r"""
        Perform histogram equalization for a grid.

        Must provide ``outfile`` or ``outgrid``.

        Full option list at :gmt-docs:`grdhisteq.html`

        {aliases}

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.
        outgrid : str or bool or None
            The name of the output netCDF file with extension .nc to store the
            grid in.
        outfile : str or bool or None
            The name of the output ASCII file to store the results of the
            histogram equalization in.
        output_type: str
            Determines the output type. Use "file", "xarray", "pandas", or
            "numpy".
        divisions : int
            Set the number of divisions of the data range [Default is 16].

        {region}
        {verbose}
        {header}

        Returns
        -------
        ret: pandas.DataFrame or xarray.DataArray or None
            Return type depends on whether the ``outgrid`` parameter is set:

            - xarray.DataArray if ``output_type`` is "xarray""
            - numpy.ndarray if ``output_type`` is "numpy"
            - pandas.DataFrame if ``output_type`` is "pandas"
            - None if ``output_type`` is "file" (output is stored in
              ``outgrid`` or ``outfile``)

        See Also
        -------
        :func:`pygmt.grd2cpt`
        """

        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                lib.call_module(
                    module="grdhisteq", args=build_arg_string(kwargs, infile=infile)
                )

        if output_type == "file":
            return None
        if output_type == "xarray":
            return load_dataarray(kwargs["G"])

        result = pd.read_csv(
            filepath_or_buffer=kwargs["D"],
            sep="\t",
            header=None,
            names=["start", "stop", "bin_id"],
            dtype={
                "start": np.float32,
                "stop": np.float32,
                "bin_id": np.uint32,
            },
        )
        if output_type == "numpy":
            return result.to_numpy()

        return result.set_index("bin_id")

    @staticmethod
    @fmt_docstring
    def equalize_grid(
        grid,
        *,
        outgrid=None,
        divisions=None,
        region=None,
        gaussian=None,
        quadratic=None,
        verbose=None,
    ):
        r"""
        Perform histogram equalization for a grid.

        :meth:`pygmt.grdhisteq.equalize_grid` provides a way to write a grid
        with statistics based on a cumulative distribution function. The
        ``outgrid`` has relative highs and lows in the same (x,y) locations as
        the ``grid``, but the values are changed to reflect their place in the
        cumulative distribution.

        Full option list at :gmt-docs:`grdhisteq.html`

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.
        outgrid : str or None
            The name of the output netCDF file with extension .nc to store the
            grid in.
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
        >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to
        >>> # 30, and a y-range of 15 to 25
        >>> grid = pygmt.datasets.load_earth_relief(
        ...     resolution="30m", region=[10, 30, 15, 25]
        ... )
        >>> # Create a new grid with a Gaussian data distribution
        >>> grid = pygmt.grdhisteq.equalize_grid(grid=grid, gaussian=True)

        See Also
        -------
        :func:`pygmt.grd2cpt`

        Note
        ----
        This method does a weighted histogram equalization for geographic
        grids to account for node area varying with latitude.
        """
        # Return an xarray.DataArray if ``outgrid`` is not set
        with GMTTempFile(suffix=".nc") as tmpfile:
            if isinstance(outgrid, str):
                output_type = "file"
            elif outgrid is None:
                output_type = "xarray"
                outgrid = tmpfile.name
            else:
                raise GMTInvalidInput("Must specify 'outgrid' as a string or None.")
            return grdhisteq._grdhisteq(
                grid=grid,
                output_type=output_type,
                outgrid=outgrid,
                divisions=divisions,
                region=region,
                gaussian=gaussian,
                quadratic=quadratic,
                verbose=verbose,
            )

    @staticmethod
    @fmt_docstring
    def compute_bins(
        grid,
        *,
        output_type="pandas",
        outfile=None,
        divisions=None,
        quadratic=None,
        verbose=None,
        region=None,
        header=None,
    ):
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

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.
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
        >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to
        >>> # 30, and a y-range of 15 to 25
        >>> grid = pygmt.datasets.load_earth_relief(
        ...     resolution="30m", region=[10, 30, 15, 25]
        ... )
        >>> # Find elevation intervals that splits the data range into 5
        >>> # divisions, each of which have an equal area in the original grid.
        >>> bins = pygmt.grdhisteq.compute_bins(grid=grid, divisions=5)
        >>> print(bins)
                start    stop
        bin_id
        0       170.0   389.0
        1       389.0   470.5
        2       470.5   571.0
        3       571.0   705.0
        4       705.0  2275.5

        See Also
        -------
        :func:`pygmt.grd2cpt`

        Note
        ----
        This method does a weighted histogram equalization for geographic
        grids to account for node area varying with latitude.
        """
        # Return a pandas.DataFrame if ``outfile`` is not set
        if output_type not in ["numpy", "pandas", "file"]:
            raise GMTInvalidInput(
                "Must specify 'output_type' either as 'numpy', 'pandas' or 'file'."
            )

        if header is not None and output_type != "file":
            raise GMTInvalidInput("'header' is only allowed with output_type='file'.")

        if isinstance(outfile, str) and output_type != "file":
            msg = (
                f"Changing 'output_type' from '{output_type}' to 'file' "
                "since 'outfile' parameter is set. Please use output_type='file' "
                "to silence this warning."
            )
            warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
            output_type = "file"
        with GMTTempFile(suffix=".txt") as tmpfile:
            if output_type != "file":
                outfile = tmpfile.name
            return grdhisteq._grdhisteq(
                grid,
                output_type=output_type,
                outfile=outfile,
                divisions=divisions,
                quadratic=quadratic,
                verbose=verbose,
                region=region,
                header=header,
            )
