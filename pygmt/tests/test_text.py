"""
Test Figure.text.
"""

from pathlib import Path

import numpy as np
import pytest
from pygmt import Figure, config
from pygmt.exceptions import GMTCLibError, GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import skip_if_no

try:
    import pyarrow as pa

    pa_array = pa.array
except ImportError:
    pa_array = None

TEST_DATA_DIR = Path(__file__).parent / "data"
POINTS_DATA = TEST_DATA_DIR / "points.txt"
CITIES_DATA = TEST_DATA_DIR / "cities.txt"


@pytest.fixture(scope="module", name="projection")
def fixture_projection():
    """
    The projection system.
    """
    return "x10c"


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    The data region.
    """
    return [0, 5, 0, 2.5]


@pytest.mark.mpl_image_compare
def test_text_single_line_of_text(region, projection):
    """
    Place a single line text of text at some x, y location.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="This is a line of text",
    )
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_text_multiple_lines_of_text.png")
@pytest.mark.parametrize(
    "array_func",
    [
        list,
        pytest.param(np.array, id="numpy"),
        pytest.param(pa_array, marks=skip_if_no(package="pyarrow"), id="pyarrow"),
    ],
)
def test_text_multiple_lines_of_text(region, projection, array_func):
    """
    Place multiple lines of text at their respective x, y locations.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=[1.2, 1.6],
        y=[0.6, 0.3],
        text=array_func(["This is a line of text", "This is another line of text"]),
    )
    return fig


def test_text_without_text_input(region, projection):
    """
    Run text by passing in x and y, but no text.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection=projection, x=1.2, y=2.4)


@pytest.mark.mpl_image_compare
def test_text_input_single_filename():
    """
    Run text by passing in one filename to textfiles.
    """
    fig = Figure()
    fig.text(region=[10, 70, -5, 10], textfiles=POINTS_DATA)
    return fig


@pytest.mark.mpl_image_compare
def test_text_input_remote_filename():
    """
    Run text by passing in a remote filename to textfiles.
    """
    fig = Figure()
    fig.text(region=[0, 6.5, 0, 6.5], textfiles="@Table_5_11.txt")
    return fig


@pytest.mark.mpl_image_compare
def test_text_input_multiple_filenames():
    """
    Run text by passing in multiple filenames to textfiles.
    """
    fig = Figure()
    fig.text(region=[10, 70, -30, 10], textfiles=[POINTS_DATA, CITIES_DATA])
    return fig


def test_text_nonexistent_filename():
    """
    Run text by passing in a list of filenames with one that does not exist.
    """
    fig = Figure()
    with pytest.raises(GMTCLibError):
        fig.text(region=[10, 70, -5, 10], textfiles=[POINTS_DATA, "notexist.txt"])


@pytest.mark.mpl_image_compare
def test_text_position(region):
    """
    Print text at center middle (CM) and eight other positions (Top/Middle/Bottom x
    Left/Centre/Right).
    """
    fig = Figure()
    fig.text(region=region, projection="x1c", frame="a", position="CM", text="C M")
    for position in ("TL", "TC", "TR", "ML", "MR", "BL", "BC", "BR"):
        fig.text(position=position, text=position)
    return fig


def test_text_invalid_inputs(region):
    """
    Run text by providing invalid combinations of inputs.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.text(
            region=region, projection="x1c", x=1.2, y=2.4, position="MC", text="text"
        )
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection="x1c", textfiles="file.txt", text="text")
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection="x1c", position="MC", text=None)
    with pytest.raises(GMTInvalidInput):
        fig.text(
            region=region, projection="x1c", position="MC", text=["text1", "text2"]
        )
    with pytest.raises(GMTInvalidInput):
        fig.text(region=region, projection="x1c", textfiles="file.txt", x=1.2, y=2.4)


@pytest.mark.mpl_image_compare
def test_text_position_offset_with_line(region):
    """
    Print text at centre middle (CM) and eight other positions (Top/Middle/Bottom x
    Left/Centre/Right), offset by 0.5 cm, with a line drawn from the original to the
    shifted point.
    """
    fig = Figure()
    fig.text(region=region, projection="x1c", frame="a", position="CM", text="C M")
    for position in ("TL", "TC", "TR", "ML", "MR", "BL", "BC", "BR"):
        fig.text(position=position, text=position, offset="j0.5c+v")
    return fig


@pytest.mark.mpl_image_compare
def test_text_angle_30(region, projection):
    """
    Print text at 30 degrees counter-clockwise from horizontal.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="text angle 30 degrees",
        angle=30,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_font_bold(region, projection):
    """
    Print text with a bold font.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=2.4,
        text="text in bold",
        font="Helvetica-Bold",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_fill(region, projection):
    """
    Print text with blue color fill.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="blue fill around text",
        fill="blue",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_pen(region, projection):
    """
    Print text with thick green dashed pen.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="green pen around text",
        pen="thick,green,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_round_clearance(region, projection):
    """
    Print text with round rectangle box clearance.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=1.2,
        text="clearance around text",
        clearance="90%+tO",
        pen="default,black,dashed",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_justify_bottom_right_and_top_left(region, projection):
    """
    Print text justified at bottom right and top left.
    """
    fig = Figure()
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=0.2,
        text="text justified bottom right",
        justify="BR",
    )
    fig.text(
        region=region,
        projection=projection,
        x=1.2,
        y=0.2,
        text="text justified top left",
        justify="TL",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_justify_parsed_from_textfile():
    """
    Print text justified based on a column from textfile, using justify=True boolean
    operation.

    Loosely based on "All great-circle paths lead to Rome" gallery example at
    https://docs.generic-mapping-tools.org/latest/gallery/ex23.html
    """
    fig = Figure()
    fig.text(
        region="g",
        projection="H90/9i",
        justify=True,
        textfiles=CITIES_DATA,
        offset="j0.45/0+vred",  # draw red-line from xy point to text label (city name)
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_angle_font_justify_from_textfile():
    """
    Print text with x, y, angle, font, justify, and text arguments parsed from the
    textfile.
    """
    fig = Figure()
    with GMTTempFile(suffix=".txt") as tempfile:
        Path(tempfile.name).write_text(
            "114 0.5 30 22p,Helvetica-Bold,black LM BORNEO", encoding="utf-8"
        )
        fig.text(
            region=[113, 117.5, -0.5, 3],
            projection="M5c",
            frame="a",
            textfiles=tempfile.name,
            angle=True,
            font=True,
            justify=True,
        )
    return fig


@pytest.mark.mpl_image_compare(filename="test_text_position.png")
def test_text_justify_array(region):
    """
    Test passing an array of justify codes.
    """
    fig = Figure()
    fig.basemap(region=region, projection="x1c", frame="a")
    fig.text(
        x=[0, 2.5, 5.0, 0, 2.5, 5.0, 0, 2.5, 5.0],
        y=[0, 0, 0, 1.25, 1.25, 1.25, 2.5, 2.5, 2.5],
        justify=["BL", "BC", "BR", "ML", "MC", "MR", "TL", "TC", "TR"],
        text=["BL", "BC", "BR", "ML", "C M", "MR", "TL", "TC", "TR"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_angle_justify_font_arrays(region):
    """
    Test passing arrays of angle, justify and font.
    """
    fig = Figure()
    fig.basemap(region=region, projection="X5c/2.5c", frame=True)
    fig.text(
        x=[2.5, 2.5],
        y=[1.0, 2.0],
        angle=[30, 50],
        justify=["TL", "BR"],
        font=["15p,Helvetica-Bold,red", "5p,Times-Italic,blue"],
        text=["TEXT1", "TEXT2 with spaces"],
    )
    return fig


@pytest.mark.mpl_image_compare
def test_text_transparency():
    """
    Add texts with a constant transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(11, 20)
    text = [f"TEXT-{i}-{j}" for i, j in zip(x, y, strict=True)]

    fig = Figure()
    fig.basemap(region=[0, 10, 10, 20], projection="X10c", frame=True)
    fig.text(x=x, y=y, text=text, transparency=50)
    return fig


@pytest.mark.mpl_image_compare
def test_text_varying_transparency():
    """
    Add texts with varying transparency.
    """
    x = np.arange(1, 10)
    y = np.arange(11, 20)
    text = [f"TEXT-{i}-{j}" for i, j in zip(x, y, strict=True)]
    transparency = np.arange(10, 100, 10)

    fig = Figure()
    fig.basemap(region=[0, 10, 10, 20], projection="X10c", frame=True)
    fig.text(x=x, y=y, text=text, transparency=transparency)
    return fig


@pytest.mark.mpl_image_compare(filename="test_text_input_single_filename.png")
@pytest.mark.parametrize("transparency", [None, False, 0])
def test_text_no_transparency(transparency):
    """
    Add text with no transparency set.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/issues/1852.
    """
    fig = Figure()
    fig.text(region=[10, 70, -5, 10], textfiles=POINTS_DATA, transparency=transparency)
    return fig


@pytest.mark.mpl_image_compare
def test_text_nonstr_text():
    """
    Input text is in non-string type (e.g., int, float)
    """
    fig = Figure()
    fig.text(
        region=[0, 10, 0, 10],
        projection="X10c",
        frame=True,
        x=[1, 2, 3, 4],
        y=[1, 2, 3, 4],
        text=[1, 2, 3.0, 4.0],
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_text_nonascii.png")
@pytest.mark.parametrize("encoding", ["ISOLatin1+", "Standard+"])
def test_text_nonascii(encoding):
    """
    Test passing text strings with non-ascii characters.

    Default PS_CHAR_ENCODING setting should not affect the result.
    """
    fig = Figure()
    if encoding == "Standard+":  # Temporarily set the PS_CHAR_ENCODING to "Standard+".
        config(PS_CHAR_ENCODING="Standard+")
    fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    fig.text(position="TL", text="position-text:°α")  # noqa: RUF001
    fig.text(x=1, y=1, text="xytext:°α")  # noqa: RUF001
    fig.text(x=[5, 5], y=[3, 5], text=["xytext1:αζ∆❡", "xytext2:∑π∇✉"])
    return fig


@pytest.mark.mpl_image_compare
def test_text_quotation_marks():
    """
    Test typesetting quotation marks.

    See https://github.com/GenericMappingTools/pygmt/issues/3104.
    """
    fig = Figure()
    fig.basemap(projection="X4c/2c", region=[0, 4, 0, 2], frame=0)
    fig.text(x=2, y=1, text='\\234 ‘ ’ " “ ”', font="20p")  # noqa: RUF001
    return fig


@pytest.mark.mpl_image_compare
def test_text_nonascii_iso8859():
    """
    Test passing text strings with non-ascii characters in ISO-8859-4 encoding.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=["WSEN+tAāáâãäåB"])
    fig.text(position="TL", text="position-text:1ÉĘËĖ2")
    fig.text(x=1, y=1, text="xytext:1éęëė2")
    fig.text(x=[5, 5], y=[3, 5], text=["xytext1:ųúûüũūαζ∆❡", "xytext2:íîī∑π∇✉"])
    return fig
