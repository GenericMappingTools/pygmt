"""
triangulate - Delaunay triangulation or Voronoi partitioning and gridding of
Cartesian data.
"""

from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)


class triangulate:  # noqa: N801
    """
    Delaunay triangulation or Voronoi partitioning and gridding of Cartesian data.

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
    def regular_grid(
        data=None, x=None, y=None, z=None, outgrid: str | None = None, **kwargs
    ) -> xr.DataArray | None:
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

        {aliases}

        Parameters
        ----------
        x/y/z : np.ndarray
            Arrays of x and y coordinates and values z of the data points.
        data : str, {table-like}
            Pass in (x, y[, z]) or (longitude, latitude[, elevation]) values by
            providing a file name to an ASCII data table, a 2-D
            {table-classes}.
        {projection}
        {region}
        {spacing}
        {outgrid}
            The interpolation is performed in the original coordinates, so if
            your triangles are close to the poles you are better off projecting
            all data to a local coordinate system before using ``triangulate``
            (this is true of all gridding routines) or instead select
            :gmt-docs:`sphtriangulate <sphtriangulate.html>`.
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
        ret
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
        with Session() as lib:
            with (
                lib.virtualfile_in(
                    check_kind="vector", data=data, x=x, y=y, z=z, required_z=False
                ) as vintbl,
                lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
            ):
                kwargs["G"] = voutgrd
                lib.call_module(
                    module="triangulate", args=build_arg_list(kwargs, infile=vintbl)
                )
                return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)

    @staticmethod
    @fmt_docstring
    @use_alias(
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
    def delaunay_triples(
        data=None,
        x=None,
        y=None,
        z=None,
        *,
        output_type: Literal["pandas", "numpy", "file"] = "pandas",
        outfile: str | None = None,
        **kwargs,
    ) -> pd.DataFrame | np.ndarray | None:
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

        {aliases}

        Parameters
        ----------
        x/y/z : np.ndarray
            Arrays of x and y coordinates and values z of the data points.
        data : str, {table-like}
            Pass in (x, y, z) or (longitude, latitude, elevation) values by
            providing a file name to an ASCII data table, a 2-D
            {table-classes}.
        {projection}
        {region}
        {output_type}
        {outfile}
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
        ret
            Return type depends on ``outfile`` and ``output_type``:

            - ``None`` if ``outfile`` is set (output will be stored in file set by
              ``outfile``)
            - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not
              set (depends on ``output_type``)

        Note
        ----
        For geographic data with global or very large extent you should
        consider :gmt-docs:`sphtriangulate <sphtriangulate.html>` instead since
        ``triangulate`` is a Cartesian or small-geographic area operator and is
        unaware of periodic or polar boundary conditions.
        """
        output_type = validate_output_table_type(output_type, outfile=outfile)

        with Session() as lib:
            with (
                lib.virtualfile_in(
                    check_kind="vector", data=data, x=x, y=y, z=z, required_z=False
                ) as vintbl,
                lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
            ):
                lib.call_module(
                    module="triangulate",
                    args=build_arg_list(kwargs, infile=vintbl, outfile=vouttbl),
                )
            return lib.virtualfile_to_dataset(vfname=vouttbl, output_type=output_type)
