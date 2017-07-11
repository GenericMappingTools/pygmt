"""
Test some of the extra modules from the Python API
"""
import os

from ..extra_modules import show
from .. import figure, psbasemap


def test_show():
    "Test that show creates the correct file name and deletes the temp dir"
    figure()
    psbasemap(R='10/70/-300/800', J='X3i/5i', B='af',
              D='30/35/-200/500', F=True)
    img = show(width=800, return_img=True)
    assert os.path.split(img.filename)[-1] == 'gmt-figure-for-notebook.png'
    assert not os.path.exists(img.filename)
    assert img.width == 800
