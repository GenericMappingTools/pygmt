"""
Test the pygmt.show_versions function.
"""

import io
from unittest.mock import patch

import pygmt
import pytest


def test_show_versions():
    """
    Check that pygmt.show_versions reports version information of PyGMT, the operating
    system, dependencies and the GMT library.
    """
    buf = io.StringIO()
    pygmt.show_versions(file=buf)
    output = buf.getvalue()

    assert "PyGMT information:" in output
    assert "System information:" in output
    assert "Dependency information:" in output
    assert "GMT library information:" in output
    assert "WARNING:" not in output  # No GMT-Ghostscript incompatibility warnings.


@pytest.mark.parametrize(
    ("gs_version", "gmt_version"),
    [
        ("9.52", "6.4.0"),
        ("10.01", "6.4.0"),
        ("10.02", "6.4.0"),
        (None, "6.5.0"),
    ],
)
def test_show_versions_ghostscript_warnings(gs_version, gmt_version):
    """
    Check that pygmt.show_versions reports warnings for GMT-Ghostscript incompatibility.
    """
    with (
        patch("pygmt._show_versions.__gmt_version__", gmt_version),
        patch("pygmt._show_versions._get_ghostscript_version", return_value=gs_version),
    ):
        buf = io.StringIO()
        pygmt.show_versions(file=buf)
        assert "WARNING:" in buf.getvalue()


def test_show_versions_ghostscript_unsupported_os():
    """
    Check that pygmt.show_versions reports ghostscript version is None for an
    unsupported operating system.
    """
    with patch("sys.platform", new="unsupported_os"):
        buf = io.StringIO()
        pygmt.show_versions(file=buf)
        assert "ghostscript: None" in buf.getvalue()
        assert "WARNING:" in buf.getvalue()


def test_show_versions_ghostscript_not_found():
    """
    Check that pygmt.show_versions reports ghostscript version is None when ghostscript
    is not found in the system.
    """
    with patch("shutil.which", return_value=None):
        buf = io.StringIO()
        pygmt.show_versions(file=buf)
        assert "ghostscript: None" in buf.getvalue()
        assert "WARNING:" in buf.getvalue()
