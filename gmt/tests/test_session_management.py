"""
Test the session management modules.
"""
import os

from .. import begin, end, figure
from ..clib import call_module, create_session
from .utils import figure_comparison_test


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@figure_comparison_test
def test_session(prefix, fmt):
    "Run a command inside a begin-end modern mode block."
    begin(prefix=prefix, fmt=fmt)
    session = create_session()
    call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()


@figure_comparison_test
def test_session_figure(prefix, fmt):
    "Run a figure command inside a begin-end modern mode block."
    begin()
    figure(prefix=prefix, formats=fmt)
    session = create_session()
    call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    # Plot some points with red circles
    data_file = os.path.join(TEST_DATA_DIR, 'points.txt')
    call_module(session, 'psxy', '-<{} -Sc -Gred'.format(data_file))
    end()
