"""
Test that Parameter 'PS_CONVERT' is not supported.
"""

import pytest
from pygmt import config

def test_config_ps_convert():
    """
    Test that Parameter 'PS_CONVERT' is not supported.
    """
    # Check that PS_CONVERT is removed from the autocomplete list
    assert "PS_CONVERT" not in config._keywords

    # Check that a warning is raised when PS_CONVERT is used in config
    msg = (
        "Parameter 'PS_CONVERT' is not supported. "
        "To confiure conversion options, please pass parameters to "
        "pygmt.Figure.savefig or pygmt.Figure.show instead."
    )
    with pytest.warns(SyntaxWarning, match=msg):
        config(PS_CONVERT="C")
