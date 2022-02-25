"""
grdhisteq - Perform histogram equalization for a grid.
"""
import warnings

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


class grdhisteq:  # pylint: disable=invalid-name
    r"""
    Perform histogram equalization for a grid.

    Two common use cases of :meth:`pygmt.grdhisteq` are to find data values
    that divide a grid into patches of equal area using
    :meth:`pygmt.grdhisteq.equalize_grid` or to write a grid with
    statistics based on some kind of cumulative distribution function using
    :meth:`pygmt.grdhisteq.compute_bins`.

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
    make a colormap with :meth:`pygmt.makecpt` and an image with
    :meth:`pygmt.Figure.grdimage` that has all levels of gray occuring
    equally.

    :meth:`pygmt.grdhisteq.equalize_grid` provides a way to write a grid with
    statistics based on a cumulative distribution function. In this
    application, the ``outgrid`` has relative highs and lows in the same
    (x,y) locations as the ``grid``, but the values are changed to reflect
    their place in the cumulative distribution.
    """

    @staticmethod
    def _grdhisteq(grid, output_type=None, tmpfile=None, **kwargs):
        r"""
        Perform histogram equalization for a grid.

        Two common use cases of :meth:`pygmt.grdhisteq` are to find data values
        that divide a grid into patches of equal area or to write a grid with
        statistics based on some kind of cumulative distribution function.

        Histogram equalization provides a way to highlight data that has most
        values clustered in a small portion of the dynamic range, such as a
        grid of flat topography with a mountain in the middle. Ordinary gray
        shading of this grid (using :meth:`pygmt.Figure.grdimage` or
        :meth:`pygmt.Figure.grdview`) with a linear mapping from topography to
        graytone will result in most of the image being very dark gray, with
        the mountain being almost white. :meth:`pygmt.grdhisteq` can provide a
        list of data values that divide the data range into divisions which
        have an equal area in the image [Default is 16 if ``divisions`` is not
        set]. The :class:`pandas.DataFrame` or ASCII file output can be used to
        make a colormap with :meth:`pygmt.makecpt` and an image with
        :meth:`pygmt.Figure.grdimage` that has all levels of gray occuring
        equally.

        :meth:`pygmt.grdhisteq` also provides a way to write a grid with
        statistics based on a cumulative distribution function. In this
        application, the ``outgrid`` has relative highs and lows in the same
        (x,y) locations as the ``grid``, but the values are changed to reflect
        their place in the cumulative distribution.

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
            histogram equalization in. Not allowed if ``outgrid`` is used.
        divisions : int
            Set the number of divisions of the data range.

        {R}
        {V}

        Returns
        -------
        ret: pandas.DataFrame or xarray.DataArray or None
            Return type depends on whether the ``outgrid`` parameter is set:

            - pandas.DataFrame if ``outfile`` is True
            - xarray.DataArray if ``outgrid`` is True
            - None if ``outgrid`` is a str (grid output is stored in
              ``outgrid``)
            - None if ``outfile`` is a str (file output is stored in
              ``outfile``)

        See Also
        -------
        :meth:`pygmt.grd2cpt`
        """

        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdhisteq", arg_str)

        if output_type == "file":
            return None
        if output_type == "xarray":
            return load_dataarray(tmpfile.name)

        result = pd.read_csv(kwargs["D"], sep="\t", header=None)
        if output_type == "numpy":
            result = result.to_numpy()
        return result

    @staticmethod
    @fmt_docstring
    @use_alias(
        C="divisions",
        G="outgrid",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
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
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.
        outgrid : str or bool or None
            The name of the output netCDF file with extension .nc to store the
            grid in.
        divisions : int
            Set the number of divisions of the data range.

        {R}
        {V}

        Returns
        -------
        ret: xarray.DataArray or None
            Return type depends on the ``outgrid`` parameter:

            - xarray.DataArray if ``outgrid`` is True or None
            - None if ``outgrid`` is a str (grid output is stored in
              ``outgrid``)

        See Also
        -------
        :meth:`pygmt.grd2cpt`
        """
        # Return a xarray.DataArray if ``outgrid`` is not set
        if "G" in kwargs and isinstance(kwargs["G"], str):
            output_type = "file"
        else:
            output_type = "xarray"
        with GMTTempFile(suffix=".nc") as tmpfile:
            if output_type != "file":
                kwargs.update({"G": tmpfile.name})
            return grdhisteq._grdhisteq(
                grid=grid,
                output_type=output_type,
                tmpfile=tmpfile,
                **kwargs,
            )

    @staticmethod
    @fmt_docstring
    @use_alias(
        C="divisions",
        D="outfile",
        R="region",
        N="gaussian",
        Q="quadratic",
        V="verbose",
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
        output can be used to make a colormap with :meth:`pygmt.makecpt` and an
        image with :meth:`pygmt.Figure.grdimage` that has all levels of gray
        occuring equally.

        Full option list at :gmt-docs:`grdhisteq.html`

        {aliases}

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

        {R}
        {V}

        Returns
        -------
        ret: pandas.DataFrame None
            Return type depends on the ``outfile`` parameter:

            - pandas.DataFrame if ``outfile`` is True or None
            - None if ``outfile`` is a str (file output is stored in
              ``outfile``)

        See Also
        -------
        :meth:`pygmt.grd2cpt`
        """
        # Return a pandas.DataFrame if ``outfile`` is not set
        if output_type not in ["numpy", "pandas", "file"]:
            raise GMTInvalidInput(
                "Must specify 'output_type' either as 'numpy', 'pandas' or 'file'."
            )

        if "D" in kwargs and output_type != "file":
            msg = (
                f"Changing 'output_type' of grd2xyz from '{output_type}' to 'file' "
                "since 'outfile' parameter is set. Please use output_type='file' "
                "to silence this warning."
            )
            warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
            output_type = "file"
        with GMTTempFile(suffix=".txt") as tmpfile:
            if output_type != "file":
                kwargs.update({"D": tmpfile.name})
            return grdhisteq._grdhisteq(
                grid, output_type=output_type, tmpfile=tmpfile, **kwargs
            )
