"""
Test the helper functions/classes/etc used in wrapping GMT.
"""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    args_in_kwargs,
    data_kind,
    kwargs_to_strings,
    unique_name,
)
from pygmt.helpers.testing import load_static_earth_relief, skip_if_no


def test_load_static_earth_relief():
    """
    Check that @static_earth_relief.nc loads without errors.
    """
    data = load_static_earth_relief()
    assert data.dims == ("lat", "lon")
    assert data.shape == (14, 8)
    assert data.min() == 190
    assert data.max() == 981
    assert data.median() == 467
    assert isinstance(data, xr.DataArray)


@pytest.mark.parametrize(
    ("data", "x", "y"),
    [
        (None, None, None),
        ("data.txt", np.array([1, 2]), np.array([4, 5])),
        ("data.txt", np.array([1, 2]), None),
        ("data.txt", None, np.array([4, 5])),
        (None, np.array([1, 2]), None),
        (None, None, np.array([4, 5])),
    ],
)
def test_data_kind_fails(data, x, y):
    """
    Make sure data_kind raises exceptions when it should.
    """
    with pytest.raises(GMTInvalidInput):
        data_kind(data=data, x=x, y=y)


def test_unique_name():
    """
    Make sure the names are really unique.
    """
    names = [unique_name() for i in range(100)]
    assert len(names) == len(set(names))


@pytest.mark.mpl_image_compare
def test_non_ascii_to_octal():
    """
    Test support of non-ASCII characters.
    """
    fig = Figure()
    fig.basemap(
        region=[0, 10, 0, 5],
        projection="X10c/5c",
        frame=[
            "xaf+lISOLatin1: ﬁ‰“”¥",
            "yaf+lSymbol: αβ∇∋∈",
            "WSen+tZapfDingbats: ①❷➂➍✦❝❞",
        ],
    )
    return fig


def test_kwargs_to_strings_fails():
    """
    Make sure it fails for invalid conversion types.
    """
    with pytest.raises(GMTInvalidInput):
        kwargs_to_strings(bla="blablabla")


def test_gmttempfile():
    """
    Check that file is really created and deleted.
    """
    with GMTTempFile() as tmpfile:
        assert Path(tmpfile.name).exists()
    # File should be deleted when leaving the with block
    assert not Path(tmpfile.name).exists()


def test_gmttempfile_unique():
    """
    Check that generating multiple files creates unique names.
    """
    with GMTTempFile() as tmp1:
        with GMTTempFile() as tmp2:
            with GMTTempFile() as tmp3:
                assert tmp1.name != tmp2.name != tmp3.name


def test_gmttempfile_prefix_suffix():
    """
    Make sure the prefix and suffix of temporary files are user specifiable.
    """
    with GMTTempFile() as tmpfile:
        tmpname = Path(tmpfile.name).name
        assert tmpname.startswith("pygmt-")
        assert tmpname.endswith(".txt")
    with GMTTempFile(prefix="user-prefix-") as tmpfile:
        tmpname = Path(tmpfile.name).name
        assert tmpname.startswith("user-prefix-")
        assert tmpname.endswith(".txt")
    with GMTTempFile(suffix=".log") as tmpfile:
        tmpname = Path(tmpfile.name).name
        assert tmpname.startswith("pygmt-")
        assert tmpname.endswith(".log")
    with GMTTempFile(prefix="user-prefix-", suffix=".log") as tmpfile:
        tmpname = Path(tmpfile.name).name
        assert tmpname.startswith("user-prefix-")
        assert tmpname.endswith(".log")


def test_gmttempfile_read():
    """
    Make sure GMTTempFile.read() works.
    """
    with GMTTempFile() as tmpfile:
        Path(tmpfile.name).write_text("in.dat: N = 2\t<1/3>\t<2/4>\n")
        assert tmpfile.read() == "in.dat: N = 2 <1/3> <2/4>\n"
        assert tmpfile.read(keep_tabs=True) == "in.dat: N = 2\t<1/3>\t<2/4>\n"


def test_args_in_kwargs():
    """
    Test that args_in_kwargs function returns correct Boolean responses.
    """
    kwargs = {"A": 1, "B": 2, "C": 3}
    # Passing list of arguments with passing values in the beginning
    passing_args_1 = ["B", "C", "D"]
    assert args_in_kwargs(args=passing_args_1, kwargs=kwargs)
    # Passing list of arguments that starts with failing arguments
    passing_args_2 = ["D", "X", "C"]
    assert args_in_kwargs(args=passing_args_2, kwargs=kwargs)
    # Failing list of arguments
    failing_args = ["D", "E", "F"]
    assert not args_in_kwargs(args=failing_args, kwargs=kwargs)


def test_skip_if_no():
    """
    Test that the skip_if_no helper testing function returns a pytest.mask.skipif mark
    decorator.
    """
    # Check pytest.mark with a dependency that can be imported
    mark_decorator = skip_if_no(package="numpy")
    assert mark_decorator.args[0] is False

    # Check pytest.mark with a dependency that cannot be imported
    mark_decorator = skip_if_no(package="nullpackage")
    assert mark_decorator.args[0] is True
    assert mark_decorator.kwargs["reason"] == "Could not import 'nullpackage'"
    assert mark_decorator.markname == "skipif"
