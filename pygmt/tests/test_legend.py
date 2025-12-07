"""
Test Figure.legend.
"""

import io
from pathlib import Path

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTTypeError
from pygmt.helpers import GMTTempFile
from pygmt.params import Position


@pytest.fixture(scope="module", name="legend_spec")
def fixture_legend_spec():
    """
    A string contains a legend specification.
    """
    return """
G -0.1i
H 24 Times-Roman My Map Legend
D 0.2i 1p
N 2
V 0 1p
S 0.1i c 0.15i p300/12 0.25p 0.3i This circle is hachured
S 0.1i e 0.15i yellow 0.25p 0.3i This ellipse is yellow
S 0.1i w 0.15i green 0.25p 0.3i This wedge is green
S 0.1i f0.1i+l+t 0.25i blue 0.25p 0.3i This is a fault
S 0.1i - 0.15i - 0.25p,- 0.3i A dashed contour
S 0.1i v0.1i+a40+e 0.25i magenta 0.25p 0.3i This is a vector
S 0.1i i 0.15i cyan 0.25p 0.3i This triangle is boring
V 0 1p
D 0.2i 1p
N 1
G 0.05i
G 0.05i
G 0.05i
L 9 4 R Smith et al., @%5%J. Geophys. Res., 99@%%, 2000
G 0.1i
P
T Let us just try some simple text that can go on a few lines.
T There is no easy way to predetermine how many lines will be required,
T so we may have to adjust the box height to get the right size box.
"""


@pytest.mark.mpl_image_compare
def test_legend_position():
    """
    Test positioning the legend with different coordinate systems.
    """
    fig = Figure()
    fig.basemap(region=[-2, 2, -2, 2], frame=True)
    positions = [
        Position("TR", anchor="TR"),
        Position((0, 1), type="mapcoords"),
        Position((0.2, 0.2), type="boxcoords"),
        Position(("4i", "2i"), type="plotcoords"),
    ]
    for i, position in enumerate(positions):
        fig.plot(x=[0], y=[0], style="p10p", label=i)
        fig.legend(position=position, box=True)
    return fig


@pytest.mark.mpl_image_compare
def test_legend_default_position():
    """
    Test using the default legend position.
    """
    fig = Figure()
    fig.basemap(region=[-1, 1, -1, 1], frame=True)
    fig.plot(x=[0], y=[0], style="p10p", label="Default")
    fig.legend()
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_legend_entries():
    """
    Test legend using the automatically generated legend entries.
    """
    fig = Figure()
    fig.basemap(projection="x1i", region=[0, 7, 3, 7], frame=True)
    fig.plot(
        data="@Table_5_11.txt",
        style="c0.15i",
        fill="lightgreen",
        pen="faint",
        label="Apples",
    )
    fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", label="My lines")
    fig.plot(data="@Table_5_11.txt", style="t0.15i", fill="orange", label="Oranges")
    fig.legend(position=Position("TR", type="outside", anchor="TR"))
    return fig


@pytest.mark.mpl_image_compare
def test_legend_specfile(legend_spec):
    """
    Test passing a legend specification file.
    """
    with GMTTempFile() as specfile:
        Path(specfile.name).write_text(legend_spec, encoding="utf-8")
        fig = Figure()
        fig.basemap(projection="x6i", region=[0, 1, 0, 1], frame=True)
        fig.legend(
            specfile.name,
            position=Position("MC", type="outside", anchor="CM"),
            width="5i",
        )
        return fig


@pytest.mark.mpl_image_compare(filename="test_legend_specfile.png")
def test_legend_stringio(legend_spec):
    """
    Test passing a legend specification via an io.StringIO object.
    """
    spec = io.StringIO(legend_spec)
    fig = Figure()
    fig.basemap(projection="x6i", region=[0, 1, 0, 1], frame=True)
    fig.legend(spec, position=Position("MC", type="outside", anchor="CM"), width="5i")
    return fig


@pytest.mark.mpl_image_compare
def test_legend_width_height():
    """
    Test legend with specified width and height.
    """
    spec = io.StringIO(
        """
S 0.1i c 0.15i p300/12 0.25p 0.3i This circle is hachured
S 0.1i e 0.15i yellow 0.25p 0.3i This ellipse is yellow
S 0.1i w 0.15i green 0.25p 0.3i This wedge is green
S 0.1i f0.1i+l+t 0.25i blue 0.25p 0.3i This is a fault
S 0.1i - 0.15i - 0.25p,- 0.3i A dashed contour
S 0.1i v0.1i+a40+e 0.25i magenta 0.25p 0.3i This is a vector
S 0.1i i 0.15i cyan 0.25p 0.3i This triangle is boring
"""
    )
    fig = Figure()
    fig.basemap(projection="x1c", region=[0, 20, 0, 20], frame="g1")
    # Default width and height
    fig.legend(spec, position=Position("TL"), box=True)

    # Width only
    fig.legend(spec, position=Position("TC"), width="6c", box=True)
    # Width as percentage of plot width
    fig.legend(spec, position=Position("TR"), width="25%", box=True)

    # Height only, with automatic width
    fig.legend(spec, position=Position("ML"), height="4.5c", box=True)
    # Height as percentage of legend width
    fig.legend(spec, position=Position("BL"), height="75%", box=True)

    # Both width and height
    fig.legend(spec, position=Position("MC"), width="6c", height="4.5c", box=True)
    # Height as percentage of legend width
    fig.legend(spec, position=Position("BC"), width="6c", height="75%", box=True)
    # Width as percentage of plot width and height as percentage of legend width
    fig.legend(spec, position=Position("BR"), width="25%", height="75%", box=True)

    return fig


def test_legend_fails():
    """
    Test legend fails with invalid spec.
    """
    fig = Figure()
    with pytest.raises(GMTTypeError):
        fig.legend(spec=["@Table_5_11.txt"])

    with pytest.raises(GMTTypeError):
        fig.legend(spec=[1, 2])
