"""
Utilities for testing the modules and figures they generate.
"""
import os
import shutil
import pytest


class DummyFigure():  # pylint: disable=too-few-public-methods
    """
    Not really a figure. Mocks the ``savefig`` method from matplotlib figures.

    Pretends to be a matploblib figure so that we can use pytest-mpl to compare
    generated images.

    ``savefig`` renames the original figure file (``image``) to the given name
    and ignores all other arguments.
    """

    def __init__(self, image):
        self.image = image

    # pylint: disable=unused-argument
    def savefig(self, fname, *args, **kwargs):
        """
        Rename ``image`` to ``fname``. Ignores all other arguments.
        """
        shutil.move(self.image, fname)


def figure_comparison_test(test_func, **kwargs):
    """
    Make a test function compare the generated figure against a baseline.

    Use as a decorator::

        @figure_comparison_test
        def test_some_plot(prefix, fmt):
            "Tests some plotting command"
            begin(prefix=prefix, fmt=fmt)
            ...
            end()

    The test function must receive the ``prefix`` and ``fmt`` arguments and
    pass them along to ``gmt.begin`` or ``gmt.figure``.

    Uses ``pytest-mpl`` for the image comparison. You can pass any argument
    that ``pytest.mark.mpl_image_compare`` accepts to this decorator as well.

    Generate baseline images for a test by running::

        py.test --mpl-generate-path=baseline path/to/test_file.py

    Images will be in a ``baseline`` folder in the current directory.

    When you're satisfied with the baselines, copy them to the ``baseline``
    folder of the test folder.
    """

    if 'filename' not in kwargs:
        kwargs['filename'] = test_func.__name__ + '.png'

    @pytest.mark.mpl_image_compare(**kwargs)
    def new_test():
        "Test function with image comparison"
        prefix = test_func.__name__
        fmt = 'png'
        fname = '{}.{}'.format(prefix, fmt)
        test_func(prefix, fmt)
        assert os.path.exists(fname)
        # Return a dummy figure to fool pytest-mpl into thinking this is
        # maptlotlib.
        return DummyFigure(image=fname)

    return new_test
