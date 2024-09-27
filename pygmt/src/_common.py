"""
Common functions used in multiple PyGMT functions/methods.
"""

from pathlib import Path
from typing import Any

from pygmt.src.which import which


def _data_geometry_is_point(data: Any, kind: str) -> bool:
    """
    Check if the geometry of the input data is Point or MultiPoint.

    The inptu data can be a GeoJSON object or a OGR_GMT file.

    This function is used in ``Figure.plot`` and ``Figure.plot3d``.

    Parameters
    ----------
    data
        The data being plotted.
    kind
        The data kind.

    Returns
    -------
    bool
        ``True`` if the geometry is Point/MultiPoint, ``False`` otherwise.
    """
    if kind == "geojson" and data.geom_type.isin(["Point", "MultiPoint"]).all():
        return True
    if kind == "file" and str(data).endswith(".gmt"):  # OGR_GMT file
        try:
            with Path(which(data)).open(encoding="utf-8") as file:
                line = file.readline()
            if "@GMULTIPOINT" in line or "@GPOINT" in line:
                return True
        except FileNotFoundError:
            pass
    return False
