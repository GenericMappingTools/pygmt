"""
Tests for the Session.call_module method.
"""

from pathlib import Path

import pytest
from pygmt import Figure, clib
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.helpers import GMTTempFile

POINTS_DATA = Path(__file__).parent / "data" / "points.txt"


@pytest.mark.benchmark
def test_call_module():
    """
    Call a GMT module by passing a list of arguments.
    """
    with clib.Session() as lib:
        with GMTTempFile() as out_fname:
            lib.call_module("info", [str(POINTS_DATA), "-C", f"->{out_fname.name}"])
            assert Path(out_fname.name).stat().st_size > 0
            output = out_fname.read().strip()
            assert output == "11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338"


def test_call_module_argument_string():
    """
    Call a GMT module by passing a single argument string.
    """
    with clib.Session() as lib:
        with GMTTempFile() as out_fname:
            lib.call_module("info", f"{POINTS_DATA} -C ->{out_fname.name}")
            assert Path(out_fname.name).stat().st_size > 0
            output = out_fname.read().strip()
            assert output == "11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338"


def test_call_module_empty_argument():
    """
    call_module should work if an empty string or an empty list is passed as argument.
    """
    Figure()
    with clib.Session() as lib:
        lib.call_module("logo", "")
    with clib.Session() as lib:
        lib.call_module("logo", [])


def test_call_module_invalid_argument_type():
    """
    call_module only accepts a string or a list of strings as module arguments.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            lib.call_module("get", ("FONT_TITLE", "FONT_TAG"))


def test_call_module_invalid_arguments():
    """
    call_module should fail for invalid module arguments.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module("info", ["bogus-data.bla"])


def test_call_module_invalid_name():
    """
    call_module should fail when an invalid module name is given.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module("meh", [])


def test_call_module_error_message():
    """
    Check if the GMT error message was captured when calling a module.
    """
    with clib.Session() as lib:
        with pytest.raises(GMTCLibError) as exc_info:
            lib.call_module("info", ["bogus-data.bla"])
        assert "Module 'info' failed with status code" in exc_info.value.args[0]
        assert (
            "gmtinfo [ERROR]: Cannot find file bogus-data.bla" in exc_info.value.args[0]
        )
