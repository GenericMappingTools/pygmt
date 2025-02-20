"""
Test the Session.virtualfile_from_vectors method.
"""

from importlib.util import find_spec

import numpy as np
import pandas as pd
import pytest
from pygmt import clib
from pygmt.clib.session import DTYPES_NUMERIC
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import skip_if_no

try:
    import pyarrow as pa

    pa_array = pa.array
except ImportError:
    pa_array = None


@pytest.fixture(scope="module", name="dtypes")
def fixture_dtypes():
    """
    List of supported numpy dtypes.
    """
    return [dtype for dtype in DTYPES_NUMERIC if dtype != np.timedelta64]


@pytest.fixture(scope="module", name="dtypes_pandas")
def fixture_dtypes_pandas(dtypes):
    """
    List of supported pandas dtypes.
    """
    dtypes_pandas = dtypes.copy()
    if find_spec("pyarrow") is not None:
        dtypes_pandas.extend([f"{np.dtype(dtype).name}[pyarrow]" for dtype in dtypes])
    return tuple(dtypes_pandas)


@pytest.mark.benchmark
def test_virtualfile_from_vectors(dtypes):
    """
    Test the automation for transforming vectors to virtual file dataset.
    """
    size = 10
    for dtype in dtypes:
        x = np.arange(size, dtype=dtype)
        y = np.arange(size, size * 2, 1, dtype=dtype)
        z = np.arange(size * 2, size * 3, 1, dtype=dtype)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors((x, y, z)) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{i.min():.0f}/{i.max():.0f}>" for i in (x, y, z)])
            expected = f"<vector memory>: N = {size}\t{bounds}\n"
            assert output == expected


@pytest.mark.benchmark
@pytest.mark.parametrize(
    ("array_func", "dtype"),
    [
        pytest.param(np.array, {"dtype": np.str_}, id="str"),
        pytest.param(np.array, {"dtype": np.object_}, id="object"),
        pytest.param(
            pa_array,
            {},  # {"type": pa.string()}
            marks=skip_if_no(package="pyarrow"),
            id="pyarrow",
        ),
    ],
)
def test_virtualfile_from_vectors_one_string_or_object_column(array_func, dtype):
    """
    Test passing in one column with string (numpy/pyarrow) or object (numpy)
    dtype into virtual file dataset.
    """
    size = 5
    x = np.arange(size, dtype=np.int32)
    y = np.arange(size, size * 2, 1, dtype=np.int32)
    strings = array_func(["a", "bc", "defg", "hijklmn", "opqrst"], **dtype)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors(vectors=(x, y, strings)) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("convert", [vfile, f"->{outfile.name}"])
                output = outfile.read(keep_tabs=True)
        expected = "".join(
            f"{i}\t{j}\t{k}\n" for i, j, k in zip(x, y, strings, strict=True)
        )
        assert output == expected


@pytest.mark.parametrize("dtype", [str, object])
def test_virtualfile_from_vectors_two_string_or_object_columns(dtype):
    """
    Test passing in two columns of string or object dtype into virtual file dataset.
    """
    size = 5
    x = np.arange(size, dtype=np.int32)
    y = np.arange(size, size * 2, 1, dtype=np.int32)
    # Catch bug in https://github.com/GenericMappingTools/pygmt/pull/2719
    strings1 = np.array(["a", "bc", "def", "ghij", "klmnolooong"], dtype=dtype)
    strings2 = np.array(["pqrst", "uvwx", "yz!", "@#", "$"], dtype=dtype)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors((x, y, strings1, strings2)) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("convert", [vfile, f"->{outfile.name}"])
                output = outfile.read(keep_tabs=True)
        expected = "".join(
            f"{h}\t{i}\t{j} {k}\n"
            for h, i, j, k in zip(x, y, strings1, strings2, strict=True)
        )
        assert output == expected


def test_virtualfile_from_vectors_transpose(dtypes):
    """
    Test transforming matrix columns to virtual file dataset.
    """
    shape = (7, 5)
    for dtype in dtypes:
        data = np.arange(shape[0] * shape[1], dtype=dtype).reshape(shape)
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(data.T) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, "-C", f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"{col.min():.0f}\t{col.max():.0f}" for col in data.T])
            expected = f"{bounds}\n"
            assert output == expected


def test_virtualfile_from_vectors_diff_size():
    """
    Test the function fails for arrays of different sizes.
    """
    x = np.arange(5)
    y = np.arange(6)
    with clib.Session() as lib:
        with pytest.raises(GMTInvalidInput):
            with lib.virtualfile_from_vectors((x, y)):
                pass


def test_virtualfile_from_vectors_pandas(dtypes_pandas):
    """
    Pass vectors to a dataset using pandas.Series, checking both numpy and pyarrow
    dtypes.
    """
    size = 13

    for dtype in dtypes_pandas:
        data = pd.DataFrame(
            data={
                "x": np.arange(size),
                "y": np.arange(size, size * 2, 1),
                "z": np.arange(size * 2, size * 3, 1),
            },
            dtype=dtype,
        )
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors((data.x, data.y, data.z)) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join(
                [f"<{i.min():.0f}/{i.max():.0f}>" for i in (data.x, data.y, data.z)]
            )
            expected = f"<vector memory>: N = {size}\t{bounds}\n"
            assert output == expected


def test_virtualfile_from_vectors_arraylike():
    """
    Pass array-like vectors to a dataset.
    """
    size = 13
    x = list(range(0, size, 1))
    y = tuple(range(size, size * 2, 1))
    z = range(size * 2, size * 3, 1)
    with clib.Session() as lib:
        with lib.virtualfile_from_vectors((x, y, z)) as vfile:
            with GMTTempFile() as outfile:
                lib.call_module("info", [vfile, f"->{outfile.name}"])
                output = outfile.read(keep_tabs=True)
        bounds = "\t".join([f"<{min(i):.0f}/{max(i):.0f}>" for i in (x, y, z)])
        expected = f"<vector memory>: N = {size}\t{bounds}\n"
        assert output == expected


# TODO(PyGMT>=0.16.0): Remove this test in PyGMT v0.16.0 in which the "*args" parameter
# will be removed.
def test_virtualfile_from_vectors_args():
    """
    Test the backward compatibility of the deprecated syntax for passing multiple
    vectors.

    This test is the same as test_virtualfile_from_vectors_arraylike, but using the
    old syntax.
    """
    size = 13
    x = list(range(0, size, 1))
    y = tuple(range(size, size * 2, 1))
    z = range(size * 2, size * 3, 1)
    with pytest.warns(FutureWarning, match="virtualfile_from_vectors"):
        with clib.Session() as lib:
            with lib.virtualfile_from_vectors(x, y, z) as vfile:
                with GMTTempFile() as outfile:
                    lib.call_module("info", [vfile, f"->{outfile.name}"])
                    output = outfile.read(keep_tabs=True)
            bounds = "\t".join([f"<{min(i):.0f}/{max(i):.0f}>" for i in (x, y, z)])
            expected = f"<vector memory>: N = {size}\t{bounds}\n"
            assert output == expected
