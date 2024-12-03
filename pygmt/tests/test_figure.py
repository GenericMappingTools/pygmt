"""
Test the behavior of the Figure class.

Doesn't include the plotting commands which have their own test files.
"""

import importlib
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import numpy.testing as npt
import pytest
from pygmt import Figure, set_display
from pygmt.exceptions import GMTInvalidInput
from pygmt.figure import SHOW_CONFIG, _get_default_display_method
from pygmt.helpers import GMTTempFile

_HAS_IPYTHON = bool(importlib.util.find_spec("IPython"))
_HAS_RIOXARRAY = bool(importlib.util.find_spec("rioxarray"))


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


@pytest.mark.benchmark
def test_figure_repr():
    """
    Make sure that figure output's PNG and HTML printable representations look ok.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 2, 3], frame=True)
    # Check that correct PNG 8-byte file header is produced
    # https://en.wikipedia.org/wiki/Portable_Network_Graphics#File_header
    repr_png = fig._repr_png_()
    assert repr_png.hex().startswith("89504e470d0a1a0a")
    # Check that correct HTML image tags are produced
    repr_html = fig._repr_html_()
    assert repr_html.startswith('<img src="data:image/png;base64,')
    assert repr_html.endswith('" width="500px">')


def test_figure_savefig_exists():
    """
    Make sure the saved figure has the right name.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    prefix = "test_figure_savefig_exists"
    for fmt in "bmp eps jpg jpeg pdf png ppm tif PNG JPG JPEG Png".split():
        fname = Path(f"{prefix}.{fmt}")
        fig.savefig(fname)
        assert fname.exists()
        fname.unlink()


def test_figure_savefig_geotiff():
    """
    Make sure .tif generates a normal TIFF file and .tiff generates a GeoTIFF file.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="M10c", frame=True)

    # Save as GeoTIFF
    geofname = Path("test_figure_savefig_geotiff.tiff")
    fig.savefig(geofname)
    assert geofname.exists()
    # The .pgw file should not exist
    assert not geofname.with_suffix(".pgw").exists()

    # Save as TIFF
    fname = Path("test_figure_savefig_tiff.tif")
    fig.savefig(fname)
    assert fname.exists()

    # Check if a TIFF is georeferenced or not
    if _HAS_RIOXARRAY:
        import rioxarray
        from rasterio.errors import NotGeoreferencedWarning
        from rasterio.transform import Affine

        # GeoTIFF
        with rioxarray.open_rasterio(geofname) as xds:
            assert xds.rio.crs is not None
            npt.assert_allclose(
                actual=xds.rio.bounds(),
                desired=(
                    -661136.0621116752,
                    -54631.82709660966,
                    592385.4459661598,
                    1129371.7360144067,
                ),
            )
            assert xds.rio.shape == (1257, 1331)
            assert xds.rio.transform() == Affine(
                a=941.789262267344,
                b=0.0,
                c=-661136.0621116752,
                d=0.0,
                e=-941.92805338983,
                f=1129371.7360144067,
            )
        # TIFF
        with pytest.warns(expected_warning=NotGeoreferencedWarning) as record:
            with rioxarray.open_rasterio(fname) as xds:
                assert xds.rio.crs is None
                npt.assert_allclose(
                    actual=xds.rio.bounds(), desired=(0.0, 0.0, 1331.0, 1257.0)
                )
                assert xds.rio.shape == (1257, 1331)
                assert xds.rio.transform() == Affine(
                    a=1.0, b=0.0, c=0.0, d=0.0, e=1.0, f=0.0
                )
            assert len(record) == 1
    geofname.unlink()
    fname.unlink()


def test_figure_savefig_directory_nonexists():
    """
    Make sure that Figure.savefig() raises a FileNotFoundError when the parent directory
    doesn't exist.
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
    fname = "test_figure_savefig_unknown_extension.test"
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
        fname = f"{prefix}.{fmt}"
        with pytest.raises(GMTInvalidInput):
            fig.savefig(fname, transparent=True)

    # PNG should support transparency and should not raise an error.
    fname = Path(f"{prefix}.png")
    fig.savefig(fname, transparent=True)
    assert fname.exists()
    fname.unlink()

    # The companion PNG file with KML format should also support transparency.
    fname = Path(f"{prefix}.kml")
    fig.savefig(fname, transparent=True)
    assert fname.exists()
    fname.unlink()
    assert fname.with_suffix(".png").exists()
    fname.with_suffix(".png").unlink()


def test_figure_savefig_filename_with_spaces():
    """
    Check if savefig (or psconvert) supports filenames with spaces.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    with GMTTempFile(prefix="pygmt-filename with spaces", suffix=".png") as imgfile:
        fig.savefig(fname=imgfile.name)
        imgpath = Path(imgfile.name).resolve()
        assert r"\040" not in str(imgpath)
        assert imgpath.stat().st_size > 0


def test_figure_savefig():
    """
    Check if the arguments being passed to psconvert are correct.
    """
    prefix = "test_figure_savefig"
    common_kwargs = {"prefix": prefix, "crop": True, "Qt": 2, "Qg": 2}
    expected_kwargs = {
        "png": {"fmt": "g", **common_kwargs},
        "pdf": {"fmt": "f", **common_kwargs},
        "eps": {"fmt": "e", **common_kwargs},
        "kml": {"fmt": "g", "W": "+k", **common_kwargs},
    }

    with patch.object(Figure, "psconvert") as mock_psconvert:
        fig = Figure()
        for fmt, expected in expected_kwargs.items():
            fig.savefig(f"{prefix}.{fmt}")
            mock_psconvert.assert_called_with(**expected)

        fig.savefig(f"{prefix}.png", transparent=True)
        mock_psconvert.assert_called_with(fmt="G", **common_kwargs)


def test_figure_savefig_worldfile():
    """
    Check if a world file is created for supported formats and raise an error for
    unsupported formats.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    # supported formats
    for fmt in [".bmp", ".jpg", ".png", ".ppm", ".tif"]:
        with GMTTempFile(prefix="pygmt-worldfile", suffix=fmt) as imgfile:
            fig.savefig(fname=imgfile.name, worldfile=True)
            assert Path(imgfile.name).stat().st_size > 0
            worldfile_suffix = "." + fmt[1] + fmt[3] + "w"
            assert Path(imgfile.name).with_suffix(worldfile_suffix).stat().st_size > 0
    # unsupported formats
    for fmt in [".eps", ".kml", ".pdf", ".tiff"]:
        with GMTTempFile(prefix="pygmt-worldfile", suffix=fmt) as imgfile:
            with pytest.raises(GMTInvalidInput):
                fig.savefig(fname=imgfile.name, worldfile=True)


def test_figure_savefig_show():
    """
    Check if the external viewer is launched when the show parameter is specified.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    prefix = "test_figure_savefig_show"
    with patch("pygmt.figure.launch_external_viewer") as mock_viewer:
        with GMTTempFile(prefix=prefix, suffix=".png") as imgfile:
            fig.savefig(imgfile.name, show=True)
        assert mock_viewer.call_count == 1


@pytest.mark.skipif(not _HAS_IPYTHON, reason="run when IPython is installed")
def test_figure_show():
    """
    Test that show creates the correct file name and deletes the temp dir.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    fig.show()


def test_figure_show_invalid_method():
    """
    Test to check if an error is raised when an invalid method is passed to show.
    """
    fig = Figure()
    fig.basemap(region="10/70/-300/800", projection="X3i/5i", frame="af")
    with pytest.raises(GMTInvalidInput):
        fig.show(method="test")


@pytest.mark.skipif(_HAS_IPYTHON, reason="run without IPython installed")
def test_figure_show_notebook_error_without_ipython():
    """
    Test to check if an error is raised when display method is 'notebook', but IPython
    is not installed.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 2, 3], frame=True)
    with pytest.raises(ImportError):
        fig.show(method="notebook")


def test_figure_display_external():
    """
    Test to check that a figure can be displayed in an external window.
    """
    fig = Figure()
    fig.basemap(region=[0, 3, 6, 9], projection="X1c", frame=True)
    fig.show(method="external")


class TestSetDisplay:
    """
    Test the pygmt.set_display method.
    """

    def test_set_display(self):
        """
        Test if pygmt.set_display updates the SHOW_CONFIG variable correctly and
        Figure.show opens the preview image in the correct way.
        """
        default_method = SHOW_CONFIG["method"]  # Store the current default method.

        fig = Figure()
        fig.basemap(region=[0, 3, 6, 9], projection="X1c", frame=True)

        # Test the "notebook" display method.
        set_display(method="notebook")
        assert SHOW_CONFIG["method"] == "notebook"
        if _HAS_IPYTHON:
            with (
                patch("IPython.display.display") as mock_display,
                patch("pygmt.figure.launch_external_viewer") as mock_viewer,
            ):
                fig.show()
                assert mock_viewer.call_count == 0
                assert mock_display.call_count == 1
        else:
            with pytest.raises(ImportError):
                fig.show()

        # Test the "external" display method
        set_display(method="external")
        assert SHOW_CONFIG["method"] == "external"
        with patch("pygmt.figure.launch_external_viewer") as mock_viewer:
            fig.show()
            assert mock_viewer.call_count == 1
        if _HAS_IPYTHON:
            with patch("IPython.display.display") as mock_display:
                fig.show()
                assert mock_display.call_count == 0

        # Test the "none" display method.
        set_display(method="none")
        assert SHOW_CONFIG["method"] == "none"
        with patch("pygmt.figure.launch_external_viewer") as mock_viewer:
            fig.show()
            assert mock_viewer.call_count == 0
        if _HAS_IPYTHON:
            with patch("IPython.display.display") as mock_display:
                fig.show()
                assert mock_display.call_count == 0

        # Setting method to None should revert it to the default method.
        set_display(method=None)
        assert SHOW_CONFIG["method"] == default_method

    def test_invalid_method(self):
        """
        Test if an error is raised when an invalid method is passed.
        """
        with pytest.raises(GMTInvalidInput):
            set_display(method="invalid")


class TestGetDefaultDisplayMethod:
    """
    Test the _get_default_display_method function.
    """

    def test_default_display_method(self, monkeypatch):
        """
        Default display method is "external" if PYGMT_USE_EXTERNAL_DISPLAY is undefined.
        """
        monkeypatch.delenv("PYGMT_USE_EXTERNAL_DISPLAY", raising=False)
        assert _get_default_display_method() == "external"

    def test_disable_external_display(self, monkeypatch):
        """
        Setting PYGMT_USE_EXTERNAL_DISPLAY to "false" should disable external display.
        """
        monkeypatch.setenv("PYGMT_USE_EXTERNAL_DISPLAY", "false")
        assert _get_default_display_method() == "none"

    @pytest.mark.skipif(not _HAS_IPYTHON, reason="Run when IPython is installed")
    def test_notebook_display(self):
        """
        Default display method is "notebook" when an IPython kernel is running.
        """
        # Mock IPython.get_ipython() to return an object with a config attribute,
        # so PyGMT can detect that an IPython kernel is running.
        with patch(
            "IPython.get_ipython", return_value=Mock(config={"IPKernelApp": True})
        ):
            # Display method should be "notebook" when an IPython kernel is running.
            assert _get_default_display_method() == "notebook"

            # PYGMT_USE_EXTERNAL_DISPLAY should not affect notebook display.
            with patch.dict("os.environ", {"PYGMT_USE_EXTERNAL_DISPLAY": "false"}):
                assert _get_default_display_method() == "notebook"
