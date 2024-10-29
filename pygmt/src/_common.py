"""
Common functions used in multiple PyGMT functions/methods.
"""

from pathlib import Path
from typing import Any, Literal

from pygmt.exceptions import GMTInvalidInput
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


def _parse_coastline_resolution(
    resolution: Literal["auto", "full", "high", "intermediate", "low", "crude", None],
    allow_auto: bool = False,
) -> str | None:
    """
    Parse the resolution parameter for coastline-related functions.

    Parameters
    ----------
    resolution
        The resolution of the coastline dataset to use. The available resolutions from
        highest to lowest are: ``"full"``, ``"high"``, ``"intermediate"``, ``"low"``,
        and ``"crude"``, which drops by 80% between levels.
    allow_auto
        Whether to allow the ``"auto"`` resolution.

    Returns
    -------
    str or None
        The parsed resolution value.

    Raises
    ------
    GMTInvalidInput
        If the resolution is invalid.

    Examples
    --------
    >>> _parse_coastline_resolution("full")
    "f"
    >>> _parse_coastline_resolution("f")
    "f"
    >>> _parse_coastline_resolution("auto", allow_auto=True)
    "a"
    >>> _parse_coastline_resolution("invalid")
    pygmt.exceptions.GMTInvalidInput: Invalid resolution: invalid. Valid values are ...
    >>> _parse_coastline_resolution(None)
    None
    >>> _parse_coastline_resolution("auto")
    pygmt.exceptions.GMTInvalidInput: Invalid resolution: auto. Valid values are ...
    """
    if resolution is None:
        return None

    valid_resolutions = {"full", "high", "intermediate", "low", "crude"}
    if allow_auto:
        valid_resolutions.add("auto")
    if resolution not in {*valid_resolutions, *[res[0] for res in valid_resolutions]}:
        msg = (
            f"Invalid resolution: {resolution}."
            f"Valid values are {', '.join(valid_resolutions)}."
        )
        raise GMTInvalidInput(msg)
    return resolution[0]
