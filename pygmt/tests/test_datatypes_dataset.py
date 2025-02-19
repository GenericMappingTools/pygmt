"""
Tests for GMT_DATASET data type.
"""

from pathlib import Path

import pandas as pd
import pytest
from pygmt import which
from pygmt.clib import Session
from pygmt.helpers import GMTTempFile


def dataframe_from_pandas(filepath_or_buffer, sep=r"\s+", comment="#", header=None):
    """
    Read tabular data as pandas.DataFrame object using pandas.read_csv().

    The parameters have the same meaning as in ``pandas.read_csv()``.
    """
    try:
        df = pd.read_csv(filepath_or_buffer, sep=sep, comment=comment, header=header)
    except pd.errors.EmptyDataError:
        # Return an empty DataFrame if the file contains no data
        return pd.DataFrame()

    # By default, pandas reads text strings with whitespaces as multiple columns, but
    # GMT concatenates all trailing text as a single string column. Need do find all
    # string columns (with dtype="object") and combine them into a single string column.
    string_columns = df.select_dtypes(include=["object"]).columns
    if len(string_columns) > 1:
        df[string_columns[0]] = df[string_columns].apply(lambda x: " ".join(x), axis=1)
        df = df.drop(string_columns[1:], axis=1)
    # Convert 'object' to 'string' type
    df = df.convert_dtypes(
        convert_string=True,
        convert_integer=False,
        convert_boolean=False,
        convert_floating=False,
    )
    return df


def dataframe_from_gmt(fname, **kwargs):
    """
    Read tabular data as pandas.DataFrame using GMT virtual file.
    """
    with Session() as lib:
        with lib.virtualfile_out(kind="dataset") as vouttbl:
            lib.call_module("read", [fname, vouttbl, "-Td"])
            df = lib.virtualfile_to_dataset(vfname=vouttbl, **kwargs)
            return df


@pytest.mark.benchmark
def test_dataset():
    """
    Test the basic functionality of GMT_DATASET.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print(">", file=fp)
            print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
            print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)
            print(">", file=fp)
            print("7.0 8.0 9.0 TEXT8 TEXT90", file=fp)
            print("10.0 11.0 12.0 TEXT123 TEXT456789", file=fp)

        df = dataframe_from_gmt(tmpfile.name)
        expected_df = dataframe_from_pandas(tmpfile.name, comment=">")
        pd.testing.assert_frame_equal(df, expected_df)


def test_dataset_empty():
    """
    Make sure that an empty DataFrame is returned if a file contains no data.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print("# This is a comment line.", file=fp)

        df = dataframe_from_gmt(tmpfile.name)
        assert df.empty  # Empty DataFrame
        expected_df = dataframe_from_pandas(tmpfile.name)
        pd.testing.assert_frame_equal(df, expected_df)


def test_dataset_header():
    """
    Test parsing column names from dataset header.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print("# lon lat z text", file=fp)
            print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
            print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)

        # Parse column names from the first header line
        df = dataframe_from_gmt(tmpfile.name, header=0)
        assert df.columns.tolist() == ["lon", "lat", "z", "text"]
        # pd.read_csv() can't parse the header line with a leading '#'.
        # So, we need to skip the header line and manually set the column names.
        expected_df = dataframe_from_pandas(tmpfile.name, header=None)
        expected_df.columns = df.columns.tolist()
        pd.testing.assert_frame_equal(df, expected_df)


def test_dataset_header_greater_than_nheaders():
    """
    Test passing a header line number that is greater than the number of header lines.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print("# lon lat z text", file=fp)
            print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
            print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)

        # Parse column names from the second header line.
        df = dataframe_from_gmt(tmpfile.name, header=1)
        # There is only one header line, so the column names should be default.
        assert df.columns.tolist() == [0, 1, 2, 3]
        expected_df = dataframe_from_pandas(tmpfile.name, header=None)
        pd.testing.assert_frame_equal(df, expected_df)


def test_dataset_header_too_many_names():
    """
    Test passing a header line with more column names than the number of columns.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w", encoding="utf-8") as fp:
            print("# lon lat z text1 text2", file=fp)
            print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
            print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)

        df = dataframe_from_gmt(tmpfile.name, header=0)
        assert df.columns.tolist() == ["lon", "lat", "z", "text1"]
        # pd.read_csv() can't parse the header line with a leading '#'.
        # So, we need to skip the header line and manually set the column names.
        expected_df = dataframe_from_pandas(tmpfile.name, header=None)
        expected_df.columns = df.columns.tolist()
        pd.testing.assert_frame_equal(df, expected_df)


def test_dataset_to_strings_with_none_values():
    """
    Test that None values in the trailing text doesn't raise an exception.

    Due to a likely upstream bug, the trailing texts sometimes can be ``None`` when
    downloading tiled grids. The temporary workaround is to replace any None values with
    an empty string.

    See the bug report at https://github.com/GenericMappingTools/pygmt/issues/3170.
    """
    tiles = ["@N30E060.earth_age_01m_g.nc", "@N30E090.earth_age_01m_g.nc"]
    paths = which(fname=tiles, download="a")
    assert len(paths) == 2
    # 'paths' may contain an empty string or not, depending on if the tiles are cached.
    if "" not in paths:  # Contains two valid paths.
        # Delete the cached tiles and try again.
        for path in paths:
            Path(path).unlink()
        with pytest.warns(expected_warning=RuntimeWarning) as record:
            paths = which(fname=tiles, download="a")
            assert len(record) == 1
        assert len(paths) == 2
        assert "" in paths
