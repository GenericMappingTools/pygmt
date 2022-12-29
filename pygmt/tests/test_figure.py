"""
Test the behavior of the Figure class.

Doesn't include the plotting commands which have their own test files.
"""
import os
from pathlib import Path

try:
    import IPython
except ModuleNotFoundError:
    IPython = None  # pylint: disable=invalid-name


import numpy as np
import numpy.testing as npt
import pytest
from pygmt import Figure, set_display
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import GMTTempFile


def test_figure_region():
    """
    Extract the plot region for the figure.
    """
    region = [0, 1, 2, 3]
    fig = Figure()
    fig.basemap(region=region, projection="X1id/1id", frame=True)
    npt.assert_allclose(fig.region, np.array(region))


def test_figure_region_multiple():
    """
    Make sure the region argument is for the current figure.
    """
    region1 = [-10, 2, 0.355, 67]
    fig1 = Figure()
    fig1.basemap(region=region1, projection="X1id/1id", frame=True)

    fig2 = Figure()
    fig2.basemap(region="g", projection="X3id/3id", frame=True)

    npt.assert_allclose(fig1.region, np.array(region1))
    npt.assert_allclose(fig2.region, np.array([0.0, 360.0, -90.0, 90.0]))


def test_figure_region_country_codes():
    """
    Extract the plot region for the figure using country codes.
    """
    fig = Figure()
    fig.basemap(region="JP", projection="M3i", frame=True)
    npt.assert_allclose(
        fig.region, np.array([122.938515, 145.820877, 20.528774, 45.523136])
    )
    fig = Figure()
    fig.basemap(region="g", projection="X3id/3id", frame=True)
    npt.assert_allclose(fig.region, np.array([0.0, 360.0, -90.0, 90.0]))


def test_figure_repr():
    """
    Make sure that figure output's PNG and HTML printable representations look
    ok.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 2, 3], frame=True)
    # Check that correct PNG 8-byte file header is produced
    # https://en.wikipedia.org/wiki/Portable_Network_Graphics#File_header
    repr_png = fig._repr_png_()  # pylint: disable=protected-access
    assert repr_png.hex().startswith("89504e470d0a1a0a")
    # Check that correct HTML image tags are produced
    repr_html = fig._repr_html_()  # pylint: disable=protected-access
    assert repr_html.startswith('<img src="data:image/png;base64,')
    assert repr_html.endswith('" width="500px">')


def test_figure_savefig_exists():
    """
    Make sure the saved figure has the right name.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    prefix = "test_figure_savefig_exists"
    for fmt in "png pdf jpg bmp eps tif".split():
        fname = ".".join([prefix, fmt])
        fig.savefig(fname)
        assert os.path.exists(fname)
        os.remove(fname)


def test_figure_savefig_directory_nonexists():
    """
    Make sure that Figure.savefig() raises a FileNotFoundError when the parent
    directory doesn't exist.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    with pytest.raises(FileNotFoundError, match="No such directory:"):
        fig.savefig("a-nonexist-directory/test_figure_savefig_directory_nonexists.png")


def test_figure_savefig_unknown_extension():
    """
    Check that an error is raised when an unknown extension is passed.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    prefix = "test_figure_savefig_unknown_extension"
    fmt = "test"
    fname = ".".join([prefix, fmt])
    with pytest.raises(GMTInvalidInput, match="Unknown extension '.test'."):
        fig.savefig(fname)


def test_figure_savefig_ps_extension():
    """
    Check that an error is raised when .ps extension is specified.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3c/5c", frame="af")
    fname = "test_figure_savefig_ps_extension.ps"
    with pytest.raises(GMTInvalidInput, match="Extension '.ps' is not supported."):
        fig.savefig(fname)


def test_figure_savefig_transparent():
    """
    Check if fails when transparency is not supported.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    prefix = "test_figure_savefig_transparent"
    for fmt in "pdf jpg bmp eps tif".split():
        fname = ".".join([prefix, fmt])
        with pytest.raises(GMTInvalidInput):
            fig.savefig(fname, transparent=True)
    # png should not raise an error
    fname = ".".join([prefix, "png"])
    fig.savefig(fname, transparent=True)
    assert os.path.exists(fname)
    os.remove(fname)


def test_figure_savefig_filename_with_spaces():
    """
    Check if savefig (or psconvert) supports filenames with spaces.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    with GMTTempFile(prefix="pygmt-filename with spaces", suffix=".png") as imgfile:
        fig.savefig(fname=imgfile.name)
        assert r"\040" not in os.path.abspath(imgfile.name)
        assert Path(imgfile.name).stat().st_size > 0


def test_figure_savefig():
    """
    Check if the arguments being passed to psconvert are correct.
    """
    kwargs_saved = []

    def mock_psconvert(*args, **kwargs):  # pylint: disable=unused-argument
        """
        Just record the arguments.
        """
        kwargs_saved.append(kwargs)

    fig = Figure()
    fig.psconvert = mock_psconvert

    prefix = "test_figure_savefig"

    fname = ".".join([prefix, "png"])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt="g", crop=True, Qt=2, Qg=2)

    fname = ".".join([prefix, "pdf"])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt="f", crop=True, Qt=2, Qg=2)

    fname = ".".join([prefix, "png"])
    fig.savefig(fname, transparent=True)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt="G", crop=True, Qt=2, Qg=2)

    fname = ".".join([prefix, "eps"])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(prefix=prefix, fmt="e", crop=True, Qt=2, Qg=2)

    fname = ".".join([prefix, "kml"])
    fig.savefig(fname)
    assert kwargs_saved[-1] == dict(
        prefix=prefix, fmt="g", crop=True, Qt=2, Qg=2, W="+k"
    )


@pytest.mark.skipif(IPython is None, reason="run when IPython is installed")
def test_figure_show():
    """
    Test that show creates the correct file name and deletes the temp dir.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    fig.show()


@pytest.mark.mpl_image_compare
def test_figure_shift_origin():
    """
    Test if fig.shift_origin works.
    """
    kwargs = dict(region=[0, 3, 0, 5], projection="X3c/5c", frame=0)
    fig = Figure()
    # First call shift_origin without projection and region.
    # Test issue https://github.com/GenericMappingTools/pygmt/issues/514
    fig.shift_origin(xshift="2c", yshift="3c")
    fig.basemap(**kwargs)
    fig.shift_origin(xshift="4c")
    fig.basemap(**kwargs)
    fig.shift_origin(yshift="6c")
    fig.basemap(**kwargs)
    fig.shift_origin(xshift="-4c", yshift="6c")
    fig.basemap(**kwargs)
    return fig


def test_figure_show_invalid_method():
    """
    Test to check if an error is raised when an invalid method is passed to
    show.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    with pytest.raises(GMTInvalidInput):
        fig.show(method="test")


@pytest.mark.skipif(IPython is not None, reason="run without IPython installed")
def test_figure_show_notebook_error_without_ipython():
    """
    Test to check if an error is raised when display method is 'notebook', but
    IPython is not installed.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 2, 3], frame=True)
    with pytest.raises(GMTError):
        fig.show(method="notebook")


def test_figure_display_external():
    """
    Test to check that a figure can be displayed in an external window.
    """
    fig = Figure()
    fig.basemap(region=[0, 3, 6, 9], projection="X1c", frame=True)
    fig.show(method="external")


def test_figure_set_display_invalid():
    """
    Test to check if an error is raised when an invalid method is passed to
    set_display.
    """
    with pytest.raises(GMTInvalidInput):
        set_display(method="invalid")


def test_figure_deprecated_xshift_yshift():
    """
    Check if deprecation of parameters X/Y/xshift/yshift work correctly if
    used.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    with pytest.warns(expected_warning=SyntaxWarning) as record:
        fig.plot(x=1, y=1, style="c3c", xshift="3c")
        assert len(record) == 1  # check that only one warning was raised
    with pytest.warns(expected_warning=SyntaxWarning) as record:
        fig.plot(x=1, y=1, style="c3c", X="3c")
        assert len(record) == 1  # check that only one warning was raised
    with pytest.warns(expected_warning=SyntaxWarning) as record:
        fig.plot(x=1, y=1, style="c3c", yshift="3c")
        assert len(record) == 1  # check that only one warning was raised
    with pytest.warns(expected_warning=SyntaxWarning) as record:
        fig.plot(x=1, y=1, style="c3c", Y="3c")
        assert len(record) == 1  # check that only one warning was raised
