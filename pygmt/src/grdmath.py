"""
grdmath - Raster calculator for grids (element by element)
"""

from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


class GrdMathCalc:
    """
    Raster calculator for grids (element by element).
    """

    def __init__(self, arg_str=None):
        self.arg_str = "" if arg_str is None else arg_str

    def __repr__(self):
        return f"gmt grdmath {self.arg_str}"

    def compute(self):
        """
        Perform the grdmath computation and returns an xarray.DataArray object.
        """
        with Session() as lib:
            with GMTTempFile(suffix=".nc") as tmpfile:
                outgrid = tmpfile.name
                # print(f"Executing gmt grdmath {self.arg_str}")
                lib.call_module("grdmath", f"{self.arg_str} = {outgrid}")
                return load_dataarray(outgrid)

    @classmethod
    @fmt_docstring
    @use_alias(R="region", V="verbose")
    @kwargs_to_strings(R="sequence")
    def grdmath(cls, operator, ingrid=None, outgrid=None, old_arg_str=None, **kwargs):
        """
        Raster calculator for grids (element-wise operations).

        Full option list at :gmt-docs:`grdmath.html`

        {aliases}

        Parameters
        ----------
        operator : str
            The mathematical operator to use. Full list of available
            operations is at :gmt-docs:`grdmath.html#operators`.

        ingrid : str or float

        outgrid : str or bool or None
            The name of a 2-D grid file that will hold the final result. Set to
            True to output to an :class:`xarray.DataArray`. Default is None,
            which will save the computation graph, to be computed or appended
            to with more operations later.

        old_arg_str : str

        Returns
        -------
        ret : pygmt.GrdMathCalc or xarray.DataArray or None
            Return type depends on whether the ``outgrid`` parameter is set:

            - :class:`pygmt.GrdMathCalc` if ``outgrid`` is None (computational
              graph is created, and more operations can be appended)
            - :class:`xarray.DataArray` if ``outgrid`` is True
            - None if ``outgrid`` is a str (grid output will be stored in file
              set by ``outgrid``)
        """
        old_arg_str = old_arg_str or ""  # Convert None to empty string

        with Session() as lib:
            if isinstance(ingrid, GrdMathCalc):
                file_context = dummy_context(ingrid.arg_str)
            else:
                file_context = lib.virtualfile_from_data(
                    check_kind="raster", data=ingrid
                )

            with file_context as infile:
                arg_str = " ".join(
                    [old_arg_str, infile, build_arg_string(kwargs)]
                ).strip()
                arg_str += f" {operator}"

            # If no output is requested, just build computational graph
            if outgrid is None:
                result = cls(arg_str=arg_str)

            # If output is requested, compute output grid
            elif outgrid is not None:
                with GMTTempFile(suffix=".nc") as tmpfile:
                    if outgrid is True:
                        outgrid = tmpfile.name
                    arg_str += f" = {outgrid}"
                    # print(f"Executing gmt grdmath {arg_str}")
                    lib.call_module("grdmath", arg_str)
                    result = (
                        load_dataarray(outgrid) if outgrid == tmpfile.name else None
                    )

            return result

    def sqrt(self, ingrid, outgrid=None, **kwargs):
        """
        sqrt (A). 1 input, 1 output.
        """
        return self.grdmath(operator="SQRT", ingrid=ingrid, outgrid=outgrid, **kwargs)

    def std(self, ingrid, outgrid=None, **kwargs):
        """
        Standard deviation of A. 1 input, 1 output.
        """
        return self.grdmath(operator="STD", ingrid=ingrid, outgrid=outgrid, **kwargs)

    def multiply(self, ingrid, outgrid=None, **kwargs):
        """
        A * B. 2 inputs, 1 output
        """
        return self.grdmath(
            operator="MUL",
            ingrid=ingrid,
            outgrid=outgrid,
            old_arg_str=self.arg_str,
            **kwargs,
        )
