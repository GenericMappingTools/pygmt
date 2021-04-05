"""
Tests for legend.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.mark.mpl_image_compare
def test_legend_position():
    """
    Test that plots a position with each of the four legend coordinate systems.
    """

    fig = Figure()
    fig.basemap(region=[-2, 2, -2, 2], frame=True)
    positions = ["jTR+jTR", "g0/1", "n0.2/0.2", "x4i/2i/2i"]
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


@pytest.mark.mpl_image_compare
def test_legend_entries():
    """
    Test different marker types/shapes.
    """
    fig = Figure()
    fig.basemap(projection="x1i", region=[0, 7, 3, 7], frame=True)
    fig.plot(
        data="@Table_5_11.txt",
        style="c0.15i",
        color="lightgreen",
        pen="faint",
        label="Apples",
    )
    fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", label='"My lines"')
    fig.plot(data="@Table_5_11.txt", style="t0.15i", color="orange", label="Oranges")
    fig.legend(position="JTR+jTR")

    return fig


@pytest.mark.mpl_image_compare
def test_legend_specfile():
    """
    Test specfile functionality.
    """

    specfile_contents = """
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

    with GMTTempFile() as specfile:
        with open(specfile.name, "w") as file:
            file.write(specfile_contents)
        fig = Figure()
        fig.basemap(projection="x6i", region=[0, 1, 0, 1], frame=True)
        fig.legend(specfile.name, position="JTM+jCM+w5i")
    return fig


def test_legend_fails():
    """
    Test legend fails with invalid spec.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.legend(spec=["@Table_5_11.txt"])
