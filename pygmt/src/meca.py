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
    Determine the data format code for meca's -S option.

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
    codes1 = {"aki": "a", "gcmt": "c", "partial": "p"}
    # Codes for focal mechanism formats determined by both "convention" and
    # "component"
    codes2 = {
        "mt": {"deviatoric": "z", "dc": "d", "full": "m"},
        "principal_axis": {"deviatoric": "t", "dc": "y", "full": "x"},
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
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def meca(
    self,
    spec,
    scale,
    convention=None,
    component="full",
    longitude=None,
    latitude=None,
    depth=None,
    plot_longitude=None,
    plot_latitude=None,
    event_name=None,
    **kwargs,
):
    r"""
    Plot focal mechanisms.

    Full option list at :gmt-docs:`supplements/seis/meca.html`

    {aliases}

    Parameters
    ----------
    spec: str, 1-D array, 2-D array, dict, or pd.DataFrame
        Data that contains focal mechanism parameters.

        ``spec`` can be specified in either of the following types:

        - *str*: a file name containing focal mechanism parameters as
          columns. The meaning of each column is:

          - Columns 1 and 2: event longitude and latitude
          - Column 3: event depth (in km)
          - Columns 4 to 3+n: focal mechanism parameters. The number of columns
            *n* depends on the choice of ``convection``, which will be
            described below.
          - Columns 4+n and 5+n: longitude, latitude at which to place
            beachball. Using ``0 0`` will plot the beachball at the longitude,
            latitude given in columns 1 and 2. [optional and requires
            ``offset=True`` to take effect].
          - Text string to appear near the beachball [optional].

        - *1-D array*: focal mechanism parameters of a single event.
          The meanings of columns are the same as above.
        - *2-D array*: focal mechanim parameters of multiple events.
          The meanings of columns are the same as above.
        - *dict or pd.DataFrame*: The dict keys or pd.DataFrame column names
          determine the focal mechanims convention. For different conventions,
          the following combination of keys are allowed:

          - ``"aki"``: *strike, dip, rake, magnitude*
          - ``"gcmt"``: *strike1, dip1, rake1, strike2, dip2, rake2, mantissa,*
            *exponent*
          - ``"mt"``: *mrr, mtt, mff, mrt, mrf, mtf, exponent*
          - ``"partial"``: *strike1, dip1, strike2, fault_type, magnitude*
          - ``"principal_axis"``: *t_value, t_azimuth, t_plunge, n_value,
            n_azimuth, n_plunge, p_value, p_azimuth, p_plunge, exponent*

          A dict may contain values for a single focal mechanism or lists of
          values for multiple focal mechanisms.

          Both dict and pd.DataFrame may optionally contain keys/column names:
          ``latitude``, ``longitude``, ``depth``, ``plot_longitude``,
          ``plot_latitude``, and/or ``event_name``.

          If ``spec`` is either a str, a 1-D array or a 2-D array, the
          ``convention`` parameter is required so we know how to interpret the
          columns. If ``spec`` is a dict or a pd.DataFrame, ``convention`` is
          not needed and is ignored if specified.

    scale: str
        Adjusts the scaling of the radius of the beachball, which is
        proportional to the magnitude. *scale* defines the size for
        magnitude = 5 (i.e. scalar seismic moment M0 = 4.0E23 dynes-cm).
    convention: str
        Focal mechanism convention. Choose from:

        - ``"aki"`` (Aki & Richards)
        - ``"gcmt"`` (global CMT)
        - ``"mt"`` (seismic moment tensor)
        - ``"partial"`` (partial focal mechanism)
        - ``"principal_axis"`` (principal axis)

        Ignored if ``spec`` is a dictionary or pd.DataFrame.
    component: str
        The component of the seismic moment tensor to plot.

        - ``"full"``: the full seismic moment tensor
        - ``"dc"``: the closest double couple defined from the moment tensor
          (zero trace and zero determinant)
        - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)
    longitude: int, float, list, or 1-D numpy array
        Longitude(s) of event location. Must be the same length as the
        number of events. Will override the ``longitude`` values
        in ``spec`` if ``spec`` is a dict or pd.DataFrame.
    latitude: int, float, list, or 1-D numpy array
        Latitude(s) of event location. Must be the same length as the
        number of events. Will override the ``latitude`` values
        in ``spec`` if ``spec`` is a dict or pd.DataFrame.
    depth: int, float, list, or 1-D numpy array
        Depth(s) of event location in kilometers. Must be the same length as
        the number of events. Will override the ``depth`` values in ``spec``
        if ``spec`` is a dict or pd.DataFrame.
    plot_longitude: int, float, str, list, or 1-D numpy array
        Longitude(s) at which to place beachball. Must be the same length as
        the number of events. Will override the ``plot_longitude`` values in
        ``spec`` if ``spec`` is a dict or pd.DataFrame.
    plot_latitude: int, float, str, list, or 1-D numpy array
        Latitude(s) at which to place beachball. List must be the same length
        as the number of events. Will override the ``plot_latitude`` values in
        ``spec`` if ``spec`` is a dict or pd.DataFrame.
    event_name : str or list of str, or 1-D numpy array
        Text strings (e.g., event names) to appear near the beachball. List
        must be the same length as the number of events. Will override the
        ``event_name`` values in ``spec`` if ``spec`` is a dict or
        pd.DataFrame.
    offset: bool or str
        [**+p**\ *pen*][**+s**\ *size*].
        Offsets beachballs to the longitude, latitude specified in the last two
        columns of the input file or array, or by ``plot_longitude`` and
        ``plot_latitude`` if provided. A small circle is plotted at the initial
        location and a line connects the beachball to the circle. Use
        **+s**\ *size* to set the diameter of the circle [Default is
        no circle]. Use **+p**\ *pen* to set the line pen attributes [Default
        is 0.25p].
    no_clip : bool
        Does NOT skip symbols that fall outside frame boundary specified by
        ``region`` [Default is False, i.e. plot symbols inside map frame only].
    {projection}
    {region}
    {frame}
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if isinstance(spec, (dict, pd.DataFrame)):  # spec is a dict or pd.DataFrame
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
        # determine convention from dict keys or pd.DataFrame column names
        for conv, paras in param_conventions.items():
            if set(paras).issubset(set(spec.keys())):
                convention = conv
                break
        else:
            if isinstance(spec, dict):
                msg = "Keys in dict 'spec' do not match known conventions."
            else:
                msg = "Column names in pd.DataFrame 'spec' do not match known conventions."
            raise GMTError(msg)

        # override the values in dict/pd.DataFrame if parameters are explicity
        # specified
        if longitude is not None:
            spec["longitude"] = np.atleast_1d(longitude)
        if latitude is not None:
            spec["latitude"] = np.atleast_1d(latitude)
        if depth is not None:
            spec["depth"] = np.atleast_1d(depth)
        if plot_longitude is not None:
            spec["plot_longitude"] = np.atleast_1d(plot_longitude)
        if plot_latitude is not None:
            spec["plot_latitude"] = np.atleast_1d(plot_latitude)
        if event_name is not None:
            spec["event_name"] = np.atleast_1d(event_name).astype(str)

        # convert dict to pd.DataFrame so columns can be reordered
        if isinstance(spec, dict):
            # convert values to ndarray so pandas doesn't complain about "all
            # scalar values". See
            # https://github.com/GenericMappingTools/pygmt/pull/2174
            spec = {key: np.atleast_1d(value) for key, value in spec.items()}
            spec = pd.DataFrame(spec)

        # expected columns are:
        # longitude, latitude, depth, focal_parameters,
        #   [plot_longitude, plot_latitude] [event_name]
        newcols = ["longitude", "latitude", "depth"] + param_conventions[convention]
        if "plot_longitude" in spec.columns and "plot_latitude" in spec.columns:
            newcols += ["plot_longitude", "plot_latitude"]
            spec[["plot_longitude", "plot_latitude"]] = spec[
                ["plot_longitude", "plot_latitude"]
            ].astype(str)
            if kwargs.get("A") is None:
                kwargs["A"] = True
        if "event_name" in spec.columns:
            newcols += ["event_name"]
            spec["event_name"] = spec["event_name"].astype(str)
        # reorder columns in DataFrame
        spec = spec.reindex(newcols, axis=1)
    elif isinstance(spec, np.ndarray) and spec.ndim == 1:
        # Convert 1-D array into 2-D array
        spec = np.atleast_2d(spec)

    # determine data_format from convention and component
    data_format = data_format_code(convention=convention, component=component)

    # Assemble -S flag
    kwargs["S"] = data_format + scale
    with Session() as lib:
        # Choose how data will be passed into the module
        file_context = lib.virtualfile_from_data(check_kind="vector", data=spec)
        with file_context as fname:
            lib.call_module(module="meca", args=build_arg_string(kwargs, infile=fname))
