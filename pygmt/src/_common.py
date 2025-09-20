"""
Common functions used in multiple PyGMT functions/methods.
"""

from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar, Literal

from pygmt.exceptions import GMTValueError
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


class _FocalMechanismConventionCode(StrEnum):
    """
    Enum to handle focal mechanism convention codes.

    The enum names are in the format of ``CONVENTION_COMPONENT``, where ``CONVENTION``
    is the focal mechanism convention and ``COMPONENT`` is the component of the seismic
    moment tensor to plot. The enum values are the single-letter codes that can be used
    in meca/coupe's ``-S`` option.

    For some conventions, ``COMPONENT`` is not applicable, but we still define the enums
    to simplify the code logic.
    """

    AKI_DC = "a"
    AKI_DEVIATORIC = "a"
    AKI_FULL = "a"
    GCMT_DC = "c"
    GCMT_DEVIATORIC = "c"
    GCMT_FULL = "c"
    PARTIAL_DC = "p"
    PARTIAL_DEVIATORIC = "p"
    PARTIAL_FULL = "p"
    MT_DC = "d"
    MT_DEVIATORIC = "z"
    MT_FULL = "m"
    PRINCIPAL_AXIS_DC = "y"
    PRINCIPAL_AXIS_DEVIATORIC = "t"
    PRINCIPAL_AXIS_FULL = "x"


class _FocalMechanismConvention:
    """
    Class to handle focal mechanism convention, code, and associated parameters.

    Examples
    --------
    >>> from pygmt.src._common import _FocalMechanismConvention

    >>> conv = _FocalMechanismConvention("aki")
    >>> conv.code
    <_FocalMechanismConventionCode.AKI_DC: 'a'>
    >>> conv.params
    ['strike', 'dip', 'rake', 'magnitude']

    >>> conv = _FocalMechanismConvention("mt")
    >>> conv.code
    <_FocalMechanismConventionCode.MT_FULL: 'm'>
    >>> conv.params
    ['mrr', 'mtt', 'mff', 'mrt', 'mrf', 'mtf', 'exponent']

    >>> conv = _FocalMechanismConvention("mt", component="dc")
    >>> conv.code
    <_FocalMechanismConventionCode.MT_DC: 'd'>
    >>> conv.params
    ['mrr', 'mtt', 'mff', 'mrt', 'mrf', 'mtf', 'exponent']

    >>> conv = _FocalMechanismConvention("a")
    >>> conv.code
    <_FocalMechanismConventionCode.AKI_DC: 'a'>
    >>> conv.params
    ['strike', 'dip', 'rake', 'magnitude']

    >>> conv = _FocalMechanismConvention.from_params(
    ...     ["strike", "dip", "rake", "magnitude"]
    ... )
    >>> conv.code
    <_FocalMechanismConventionCode.AKI_DC: 'a'>

    >>> conv = _FocalMechanismConvention(convention="invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid focal mechanism convention: ...

    >>> conv = _FocalMechanismConvention("mt", component="invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid focal mechanism convention: ...

    >>> _FocalMechanismConvention.from_params(["strike", "dip", "rake"])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid focal mechanism parameters: ...
    """

    # Mapping of focal mechanism conventions to their parameters.
    _params: ClassVar = {
        "aki": ["strike", "dip", "rake", "magnitude"],
        "gcmt": [
            "strike1",
            "dip1",
            "rake1",
            "strike2",
            "dip2",
            "rake2",
            "mantissa",
            "exponent",
        ],
        "partial": ["strike1", "dip1", "strike2", "fault_type", "magnitude"],
        "mt": ["mrr", "mtt", "mff", "mrt", "mrf", "mtf", "exponent"],
        "principal_axis": [
            "t_value",
            "t_azimuth",
            "t_plunge",
            "n_value",
            "n_azimuth",
            "n_plunge",
            "p_value",
            "p_azimuth",
            "p_plunge",
            "exponent",
        ],
    }

    def __init__(
        self,
        convention: Literal["aki", "gcmt", "partial", "mt", "principal_axis"],
        component: Literal["full", "deviatoric", "dc"] = "full",
    ):
        """
        Initialize the ``_FocalMechanismConvention`` object from ``convention`` and
        ``component``.

        If the convention is specified via a single-letter code, ``convention`` and
        ``component`` are determined from the code.

        Parameters
        ----------
        convention
            The focal mechanism convention. Valid values are:

            - ``"aki"``: Aki and Richards convention.
            - ``"gcmt"``: Global CMT (Centroid Moment Tensor) convention.
            - ``"partial"``: Partial focal mechanism convention.
            - ``"mt"``: Moment Tensor convention.
            - ``"principal_axis"``: Principal axis convention.
        component
            The component of the seismic moment tensor to plot. Valid values are:

            - ``"full"``: the full seismic moment tensor
            - ``"dc"``: the closest double couple defined from the moment tensor (zero
              trace and zero determinant)
            - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)

            Doesn't apply to the conventions ``"aki"``, ``"gcmt"``, and ``"partial"``.
        """
        # TODO(Python>=3.12): Simplify to "convention in _FocalMechanismConventionCode".
        if convention in _FocalMechanismConventionCode.__members__.values():
            # Convention is specified via the actual single-letter convention code.
            self.code = _FocalMechanismConventionCode(convention)
            # Parse the convention from the convention code name.
            self._convention = "_".join(self.code.name.split("_")[:-1]).lower()
        else:  # Convention is specified via "convention" and "component".
            name = f"{convention.upper()}_{component.upper()}"  # e.g., "AKI_DC"
            if name not in _FocalMechanismConventionCode.__members__:
                _value = f"convention='{convention}', component='{component}'"
                raise GMTValueError(_value, description="focal mechanism convention")
            self.code = _FocalMechanismConventionCode[name]
            self._convention = convention

    @property
    def params(self):
        """
        The parameters associated with the focal mechanism convention.
        """
        return self._params[self._convention]

    @classmethod
    def from_params(
        cls,
        params: Sequence[str],
        component: Literal["full", "deviatoric", "dc"] = "full",
    ) -> "_FocalMechanismConvention":
        """
        Create a _FocalMechanismConvention object from a sequence of parameters.

        The method checks if the given parameters are a superset of a supported focal
        mechanism convention to determine the convention. If the parameters are not
        sufficient to determine the convention, an exception is raised.

        Parameters
        ----------
        params
            Sequence of parameters to determine the focal mechanism convention. The
            order of the parameters does not matter.

        Returns
        -------
        _FocalMechanismConvention
            The _FocalMechanismConvention object.

        Raises
        ------
        GMTValueError
            If the focal mechanism convention cannot be determined from the given
            parameters.
        """
        for convention, param_list in cls._params.items():
            if set(param_list).issubset(set(params)):
                return cls(convention, component=component)  # type: ignore[arg-type]
        raise GMTValueError(params, description="focal mechanism parameters")
