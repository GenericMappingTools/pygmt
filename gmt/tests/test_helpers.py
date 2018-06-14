"""
Tests the helper functions/classes/etc used in wrapping GMT
"""
import os

import pytest

from ..helpers import kwargs_to_strings, GMTTempFile, unique_name
from ..exceptions import GMTInvalidInput


def test_unique_name():
    "Make sure the names start with gmt-python- and are really unique"
    names = [unique_name() for i in range(100)]
    assert all([name.startswith("gmt-python-") for name in names])
    assert len(names) == len(set(names))


def test_kwargs_to_strings_fails():
    "Make sure it fails for invalid conversion types."
    with pytest.raises(GMTInvalidInput):
        kwargs_to_strings(bla="blablabla")


def test_kwargs_to_strings_no_bools():
    "Test that not converting bools works"

    @kwargs_to_strings(convert_bools=False)
    def my_module(**kwargs):
        "Function that does nothing"
        return kwargs

    # The module should return the exact same arguments it was given
    args = dict(P=True, A=False, R="1/2/3/4")
    assert my_module(**args) == args


def test_gmttempfile():
    "Check that file is really created and deleted."
    with GMTTempFile() as tmpfile:
        assert os.path.exists(tmpfile.name)
    # File should be deleted when leaving the with block
    assert not os.path.exists(tmpfile.name)


def test_gmttempfile_unique():
    "Check that generating multiple files creates unique names"
    with GMTTempFile() as tmp1:
        with GMTTempFile() as tmp2:
            with GMTTempFile() as tmp3:
                assert tmp1.name != tmp2.name != tmp3.name


def test_gmttempfile_prefix_suffix():
    "Make sure the prefix and suffix of temporary files are user specifiable"
    with GMTTempFile() as tmpfile:
        assert os.path.basename(tmpfile.name).startswith("gmt-python-")
        assert os.path.basename(tmpfile.name).endswith(".txt")
    with GMTTempFile(prefix="user-prefix-") as tmpfile:
        assert os.path.basename(tmpfile.name).startswith("user-prefix-")
        assert os.path.basename(tmpfile.name).endswith(".txt")
    with GMTTempFile(suffix=".log") as tmpfile:
        assert os.path.basename(tmpfile.name).startswith("gmt-python-")
        assert os.path.basename(tmpfile.name).endswith(".log")
    with GMTTempFile(prefix="user-prefix-", suffix=".log") as tmpfile:
        assert os.path.basename(tmpfile.name).startswith("user-prefix-")
        assert os.path.basename(tmpfile.name).endswith(".log")


def test_gmttempfile_read():
    "Make sure GMTTempFile.read() works"
    with GMTTempFile() as tmpfile:
        with open(tmpfile.name, "w") as ftmp:
            ftmp.write("in.dat: N = 2\t<1/3>\t<2/4>\n")
        assert tmpfile.read() == "in.dat: N = 2 <1/3> <2/4>\n"
        assert tmpfile.read(keep_tabs=True) == "in.dat: N = 2\t<1/3>\t<2/4>\n"
