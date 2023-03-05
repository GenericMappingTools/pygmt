"""
Test functions in __init__.
"""
import io

import pygmt


def test_show_versions():
    """
    Test pygmt.show_versions()
    """
    f = io.StringIO()
    pygmt.show_versions(file=f)
    assert "PyGMT information:" in f.getvalue()
    assert "System information:" in f.getvalue()
    assert "Dependency information:" in f.getvalue()
    assert "GMT library information:" in f.getvalue()
