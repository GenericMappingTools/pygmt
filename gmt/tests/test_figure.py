"""
Test the behaviors of the Figure class
Doesn't include the plotting commands, which have their own test files.
"""
import os

from .. import Figure


def test_figure_show():
    "Test that show creates the correct file name and deletes the temp dir"
    fig = Figure()
    fig.psbasemap(R='10/70/-300/800', J='X3i/5i', B='af',
                  D='30/35/-200/500', F=True)
    img = fig.show(width=800, return_img=True)
    assert os.path.split(img.filename)[-1] == 'gmt-figure-for-notebook.png'
    assert not os.path.exists(img.filename)
    assert img.width == 800
