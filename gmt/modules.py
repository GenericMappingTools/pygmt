"""
Non-plot GMT modules.
"""
from tempfile import NamedTemporaryFile

from .clib import LibGMT
from .utils import build_arg_string
from .decorators import fmt_docstring


@fmt_docstring
def info(fname, **kwargs):
    """
    Get information about data tables.

    {gmt_module_docs}

    Parameters
    ----------
    fname : str
        The file name of the input data table file.
    """
    assert isinstance(fname, str), 'Only accepts file names.'

    with GMTTempFile() as tmpfile:
        arg_str = ' '.join([fname, build_arg_string(kwargs),
                            "->" + tmpfile.name])
        with LibGMT() as lib:
            lib.call_module('info', arg_str)
        return tmpfile.read()
