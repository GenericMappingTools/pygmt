"""
Utilities for testing the modules and figures they generate.
"""
import os
import shutil
import functools

import pytest

from .. import psconvert


class DummyFigure():  # pylint: disable=too-few-public-methods
    """
    Not really a figure. Mocks the ``savefig`` method from matplotlib figures.

    Pretends to be a matploblib figure so that we can use pytest-mpl to compare
    generated images.

    ``savefig`` calls ``psconvert`` and moves the function to the file name
    given.
    """

    def __init__(self, image_prefix):
        self.image_prefix = image_prefix
        self.image_name = self.image_prefix + '.png'

    # pylint: disable=unused-argument
    def savefig(self, fname, *args, **kwargs):
        """
        Rename ``image`` to ``fname``. Ignores all other arguments.
        """
        psconvert(F=self.image_prefix, T='g', A=True, P=True)
        assert os.path.exists(self.image_name)
        shutil.move(self.image_name, fname)


def figure_comparison_test(test_func):
    """
    Make a test function compare the generated figure against a baseline.

    Use as a decorator::

        @figure_comparison_test
        def test_some_plot():
            "Tests some plotting command"
            figure()
            psbasemap(...)
            ...

    Uses ``pytest-mpl`` for the image comparison.

    Generate baseline images for a test by running::

        py.test --mpl-generate-path=baseline path/to/test_file.py

    Images will be in a ``baseline`` folder in the current directory.

    When you're satisfied with the baselines, copy them to the ``baseline``
    folder of the test folder.
    """
    prefix = test_func.__name__
    fmt = 'png'
    filename = '{}.{}'.format(prefix, fmt)

    @pytest.mark.mpl_image_compare(filename=filename)
    @functools.wraps(test_func)
    def new_test():
        "Test function with image comparison"
        test_func()
        # Return a dummy figure to fool pytest-mpl into thinking this is
        # maptlotlib.
        return DummyFigure(image_prefix=prefix)

    return new_test
