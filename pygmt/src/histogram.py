"""
Histogram - Create a histogram
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    J="projection",
    G="color",
    R="region",
)
@kwargs_to_strings(R="sequence")
def histogram(self, table, **kwargs):
    r"""
    Histogram
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(data=table)
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs)]
                )
                lib.call_module("histogram", arg_str)
        result = outfile.read()
    return result
