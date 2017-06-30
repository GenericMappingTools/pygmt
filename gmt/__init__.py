"""
GMT Python interface
"""
from ._version import get_versions

# Import modules to make the high-level GMT Python API
from .modules import pscoast


__version__ = get_versions()['version']
del get_versions
