"""
Extra modules that are exclusive to the Python API (for things like the Jupyter
notebook or simpler interfaces).
"""
import tempfile
import os

try:
    from IPython.display import Image, display
except ImportError:
    Image, display = None, None

from . import psconvert


def show(dpi=100, width=500, return_img=False):
    """
    Display the last figure in the Jupyter notebook

    You will need to have IPython installed for this to work. You should have
    it if you are using a Jupyter notebook.

    Parameters
    ----------
    dpi : int
        The image resolution (dots per inch).
    width : int
        Width of the figure shown in the notebook in pixels.
    return_img : bool
        Whether or not to return the IPython.display.Image variable.

    """
    assert Image is not None and display is not None, \
        "Couldn't find IPython. Please make sure it's installed."
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = os.path.join(tmpdir, 'gmt-figure-for-notebook')
        fname = prefix + '.png'
        psconvert(prefix=prefix, fmt='G', dpi=dpi,
                  crop=True, portrait=True)
        img = Image(filename=fname, embed=True, width=width)
        display(img)
    if return_img:
        return img
