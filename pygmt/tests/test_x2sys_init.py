"""
Test pygmt.x2sys_init.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pygmt import x2sys_init


@pytest.fixture(name="mock_x2sys_home")
def _fixture_mock_x2sys_home(monkeypatch):
    """
    Set the X2SYS_HOME environment variable to the current working directory for the
    test session.
    """
    monkeypatch.setenv("X2SYS_HOME", str(Path.cwd()))


@pytest.mark.usefixtures("mock_x2sys_home")
def test_x2sys_init_region_spacing():
    """
    Test that x2sys_init's region (R) and spacing (I) sequence arguments accept a list
    properly.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=Path.cwd()) as tmpdir:
        tmpdir_p = Path(tmpdir)
        tag = tmpdir_p.name
        x2sys_init(
            tag=tag, fmtfile="xyz", force=True, region=[0, 10, 20, 30], spacing=[5, 5]
        )
        tail_line = (tmpdir_p / f"{tag}.tag").read_text().splitlines()[-1]
        assert "-R0/10/20/30" in tail_line
        assert "-I5/5" in tail_line


@pytest.mark.benchmark
@pytest.mark.usefixtures("mock_x2sys_home")
def test_x2sys_init_units_gap():
    """
    Test that x2sys_init's units (N) and gap (W) arguments accept a list properly.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=Path.cwd()) as tmpdir:
        tmpdir_p = Path(tmpdir)
        tag = tmpdir_p.name
        x2sys_init(
            tag=tag,
            fmtfile="xyz",
            force=True,
            units=["de", "se"],
            gap=["tseconds", "de"],
        )

        tail_line = (tmpdir_p / f"{tag}.tag").read_text().splitlines()[-1]
        assert "-Nse -Nde" in tail_line
        assert "-Wtseconds -Wde" in tail_line
