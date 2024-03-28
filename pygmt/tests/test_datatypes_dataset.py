"""
Tests for GMT_DATASET data type.
"""

from pathlib import Path

import pandas as pd
import pytest
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


def dataframe_from_gmt(fname):
    """
    Read tabular data as pandas.DataFrame using GMT virtual file.
    """
    with Session() as lib:
        with lib.virtualfile_out(kind="dataset") as vouttbl:
            lib.call_module("read", f"{fname} {vouttbl} -Td")
            df = lib.virtualfile_to_dataset(vfname=vouttbl)
            return df


@pytest.mark.benchmark
def test_dataset():
    """
    Test the basic functionality of GMT_DATASET.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with Path(tmpfile.name).open(mode="w") as fp:
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
        with Path(tmpfile.name).open(mode="w") as fp:
            print("# This is a comment line.", file=fp)

        df = dataframe_from_gmt(tmpfile.name)
        assert df.empty  # Empty DataFrame
        expected_df = dataframe_from_pandas(tmpfile.name)
        pd.testing.assert_frame_equal(df, expected_df)
