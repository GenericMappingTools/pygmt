"""
Test the behaviors of the Figure class
Doesn't include the plotting commands, which have their own test files.
"""
import os

import pytest

from .. import Figure
from ..figure import _unique_name


def test_figure_unique_name():
    "Make sure the figure name starts with gmt-python-"
    name = _unique_name()
    assert name.startswith('gmt-python-')


def test_figure_savefig_exists():
    "Make sure the saved figure has the right name"
    fig = Figure()
    fig.psbasemap(region='10/70/-300/800', J='X3i/5i', B='af',
                  D='30/35/-200/500', F=True)
    prefix = 'test_figure_savefig_exists'
    for fmt in 'png pdf jpg bmp eps tif'.split():
        fname = '.'.join([prefix, fmt])
        fig.savefig(fname)
        assert os.path.exists(fname)
        os.remove(fname)


def test_figure_savefig_transparent():
    "Check if fails when transparency is not supported"
    fig = Figure()
    fig.psbasemap(region='10/70/-300/800', J='X3i/5i', B='af',
                  D='30/35/-200/500', F=True)
    prefix = 'test_figure_savefig_transparent'
    for fmt in 'pdf jpg bmp eps tif'.split():
        fname = '.'.join([prefix, fmt])
        with pytest.raises(AssertionError):
            fig.savefig(fname, transparent=True)
    # png should not raise an error
    fname = '.'.join([prefix, 'png'])
    fig.savefig(fname, transparent=True)
    assert os.path.exists(fname)
    os.remove(fname)


def test_figure_savefig():
    "Check if the arguments being passed to psconvert are correct"
    kwargs_saved = []

    def mock_psconvert(*args, **kwargs):  # pylint: disable=unused-argument
        "Just record the arguments"
        kwargs_saved.append(kwargs)

    fig = Figure()
    fig.psconvert = mock_psconvert

    prefix = 'test_figure_savefig'

    fname = '.'.join([prefix, 'png'])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt='g', crop=True,
                                    portrait=True)

    fname = '.'.join([prefix, 'pdf'])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt='f', crop=True,
                                    portrait=True)

    fname = '.'.join([prefix, 'png'])
    fig.savefig(fname, transparent=True)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt='G', crop=True,
                                    portrait=True)

    fname = '.'.join([prefix, 'eps'])
    fig.savefig(fname, orientation='landscape')
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt='e', crop=True,
                                    portrait=False)


def test_figure_show():
    "Test that show creates the correct file name and deletes the temp dir"
    fig = Figure()
    fig.psbasemap(R='10/70/-300/800', J='X3i/5i', B='af',
                  D='30/35/-200/500', F=True)
    img = fig.show(width=800, return_img=True)
    assert os.path.split(img.filename)[-1] == 'gmt-figure-for-notebook.png'
    assert not os.path.exists(img.filename)
    assert img.width == 800
