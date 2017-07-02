"""
Test the session management modules.
"""
import os

from .. import begin, end  # , figure
from ...clib import call_module, create_session


def test_session_defaults():
    "Run a command inside a begin-end modern mode block."
    begin(prefix='test_session_defaults')
    session = create_session()
    call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()
    print(os.path.abspath('.'))
    assert os.path.exists('test_session_defaults.pdf')


def test_session_format():
    "Run a command inside a begin-end modern mode block and specify a format."
    begin(prefix='test_session_format', fmt='png')
    session = create_session()
    call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()
    assert os.path.exists('test_session_format.png')


# def test_session_figure():
    # "Run a figure command inside a begin-end modern mode block."
    # begin(prefix='test_session_figure')
    # figure(prefix='test_session_figure_for_real', formats='png')
    # session = create_session()
    # call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    # end()
    # assert os.path.exists('test_session_figure_for_real.png')
    # assert not os.path.exists('test_session_figure.pdf')
