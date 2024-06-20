"""
PyGMT is a library for processing geospatial and geophysical data and making
publication-quality maps and figures. It provides a Pythonic interface for the Generic
Mapping Tools (GMT), a command-line program widely used across the Earth, Ocean, and
Planetary sciences and beyond. Besides making GMT more accessible to new users, PyGMT
aims to provide integration with the PyData ecosystem as well as support for rich
display in Jupyter notebooks.

Main Features
-------------
Here are just a few of the things that PyGMT does well:

  - Easy handling of individual types of data like Cartesian, geographic, or
    time-series data.
  - Processing of (geo)spatial data including gridding, filtering, and masking.
  - Plotting of a large spectrum of objects on figures including
    lines, vectors, polygons, and symbols (pre-defined and customized).
  - Generating publication-quality illustrations and making animations.
"""

import atexit as _atexit

# Import modules to make the high-level GMT Python API
from pygmt import datasets
from pygmt._show_versions import __commit__, __version__, show_versions
from pygmt.accessors import GMTDataArrayAccessor
from pygmt.figure import Figure, set_display
from pygmt.io import load_dataarray
from pygmt.session_management import begin as _begin
from pygmt.session_management import end as _end
from pygmt.src import (
    binstats,
    blockmean,
    blockmedian,
    blockmode,
    config,
    dimfilter,
    filter1d,
    grd2cpt,
    grd2xyz,
    grdclip,
    grdcut,
    grdfill,
    grdfilter,
    grdgradient,
    grdhisteq,
    grdinfo,
    grdlandmask,
    grdproject,
    grdsample,
    grdtrack,
    grdvolume,
    info,
    makecpt,
    nearneighbor,
    project,
    select,
    sph2grd,
    sphdistance,
    sphinterpolate,
    surface,
    triangulate,
    which,
    x2sys_cross,
    x2sys_init,
    xyz2grd,
)

# Start our global modern mode session
_begin()
# Tell Python to run _end when shutting down
_atexit.register(_end)
