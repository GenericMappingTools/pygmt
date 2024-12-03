"""
Test the Session.virtualfile_from_stringio method.
"""

import io

import numpy as np
from pygmt import clib


def _stringio_to_dataset(data: io.StringIO):
    """
    A helper function for check the virtualfile_from_stringio method.

    The function does the following:

    1. Creates a virtual file from the input StringIO object.
    2. Pass the virtual file to the ``read`` module, which reads the virtual file and
       writes it to another virtual file.
    3. Reads the output virtual file as a GMT_DATASET object.
    4. Extracts the header and the trailing text from the dataset and returns it as a
       string.
    """
    with clib.Session() as lib:
        with (
            lib.virtualfile_from_stringio(data) as vintbl,
            lib.virtualfile_out(kind="dataset") as vouttbl,
        ):
            lib.call_module("read", args=[vintbl, vouttbl, "-Td"])
            ds = lib.read_virtualfile(vouttbl, kind="dataset").contents

            output = []
            table = ds.table[0].contents
            for segment in table.segment[: table.n_segments]:
                seg = segment.contents
                output.append(f"> {seg.header.decode()}" if seg.header else ">")
                output.extend(np.char.decode(seg.text[: seg.n_rows]))
        return "\n".join(output) + "\n"


def test_virtualfile_from_stringio():
    """
    Test the virtualfile_from_stringio method.
    """
    data = io.StringIO(
        "# Comment\n"
        "H 24p Legend\n"
        "N 2\n"
        "S 0.1i c 0.15i p300/12 0.25p 0.3i My circle\n"
    )
    expected = (
        ">\n" "H 24p Legend\n" "N 2\n" "S 0.1i c 0.15i p300/12 0.25p 0.3i My circle\n"
    )
    assert _stringio_to_dataset(data) == expected


def test_one_segment():
    """
    Test the virtualfile_from_stringio method with one segment.
    """
    data = io.StringIO(
        "# Comment\n"
        "> Segment 1\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FGHIJK LMN OPQ\n"
        "RSTUVWXYZ\n"
    )
    expected = (
        "> Segment 1\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FGHIJK LMN OPQ\n"
        "RSTUVWXYZ\n"
    )
    assert _stringio_to_dataset(data) == expected


def test_multiple_segments():
    """
    Test the virtualfile_from_stringio method with multiple segments.
    """
    data = io.StringIO(
        "# Comment line 1\n"
        "# Comment line 2\n"
        "> Segment 1\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FG\n"
        "# Comment line 3\n"
        "> Segment 2\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FG\n"
    )
    expected = (
        "> Segment 1\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FG\n"
        "> Segment 2\n"
        "1 2 3 ABC\n"
        "4 5 DE\n"
        "6 7 8   9  FG\n"
    )
    assert _stringio_to_dataset(data) == expected
