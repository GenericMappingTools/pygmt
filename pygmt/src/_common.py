"""
Common functions used in multiple PyGMT functions/methods.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Any, ClassVar, Literal

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


class _FocalMechanismConvention:
    """
    Class to handle focal mechanism convention, code, and associated parameters.

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

        - ``"full"``: the full tensor seismic moment tensor
        - ``"dc"``: the closest double coupe defined from the moment tensor (zero trace
          and zero determinant)
        - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)

        Only valid for conventions ``"mt"`` and ``"principal_axis"``.

    Attributes
    ----------
    convention
        The focal mechanism convention.
    params
        List of parameters associated with the focal mechanism convention.
    code
        The single-letter code that can be used in meca/coupe's -S option.

    Examples
    --------
    >>> from pygmt.src._common import _FocalMechanismConvention

    >>> conv = _FocalMechanismConvention("aki")
    >>> conv.convention, conv.code
    ('aki', 'a')
    >>> conv.params
    ['strike', 'dip', 'rake', 'magnitude']

    >>> conv = _FocalMechanismConvention("gcmt")
    >>> conv.convention, conv.code
    ('gcmt', 'c')
    >>> conv.params
    ['strike1', 'dip1', 'rake1', 'strike2', 'dip2', 'rake2', 'mantissa', 'exponent']

    >>> conv = _FocalMechanismConvention("partial")
    >>> conv.convention, conv.code
    ('partial', 'p')
    >>> conv.params
    ['strike1', 'dip1', 'strike2', 'fault_type', 'magnitude']

    >>> conv = _FocalMechanismConvention("mt", component="dc")
    >>> conv.convention, conv.code
    ('mt', 'd')
    >>> conv.params
    ['mrr', 'mtt', 'mff', 'mrt', 'mrf', 'mtf', 'exponent']

    >>> conv = _FocalMechanismConvention("principal_axis", component="deviatoric")
    >>> conv.convention, conv.code
    ('principal_axis', 't')

    >>> conv = _FocalMechanismConvention("a")
    >>> conv.convention, conv.code
    ('aki', 'a')

    >>> conv = _FocalMechanismConvention.from_params(
    ...     ["strike", "dip", "rake", "magnitude"]
    ... )
    >>> conv.convention, conv.code
    ('aki', 'a')

    >>> conv = _FocalMechanismConvention(convention="invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Invalid focal mechanism convention 'invalid'.

    >>> conv = _FocalMechanismConvention("mt", component="invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Invalid component 'invalid' for ... 'mt'.

    >>> _FocalMechanismConvention.from_params(["strike", "dip", "rake"])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Fail to determine ...
    """

    # Mapping of focal mechanism conventions to their single-letter codes.
    _conventions: ClassVar = {
        "aki": "a",
        "gcmt": "c",
        "partial": "p",
        "mt": {"full": "m", "deviatoric": "z", "dc": "d"},
        "principal_axis": {"full": "x", "deviatoric": "t", "dc": "y"},
    }

    # Mapping of single-letter codes to focal mechanism convention names
    _codes: ClassVar = {
        "a": "aki",
        "c": "gcmt",
        "p": "partial",
        "m": "mt",
        "z": "mt",
        "d": "mt",
        "x": "principal_axis",
        "t": "principal_axis",
        "y": "principal_axis",
    }

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
        Initialize the FocalMechanismConvention object.
        """
        if convention in self._conventions:
            # Convention is given via 'convention' and 'component' parameters.
            if component not in {"full", "deviatoric", "dc"}:
                msg = (
                    f"Invalid component '{component}' for focal mechanism convention "
                    f"'{convention}'."
                )
                raise GMTInvalidInput(msg)

            self.convention = convention
            self.code = self._conventions[convention]
            if isinstance(self.code, dict):
                self.code = self.code[component]
        elif convention in self._codes:
            # Convention is given as a single-letter code.
            self.code = convention
            self.convention = self._codes[convention]
        else:
            msg = f"Invalid focal mechanism convention '{convention}'."
            raise GMTInvalidInput(msg)
        self.params = self._params[self.convention]

    @staticmethod
    def from_params(
        params: Sequence[str], component: Literal["full", "deviatoric", "dc"] = "full"
    ) -> "_FocalMechanismConvention":
        """
        Create a FocalMechanismConvention object from a sequence of parameters.

        The method checks if the given parameters are a superset of a known focal
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
            The FocalMechanismConvention object.

        Raises
        ------
        GMTInvalidInput
            If the focal mechanism convention cannot be determined from the given
            parameters
        """
        for convention, param_list in _FocalMechanismConvention._params.items():
            if set(param_list).issubset(set(params)):
                return _FocalMechanismConvention(convention, component=component)
        msg = "Fail to determine focal mechanism convention from the data column names."
        raise GMTInvalidInput(msg)
