"""
meca - Plot focal mechanisms.
"""

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


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
    self,  # pylint: disable=unused-argument
    spec,
    scale,
    longitude=None,
    latitude=None,
    depth=None,
    convention=None,
    component="full",
    plot_longitude=None,
    plot_latitude=None,
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
        longitude, depth, plot_longitude, and/or plot_latitude instead of
        passing them to the meca method.

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
        Longitude(s) of event location. Ignored if `spec` is not a dictionary.
        List must be the length of the number of events. Ignored if `spec` is a
        DataFrame and contains a 'longitude' column.
    latitude: int, float, list, or 1d numpy array
        Latitude(s) of event location. Ignored if `spec` is not a dictionary.
        List must be the length of the number of events. Ignored if `spec` is a
        DataFrame and contains a 'latitude' column.
    depth: int, float, list, or 1d numpy array
        Depth(s) of event location in kilometers. Ignored if `spec` is not a
        dictionary. List must be the length of the number of events. Ignored if
        `spec` is a DataFrame and contains a 'depth' column.
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
        Longitude(s) at which to place beachball, only used if `spec` is a
        dictionary. List must be the length of the number of events. Ignored if
        `spec` is a DataFrame and contains a 'plot_longitude' column.
    plot_latitude: int, float, list, or 1d numpy array
        Latitude(s) at which to place beachball, only used if `spec` is a
        dictionary. List must be the length of the number of events. Ignored if
        `spec` is a DataFrame and contains a 'plot_latitude' column.
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

    # pylint warnings that need to be fixed
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-nested-blocks
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    def set_pointer(data_pointers, spec):
        """
        Set optional parameter pointers based on DataFrame or dict, if those
        parameters are present in the DataFrame or dict.
        """
        for param in list(data_pointers.keys()):
            if param in spec:
                # set pointer based on param name
                data_pointers[param] = spec[param]

    def update_pointers(data_pointers):
        """
        Updates variables based on the location of data, as the following data
        can be passed as parameters or it can be contained in `spec`.
        """
        # update all pointers
        longitude = data_pointers["longitude"]
        latitude = data_pointers["latitude"]
        depth = data_pointers["depth"]
        plot_longitude = data_pointers["plot_longitude"]
        plot_latitude = data_pointers["plot_latitude"]
        return (longitude, latitude, depth, plot_longitude, plot_latitude)

    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    # Check the spec and parse the data according to the specified
    # convention
    if isinstance(spec, (dict, pd.DataFrame)):
        # dicts and DataFrames are handed similarly but not identically
        if (longitude is None or latitude is None or depth is None) and not isinstance(
            spec, (dict, pd.DataFrame)
        ):
            raise GMTError("Location not fully specified.")

        param_conventions = {
            "AKI": ["strike", "dip", "rake", "magnitude"],
            "GCMT": ["strike1", "dip1", "dip2", "rake2", "mantissa", "exponent"],
            "MT": ["mrr", "mtt", "mff", "mrt", "mrf", "mtf", "exponent"],
            "PARTIAL": ["strike1", "dip1", "strike2", "fault_type", "magnitude"],
            "PRINCIPAL_AXIS": [
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

        # to keep track of where optional parameters exist
        data_pointers = {
            "longitude": longitude,
            "latitude": latitude,
            "depth": depth,
            "plot_longitude": plot_longitude,
            "plot_latitude": plot_latitude,
        }

        # make a DataFrame copy to check convention if it contains
        # other parameters
        if isinstance(spec, (dict, pd.DataFrame)):
            # check if a copy is necessary
            copy = False
            drop_list = []
            for pointer in data_pointers:
                if pointer in spec:
                    copy = True
                    drop_list.append(pointer)
            if copy:
                spec_conv = spec.copy()
                # delete optional parameters from copy for convention check
                for item in drop_list:
                    del spec_conv[item]
            else:
                spec_conv = spec

        # set convention and focal parameters based on spec convention
        for conv in list(param_conventions):
            if set(spec_conv.keys()) == set(param_conventions[conv]):
                convention = conv.lower()
                foc_params = param_conventions[conv]
                break
        else:  # if there is no convention assigned
            raise GMTError(
                "Parameters in spec dictionary do not match known conventions."
            )

        # create a dict type pointer for easier to read code
        if isinstance(spec, dict):
            dict_type_pointer = list(spec.values())[0]
        elif isinstance(spec, pd.DataFrame):
            # use df.values as pointer for DataFrame behavior
            dict_type_pointer = spec.values

        # assemble the 1D array for the case of floats and ints as values
        if isinstance(dict_type_pointer, (int, float)):
            # update pointers
            set_pointer(data_pointers, spec)
            # look for optional parameters in the right place
            (
                longitude,
                latitude,
                depth,
                plot_longitude,
                plot_latitude,
            ) = update_pointers(data_pointers)

            # Construct the array (order matters)
            spec = [longitude, latitude, depth] + [spec[key] for key in foc_params]

            # Add in plotting options, if given, otherwise add 0s
            for arg in plot_longitude, plot_latitude:
                if arg is None:
                    spec.append(0)
                else:
                    if "A" not in kwargs:
                        kwargs["A"] = True
                    spec.append(arg)

        # or assemble the 2D array for the case of lists as values
        elif isinstance(dict_type_pointer, list):
            # update pointers
            set_pointer(data_pointers, spec)
            # look for optional parameters in the right place
            (
                longitude,
                latitude,
                depth,
                plot_longitude,
                plot_latitude,
            ) = update_pointers(data_pointers)

            # before constructing the 2D array lets check that each key
            # of the dict has the same quantity of values to avoid bugs
            list_length = len(list(spec.values())[0])
            for value in list(spec.values()):
                if len(value) != list_length:
                    raise GMTError(
                        "Unequal number of focal mechanism "
                        "parameters supplied in 'spec'."
                    )
                # lets also check the inputs for longitude, latitude,
                # and depth if it is a list or array
                if (
                    isinstance(longitude, (list, np.ndarray))
                    or isinstance(latitude, (list, np.ndarray))
                    or isinstance(depth, (list, np.ndarray))
                ):
                    if (len(longitude) != len(latitude)) or (
                        len(longitude) != len(depth)
                    ):
                        raise GMTError(
                            "Unequal number of focal mechanism " "locations supplied."
                        )

            # values are ok, so build the 2D array
            spec_array = []
            for index in range(list_length):
                # Construct the array one row at a time (note that order
                # matters here, hence the list comprehension!)
                row = [longitude[index], latitude[index], depth[index]] + [
                    spec[key][index] for key in foc_params
                ]

                # Add in plotting options, if given, otherwise add 0s as
                # required by GMT
                for arg in plot_longitude, plot_latitude:
                    if arg is None:
                        row.append(0)
                    else:
                        if "A" not in kwargs:
                            kwargs["A"] = True
                        row.append(arg[index])
                spec_array.append(row)
            spec = spec_array

        # or assemble the array for the case of pd.DataFrames
        elif isinstance(dict_type_pointer, np.ndarray):
            # update pointers
            set_pointer(data_pointers, spec)
            # look for optional parameters in the right place
            (
                longitude,
                latitude,
                depth,
                plot_longitude,
                plot_latitude,
            ) = update_pointers(data_pointers)

            # lets also check the inputs for longitude, latitude, and depth
            # just in case the user entered different length lists
            if (
                isinstance(longitude, (list, np.ndarray))
                or isinstance(latitude, (list, np.ndarray))
                or isinstance(depth, (list, np.ndarray))
            ):
                if (len(longitude) != len(latitude)) or (len(longitude) != len(depth)):
                    raise GMTError(
                        "Unequal number of focal mechanism locations supplied."
                    )

            # values are ok, so build the 2D array in the correct order
            spec_array = []
            for index in range(len(spec)):
                # Construct the array one row at a time (note that order
                # matters here, hence the list comprehension!)
                row = [longitude[index], latitude[index], depth[index]] + [
                    spec[key][index] for key in foc_params
                ]

                # Add in plotting options, if given, otherwise add 0s as
                # required by GMT
                for arg in plot_longitude, plot_latitude:
                    if arg is None:
                        row.append(0)
                    else:
                        if "A" not in kwargs:
                            kwargs["A"] = True
                        row.append(arg[index])
                spec_array.append(row)
            spec = spec_array

        else:
            raise GMTError("Parameter 'spec' contains values of an unsupported type.")

    # determine data_foramt from convection and component
    data_format = data_format_code(convention=convention, component=component)

    # Assemble -S flag
    kwargs["S"] = data_format + scale

    kind = data_kind(spec)
    with Session() as lib:
        if kind == "matrix":
            file_context = lib.virtualfile_from_matrix(np.atleast_2d(spec))
        elif kind == "file":
            file_context = dummy_context(spec)
        else:
            raise GMTInvalidInput("Unrecognized data type: {}".format(type(spec)))
        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("meca", arg_str)
