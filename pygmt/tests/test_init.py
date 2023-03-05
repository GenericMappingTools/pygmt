"""
Test functions in __init__.
"""
import io

import pygmt


def test_show_versions():
    """
    Check that pygmt.show_versions() reports version information from PyGMT,
    the operating system, dependencies and the GMT library.
    """
    buf = io.StringIO()
    pygmt.show_versions(file=buf)
    assert "PyGMT information:" in buf.getvalue()
    assert "System information:" in buf.getvalue()
    assert "Dependency information:" in buf.getvalue()
    assert "GMT library information:" in buf.getvalue()
