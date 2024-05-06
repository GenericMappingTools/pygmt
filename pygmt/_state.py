"""
Private class to keep tracking of current PyGMT state.

The feature is only meant for internal use by PyGMT and is experimental!
"""

from dataclasses import dataclass


@dataclass
class _State:
    pass


_state = _State()
