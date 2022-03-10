"""
meca - Plot focal mechanisms.
"""
import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


def data_format_code(convention, component="full"):
    """
    Determine the data format code for meca -S option.

    See the meca() method for explanations of the parameters.

    Examples
    --------
    >>> data_format_code("aki")
    'a'
    >>> data_format_code("gcmt")
    'c'
    >>> data_format_code("partial")
    'p'

    >>> data_format_code("mt", component="full")
    'm'
    >>> data_format_code("mt", component="deviatoric")
    'z'
    >>> data_format_code("mt", component="dc")
    'd'
    >>> data_format_code("principal_axis", component="full")
    'x'
    >>> data_format_code("principal_axis", component="deviatoric")
    't'
    >>> data_format_code("principal_axis", component="dc")
    'y'

    >>> for code in ["a", "c", "m", "d", "z", "p", "x", "y", "t"]:
    ...     assert data_format_code(code) == code
    ...

    >>> data_format_code("invalid")
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput: Invalid convention 'invalid'.

    >>> data_format_code("mt", "invalid")  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput:
        Invalid component 'invalid' for convention 'mt'.
    """
    # Codes for focal mechanism formats determined by "convention"
    codes1 = {
        "aki": "a",
        "gcmt": "c",
        "partial": "p",
    }

    # Codes for focal mechanism formats determined by both "convention" and
    # "component"
    codes2 = {
        "mt": {
            "deviatoric": "z",
            "dc": "d",
            "full": "m",
        },
        "principal_axis": {
            "deviatoric": "t",
            "dc": "y",
            "full": "x",
        },
    }

    if convention in codes1:
        return codes1[convention]
    if convention in codes2:
        if component not in codes2[convention]:
            raise GMTInvalidInput(
                f"Invalid component '{component}' for convention '{convention}'."
            )
        return codes2[convention][component]
    if convention in ["a", "c", "m", "d", "z", "p", "x", "y", "t"]:
        return convention
    raise GMTInvalidInput(f"Invalid convention '{convention}'.")


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    A="offset",
    B="frame",
    N="no_clip",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def meca(
    self,
    spec,
    scale,
    longitude=None,
    latitude=None,
    depth=None,
    convention=None,
    component="full",
    plot_longitude=None,
    plot_latitude=None,
    event_name=None,
    **kwargs,
):
    """
    Plot focal mechanisms.

    Full option list at :gmt-docs:`supplements/seis/meca.html`

    Note
    ----
        Currently, labeling of beachballs with text strings is only supported
        via providing a file to `spec` as input.

    {aliases}

    Parameters
    ----------
    spec: dict, 1D array, 2D array, pd.DataFrame, or str
        Either a filename containing focal mechanism parameters as columns, a
        1- or 2-D array with the same, or a dictionary. If a filename or array,
        `convention` is required so we know how to interpret the
        columns/entries. If a dictionary, the following combinations of keys
        are supported; these determine the convention. Dictionary may contain
        values for a single focal mechanism or lists of values for many focal
        mechanisms. A Pandas DataFrame may optionally contain columns latitude,
        longitude, depth, plot_longitude, plot_latitude, and/or event_name
        instead of passing them to the meca method.

        - ``"aki"`` — *strike, dip, rake, magnitude*
        - ``"gcmt"`` — *strike1, dip1, rake1, strike2, dip2, rake2, mantissa,
          exponent*
        - ``"mt"`` — *mrr, mtt, mff, mrt, mrf, mtf, exponent*
        - ``"partial"`` — *strike1, dip1, strike2, fault_type, magnitude*
        - ``"principal_axis"`` — *t_exponent, t_azimuth, t_plunge, n_exponent,
          n_azimuth, n_plunge, p_exponent, p_azimuth, p_plunge, exponent*

    scale: str
        Adjusts the scaling of the radius of the beachball, which is
        proportional to the magnitude. Scale defines the size for magnitude = 5
        (i.e. scalar seismic moment M0 = 4.0E23 dynes-cm)
    longitude: int, float, list, or 1d numpy array
        Longitude(s) of event location. Will override the longitudes in ``spec``
        if ``spec`` is a dict or DataFrame.
    latitude: int, float, list, or 1d numpy array
        Latitude(s) of event location. Will override the latitudes in ``spec``
        if ``spec`` is a dict or DataFrame.
    depth: int, float, list, or 1d numpy array
        Depth(s) of event location in kilometers. Will override the depths in
        ``spec`` if ``spec`` is a dict or DataFrame.
    convention: str
        ``"aki"`` (Aki & Richards), ``"gcmt"`` (global CMT), ``"mt"`` (seismic
        moment tensor), ``"partial"`` (partial focal mechanism), or
        ``"principal_axis"`` (principal axis). Ignored if `spec` is a
        dictionary or dataframe.
    component: str
        The component of the seismic moment tensor to plot. ``"full"`` (the
        full seismic moment tensor), ``"dc"`` (the closest double couple with
        zero trace and zero determinant), ``"deviatoric"`` (zero trace)
    plot_longitude: int, float, list, or 1d numpy array
        Longitude(s) at which to place beachball. List must be the length of the
        number of events. Will override the plot_longitude in ``spec`` if
        ``spec`` is a dict or DataFrame
    plot_latitude: int, float, list, or 1d numpy array
        Latitude(s) at which to place beachball. List must be the length of the
        number of events. Will override the plot_latideu in ``spec`` if ``spec``
        is a dict or DataFrame.
    offset: bool or str
        Offsets beachballs to the longitude, latitude specified in the last two
        columns of the input file or array, or by `plot_longitude` and
        `plot_latitude` if provided. A small circle is plotted at the initial
        location and a line connects the beachball to the circle. Specify pen
        and optionally append ``+ssize`` to change the line style and/or size
        of the circle.
    no_clip : bool
        Does NOT skip symbols that fall outside frame boundary specified by
        *region* [Default is False, i.e. plot symbols inside map frame only].
    {J}
    {R}
    {B}
    {V}
    {XY}
    {c}
    {p}
    {t}
    """

    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if isinstance(spec, (dict, pd.DataFrame)):
        param_conventions = {
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
            "mt": ["mrr", "mtt", "mff", "mrt", "mrf", "mtf", "exponent"],
            "partial": ["strike1", "dip1", "strike2", "fault_type", "magnitude"],
            "pricipal_axis": [
                "t_exponent",
                "t_azimuth",
                "t_plunge",
                "n_exponent",
                "n_azimuth",
                "n_plunge",
                "p_exponent",
                "p_azimuth",
                "p_plunge",
                "exponent",
            ],
        }
        # determine the convention based on dict keys
        for conv, paras in param_conventions.items():
            if set(paras).issubset(set(spec.keys())):
                convention = conv
                break
        else:
            raise GMTError(
                "Parameters in spec dictionary do not match known conventions."
            )

        # override the values in dict/DataFrame if parameters are explicity specified
        if longitude is not None:
            spec["longitude"] = np.atleast_1d(longitude)
        if latitude is not None:
            spec["latitude"] = np.atleast_1d(latitude)
        if depth is not None:
            spec["depth"] = np.atleast_1d(depth)
        if plot_longitude is not None:  # must be string type
            spec["plot_longitude"] = np.atleast_1d(plot_longitude).astype(str)
        if plot_latitude is not None:  # must be string type
            spec["plot_latitude"] = np.atleast_1d(plot_latitude).astype(str)
        if event_name is not None:
            spec["event_name"] = np.atleast_1d(event_name).astype(str)

        # convert dict to DataFrame so columns can be reordered
        if isinstance(spec, dict):
            spec = pd.DataFrame(spec)

        # expected columns are:
        # longitude, latitude, depth, focal_parameters, [plot_longitude, plot_latitude] [event_name]
        newcols = ["longitude", "latitude", "depth"] + param_conventions[convention]
        if "plot_longitude" in spec.columns and "plot_latitude" in spec.columns:
            newcols += ["plot_longitude", "plot_latitude"]
            kwargs["A"] = True
        if "event_name" in spec.columns:
            newcols += ["event_name"]
        # reorder columns in DataFrame
        spec = spec.reindex(newcols, axis=1)
    elif isinstance(spec, np.ndarray) and spec.ndim == 1:
        # Convert 1d array types into 2d arrays
        spec = np.atleast_2d(spec)

    # determine data_foramt from convection and component
    data_format = data_format_code(convention=convention, component=component)

    # Assemble -S flag
    kwargs["S"] = data_format + scale
    with Session() as lib:
        # Choose how data will be passed into the module
        file_context = lib.virtualfile_from_data(check_kind="vector", data=spec)
        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            print(arg_str)
            lib.call_module("meca", arg_str)
