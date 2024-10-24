import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_paragraph():
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    fig.paragraph(x=2, y=2, text="This is a long paragraph. " * 10, parwidth="3i")
    return fig
