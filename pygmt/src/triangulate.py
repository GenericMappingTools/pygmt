"""
triangulate - Delaunay triangulation or Voronoi partitioning and gridding of
Cartesian data.
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


class triangulate:  # pylint: disable=invalid-name
    """
    Delaunay triangulation or Voronoi partitioning and gridding of Cartesian
    data.

    Triangulate reads in x,y[,z] data and performs Delaunay triangulation,
    i.e., it finds how the points should be connected to give the most
    equilateral triangulation possible. If a map projection (give ``region``
    and ``projection``) is chosen then it is applied before the triangulation
    is calculated. By default, the output is triplets of point id numbers that
    make up each triangle. The id numbers refer to the points position (line
    number, starting at 0 for the first line) in the input file. If ``outgrid``
    and ``spacing`` are set a grid will be calculated based on the surface
    defined by the planar triangles. The actual algorithm used in the
    triangulations is either that of Watson [1982] or Shewchuk [1996] [Default
    is Shewchuk if installed; type ``gmt get GMT_TRIANGULATE`` on the command
    line to see which method is selected]. Furthermore, if the Shewchuk
    algorithm is installed then you can also perform the calculation of Voronoi
    polygons and optionally grid your data via the natural nearest neighbor
    algorithm.

    Note
    ----
    For geographic data with global or very large extent you should consider
    :gmt-docs:`sphtriangulate <sphtriangulate.html>` instead since
    ``triangulate`` is a Cartesian or small-geographic area operator and is
    unaware of periodic or polar boundary conditions.
    """

    @staticmethod
    @fmt_docstring
    @use_alias(
        G="outgrid",
        I="spacing",
        J="projection",
        R="region",
        V="verbose",
        b="binary",
        d="nodata",
        e="find",
        f="coltypes",
        h="header",
        i="incols",
        r="registration",
        s="skiprows",
        w="wrap",
    )
    @kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
    def _triangulate(
        data=None, x=None, y=None, z=None, *, output_type, outfile=None, **kwargs
    ):
        """
        Delaunay triangulation or Voronoi partitioning and gridding of
        Cartesian data.

        Must provide ``outfile`` or ``outgrid``.

        Full option list at :gmt-docs:`triangulate.html`

        {aliases}

        Parameters
        ----------
        x/y/z : np.ndarray
            Arrays of x and y coordinates and values z of the data points.
        data : str or {table-like}
            Pass in (x, y, z) or (longitude, latitude, elevation) values by
            providing a file name to an ASCII data table, a 2-D
            {table-classes}.
        {projection}
        {region}
        {spacing}
        outgrid : bool or str
            The name of the output netCDF file with extension .nc to store the
            grid in. The interpolation is performed in the original
            coordinates, so if your triangles are close to the poles you are
            better off projecting all data to a local coordinate system before
            using ``triangulate`` (this is true of all gridding routines) or
            instead select :gmt-docs:`sphtriangulate <sphtriangulate.html>`.
        outfile : str or bool or None
            The name of the output ASCII file to store the results of the
            histogram equalization in.
        output_type: str
            Determines the output type. Use "file", "xarray", "pandas", or
            "numpy".
        {verbose}
        {binary}
        {nodata}
        {find}
        {coltypes}
        {header}
        {incols}
        {registration}
            Only valid with ``outgrid``.
        {skiprows}
        {wrap}

        Returns
        -------
        ret: numpy.ndarray or pandas.DataFrame or xarray.DataArray or None
            Return type depends on the ``output_type`` parameter:

            - numpy.ndarray if ``output_type`` is "numpy"
            - pandas.DataFrame if ``output_type`` is "pandas"
            - xarray.DataArray if ``output_type`` is "xarray""
            - None if ``output_type`` is "file" (output is stored in
              ``outgrid`` or ``outfile``)
        """
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=False
            )
            with table_context as infile:
                # table output if outgrid is unset, else output to outgrid
                if (outgrid := kwargs.get("G")) is None:
                    kwargs.update({">": outfile})
                lib.call_module(
                    module="triangulate", args=build_arg_string(kwargs, infile=infile)
                )

        if output_type == "file":
            return None
        if output_type == "xarray":
            return load_dataarray(outgrid)

        result = pd.read_csv(outfile, sep="\t", header=None)
        if output_type == "numpy":
            return result.to_numpy()
        return result

    @staticmethod
    @fmt_docstring
    def regular_grid(  # pylint: disable=too-many-arguments,too-many-locals
        data=None,
        x=None,
        y=None,
        z=None,
        outgrid=None,
        spacing=None,
        projection=None,
        region=None,
        verbose=None,
        binary=None,
        nodata=None,
        find=None,
        coltypes=None,
        header=None,
        incols=None,
        registration=None,
        skiprows=None,
        wrap=None,
        **kwargs,
    ):
        """
        Delaunay triangle based gridding of Cartesian data.

        Reads in x,y[,z] data and performs Delaunay triangulation, i.e., it
        finds how the points should be connected to give the most equilateral
        triangulation possible. If a map projection (give ``region`` and
        ``projection``) is chosen then it is applied before the triangulation
        is calculated. By setting ``outgrid`` and ``spacing``, a grid will be
        calculated based on the surface defined by the planar triangles. The
        actual algorithm used in the triangulations is either that of Watson
        [1982] or Shewchuk [1996] [Default is Shewchuk if installed; type
        ``gmt get GMT_TRIANGULATE`` on the command line to see which method is
        selected]. This choice is made during the GMT installation.
        Furthermore, if the Shewchuk algorithm is installed then you can also
        perform the calculation of Voronoi polygons and optionally grid your
        data via the natural nearest neighbor algorithm.

        Must provide either ``data`` or ``x``, ``y``, and ``z``.

        Must provide ``region`` and ``spacing``.

        Full option list at :gmt-docs:`triangulate.html`

        Parameters
        ----------
        x/y/z : np.ndarray
            Arrays of x and y coordinates and values z of the data points.
        data : str or {table-like}
            Pass in (x, y[, z]) or (longitude, latitude[, elevation]) values by
            providing a file name to an ASCII data table, a 2-D
            {table-classes}.
        {projection}
        {region}
        {spacing}
        outgrid : str or None
            The name of the output netCDF file with extension .nc to store the
            grid in. The interpolation is performed in the original
            coordinates, so if your triangles are close to the poles you are
            better off projecting all data to a local coordinate system before
            using ``triangulate`` (this is true of all gridding routines) or
            instead select :gmt-docs:`sphtriangulate <sphtriangulate.html>`.
        {verbose}
        {binary}
        {nodata}
        {find}
        {coltypes}
        {header}
        {incols}
        {registration}
        {skiprows}
        {wrap}

        Returns
        -------
        ret: xarray.DataArray or None
            Return type depends on whether the ``outgrid`` parameter is set:

            - xarray.DataArray if ``outgrid`` is None (default)
            - None if ``outgrid`` is a str (grid output is stored in
              ``outgrid``)

        Note
        ----
        For geographic data with global or very large extent you should
        consider :gmt-docs:`sphtriangulate <sphtriangulate.html>` instead since
        ``triangulate`` is a Cartesian or small-geographic area operator and is
        unaware of periodic or polar boundary conditions.
        """
        # Return an xarray.DataArray if ``outgrid`` is not set
        with GMTTempFile(suffix=".nc") as tmpfile:
            if isinstance(outgrid, str):
                output_type = "file"
            elif outgrid is None:
                output_type = "xarray"
                outgrid = tmpfile.name
            else:
                raise GMTInvalidInput(
                    "'outgrid' should be a proper file name or `None`"
                )

            return triangulate._triangulate(
                data=data,
                x=x,
                y=y,
                z=z,
                output_type=output_type,
                outgrid=outgrid,
                spacing=spacing,
                projection=projection,
                region=region,
                verbose=verbose,
                binary=binary,
                nodata=nodata,
                find=find,
                coltypes=coltypes,
                header=header,
                incols=incols,
                registration=registration,
                skiprows=skiprows,
                wrap=wrap,
                **kwargs,
            )

    @staticmethod
    @fmt_docstring
    def delaunay_triples(  # pylint: disable=too-many-arguments,too-many-locals
        data=None,
        x=None,
        y=None,
        z=None,
        output_type="pandas",
        outfile=None,
        projection=None,
        verbose=None,
        binary=None,
        nodata=None,
        find=None,
        coltypes=None,
        header=None,
        incols=None,
        skiprows=None,
        wrap=None,
        **kwargs,
    ):
        """
        Delaunay triangle based gridding of Cartesian data.

        Reads in x,y[,z] data and performs Delaunay triangulation, i.e., it
        finds how the points should be connected to give the most equilateral
        triangulation possible. If a map projection (give ``region`` and
        ``projection``) is chosen then it is applied before the triangulation
        is calculated. The actual algorithm used in the triangulations is
        either that of Watson [1982] or Shewchuk [1996] [Default if installed;
        type ``gmt get GMT_TRIANGULATE`` on the command line to see which
        method is selected).

        Must provide either ``data`` or ``x``, ``y``, and ``z``.

        Full option list at :gmt-docs:`triangulate.html`

        Parameters
        ----------
        x/y/z : np.ndarray
            Arrays of x and y coordinates and values z of the data points.
        data : str or {table-like}
            Pass in (x, y, z) or (longitude, latitude, elevation) values by
            providing a file name to an ASCII data table, a 2-D
            {table-classes}.
        {projection}
        {region}
        outfile : str or bool or None
            The name of the output ASCII file to store the results of the
            histogram equalization in.
        output_type : str
            Determine the format the xyz data will be returned in [Default is
            ``pandas``]:

                - ``numpy`` - :class:`numpy.ndarray`
                - ``pandas``- :class:`pandas.DataFrame`
                - ``file`` - ASCII file (requires ``outfile``)
        {verbose}
        {binary}
        {nodata}
        {find}
        {coltypes}
        {header}
        {incols}
        {skiprows}
        {wrap}

        Returns
        -------
        ret : pandas.DataFrame or numpy.ndarray or None
            Return type depends on ``outfile`` and ``output_type``:

            - None if ``outfile`` is set (output will be stored in file set by
              ``outfile``)
            - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if
              ``outfile`` is not set (depends on ``output_type``)

        Note
        ----
        For geographic data with global or very large extent you should
        consider :gmt-docs:`sphtriangulate <sphtriangulate.html>` instead since
        ``triangulate`` is a Cartesian or small-geographic area operator and is
        unaware of periodic or polar boundary conditions.
        """
        # Return a pandas.DataFrame if ``outfile`` is not set
        if output_type not in ["numpy", "pandas", "file"]:
            raise GMTInvalidInput(
                "Must specify 'output_type' either as 'numpy', 'pandas' or 'file'."
            )

        if isinstance(outfile, str) and output_type != "file":
            msg = (
                f"Changing 'output_type' from '{output_type}' to 'file' "
                "since 'outfile' parameter is set. Please use output_type='file' "
                "to silence this warning."
            )
            warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
            output_type = "file"

        # Return a pandas.DataFrame if ``outfile`` is not set
        with GMTTempFile(suffix=".txt") as tmpfile:
            if output_type != "file":
                outfile = tmpfile.name
            return triangulate._triangulate(
                data=data,
                x=x,
                y=y,
                z=z,
                output_type=output_type,
                outfile=outfile,
                projection=projection,
                verbose=verbose,
                binary=binary,
                nodata=nodata,
                find=find,
                coltypes=coltypes,
                header=header,
                incols=incols,
                skiprows=skiprows,
                wrap=wrap,
                **kwargs,
            )
