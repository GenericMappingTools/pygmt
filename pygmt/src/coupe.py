"""
coupe - Plot cross-sections of focal mechanisms
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias, GMTTempFile
import pandas as pd


@fmt_docstring
@use_alias(
    A="cross_section",
    J="projection",
    Q="suppress",
    R="region",
    S="columns",
    V="verbose",
)
@kwargs_to_strings(
    R="sequence"
)
def coupe(self, data, suppress=True, **kwargs):
    r"""
    Plot cross-sections of focal mechanisms.

    Full option list at :gmt-docs:`coupe.html`

    {aliases}

    Parameters
    ----------
    data : str or list or {table-like}
        Pass in either a file name to an ASCII data table, a Python list, a 2D
        {table-classes}.
    {J}
    {R}
    {V}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                lib.call_module(
                    module="coupe", args=build_arg_string(kwargs, infile=infile)
                )
            if not suppress:
                result = pd.read_csv(tmpfile.name)
                return result
