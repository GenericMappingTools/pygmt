# pylint: disable=unused-argument
"""
Tests for x2sys_init.
"""
import os
from tempfile import TemporaryDirectory

import pytest
from pygmt import x2sys_init


@pytest.fixture(name="mock_x2sys_home")
def fixture_mock_x2sys_home(monkeypatch):
    """
    Set the X2SYS_HOME environment variable to the current working directory
    for the test session.
    """
    monkeypatch.setenv("X2SYS_HOME", os.getcwd())


def test_x2sys_init_region_spacing(mock_x2sys_home):
    """
    Test that x2sys_init's region (R) and spacing (I) sequence arguments accept
    a list properly.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(
            tag=tag, fmtfile="xyz", force=True, region=[0, 10, 20, 30], spacing=[5, 5]
        )

        with open(os.path.join(tmpdir, f"{tag}.tag"), "r") as tagpath:
            tail_line = tagpath.readlines()[-1]
            assert "-R0/10/20/30" in tail_line
            assert "-I5/5" in tail_line


def test_x2sys_init_units_gap(mock_x2sys_home):
    """
    Test that x2sys_init's units (N) and gap (W) arguments accept a list
    properly.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(
            tag=tag,
            fmtfile="xyz",
            force=True,
            units=["de", "se"],
            gap=["tseconds", "de"],
        )

        with open(os.path.join(tmpdir, f"{tag}.tag"), "r") as tagpath:
            tail_line = tagpath.readlines()[-1]
            assert "-Nse -Nde" in tail_line
            assert "-Wtseconds -Wde" in tail_line
