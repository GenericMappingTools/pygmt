"""
Test the Figure clipping context managers.
"""

from unittest.mock import Mock

import pytest
from pygmt.exceptions import GMTParameterError
from pygmt.src.clip import (
    clip_dcw,
    clip_land,
    clip_mask,
    clip_polygon,
    clip_solar,
    clip_water,
)


class _FakeVirtualFile:
    """
    Minimal context manager that mimics a GMT virtual file handle.
    """

    def __enter__(self):
        return "fake-virtual-file"

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class _FakeSession:
    """
    Capture virtual file and module calls made by the clipping contexts.
    """

    def __init__(self, calls):
        self._calls = calls

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def virtualfile_in(self, **kwargs):
        self._calls.append(("virtualfile_in", kwargs))
        return _FakeVirtualFile()

    def call_module(self, module, args):
        self._calls.append(("call_module", module, args))


def test_clip_context_manager_activation_and_deactivation():
    """
    Figure clipping context managers should activate and deactivate clipping.
    """
    figure = Mock()
    clip = clip_land(figure, projection="W15c")

    with clip:
        pass

    assert figure._activate_figure.call_count == 2
    figure.coast.assert_any_call(land=True, projection="W15c")
    figure.coast.assert_any_call(Q=True)


@pytest.mark.parametrize(
    "kwargs",
    [{"fill": "red"}, {"G": "red"}, {"frame": True}, {"B": "af"}],
)
def test_clip_solar_rejects_fill_and_frame(kwargs):
    """
    Figure.clip_solar should reject plotting-only parameters up front.
    """
    with pytest.raises(GMTParameterError, match="Figure.clip_solar does not support"):
        clip_solar(Mock(), **kwargs)


@pytest.mark.parametrize(
    ("method", "kwargs"),
    [
        ("land", {"land": "gray"}),
        ("land", {"G": "gray"}),
        ("water", {"water": "skyblue"}),
        ("water", {"S": "skyblue"}),
    ],
)
def test_clip_coast_methods_reject_duplicate_clip_parameters(method, kwargs):
    """
    Figure coast-based clip methods should reject parameters they own internally.
    """
    funcs = {
        "land": clip_land,
        "water": clip_water,
    }
    msg = f"Figure.clip_{method} does not support"
    with pytest.raises(GMTParameterError, match=msg):
        funcs[method](Mock(), **kwargs)


def test_clip_dcw_rejects_duplicate_dcw_keyword():
    """
    Figure.clip_dcw should reject duplicate dcw parameters.
    """
    with pytest.raises(GMTParameterError, match="Figure.clip_dcw does not support"):
        clip_dcw(Mock(), code="JP", dcw="US")


def test_clip_mask_passes_xy_to_virtualfile(monkeypatch):
    """
    Figure.clip_mask should pass x/y arrays through to Session.virtualfile_in.
    """
    calls = []
    monkeypatch.setattr("pygmt.src.clip.Session", lambda: _FakeSession(calls))

    with clip_mask(Mock(), x=[1, 2], y=[3, 4], spacing="1d", radius="5k"):
        pass

    assert calls[0] == ("virtualfile_in", {"data": None, "x": [1, 2], "y": [3, 4]})
    assert [call[1] for call in calls if call[0] == "call_module"] == ["mask", "mask"]


def test_clip_polygon_passes_xy_to_virtualfile(monkeypatch):
    """
    Figure.clip_polygon should pass x/y arrays through to Session.virtualfile_in.
    """
    calls = []
    monkeypatch.setattr("pygmt.src.clip.Session", lambda: _FakeSession(calls))

    with clip_polygon(Mock(), x=[1, 2], y=[3, 4]):
        pass

    assert calls[0] == ("virtualfile_in", {"data": None, "x": [1, 2], "y": [3, 4]})
    assert [call[1] for call in calls if call[0] == "call_module"] == ["clip", "clip"]
