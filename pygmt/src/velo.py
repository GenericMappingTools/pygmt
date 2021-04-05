"""
velo - Plot velocity vectors, crosses, anisotropy bars and wedges.
"""
import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    A="vector",
    B="frame",
    C="cmap",
    D="rescale",
    E="uncertainty_color",
    G="facecolor",
    J="projection",
    L="line",
    N="no_clip",
    R="region",
    S="scaling",
    U="timestamp",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", i="sequence_comma")
def velo(self, data=None, vector="+p1p+e", **kwargs):  # pylint: disable=unused-argument
    """
    Plot velocity vectors, crosses, anisotropy bars and wedges.

    Reads data values from files, numpy array or pandas DataFrame and will
    plot velocity arrows on a map. Most options are the same as for plot,
    except *scaling*.

    Must provide *data* and *scaling*.

    Full option list at :gmt-docs:`supplements/geodesy/velo.html`

    {aliases}

    Parameters
    ----------
    data : str or numpy.ndarray or pandas.DataFrame
        Either a file name, a 2D numpy array, or a pandas DataFrame with the
        tabular data. Note that text columns are only supported with file or
        pandas DataFrame inputs.

    scaling: str
        Selects the meaning of the columns in the data file and the figure
        to be plotted. In all cases, the scales are in data units per
        length unit and sizes are in length units (default length unit is
        controlled by :gmt-term:`PROJ_LENGTH_UNIT` unless **c**, **i** , or
        **p** is appended).

        "**e**\\ *velscale/confidence*\\ [**+f**\\ *font*]"

            Velocity ellipses in (N,E) convention. *velscale* sets the
            scaling of the velocity arrows. The *confidence* sets the
            2-dimensional confidence limit for the ellipse, e.g., 0.95 for
            95% confidence ellipse. *font* sets the font and size of the
            text [9p,Helvetica,black]. The ellipse will be filled with the
            color or shade specified by the *facecolor* option [default
            transparent]. The arrow and the circumference of the ellipse
            will be drawn with the pen attributes specified by the *pen*
            option. Parameters are expected to be in the following columns:

                **1**,\\ **2**:
                longitude, latitude of station (**-:** option interchanges
                order)
                **3**,\\ **4**:
                eastward, northward velocity (**-:** option interchanges
                order)
                **5**,\\ **6**:
                uncertainty of eastward, northward velocities (1-sigma)
                (**-:** option interchanges order)
                **7**:
                correlation between eastward and northward components
                **8**:
                name of station (optional).

        "**n**\\ *barscale*"

            Anisotropy bars. *barscale* sets the scaling of the bars.
            Parameters are expected to be in the following columns:

                **1**,\\ **2**:
                longitude, latitude of station (**-:** option interchanges
                order)
                **3**,\\ **4**:
                eastward, northward components of anisotropy vector (**-:**
                option interchanges order)

        "**r**\\ *velscale/confidence*\\ [**+f**\\ *font*]"

            Velocity ellipses in rotated convention. *velscale* sets the
            scaling of the velocity arrows. The *confidence* sets the
            2-dimensional confidence limit for the ellipse, e.g., 0.95 for
            95% confidence ellipse. *font* sets the font and size of the
            text [9p,Helvetica,black]. The ellipse will be filled with the
            color or shade specified by the *facecolor* option [default
            transparent]. The arrow and the circumference of the ellipse
            will be drawn with the pen attributes specified by the *pen*
            option. Parameters are expected to be in the following columns:

                **1**,\\ **2**:
                longitude, latitude, of station (**-:** option interchanges
                order)
                **3**,\\ **4**:
                eastward, northward velocity (**-:** option interchanges
                order)
                **5**,\\ **6**:
                semi-major, semi-minor axes
                **7**:
                counter-clockwise angle, in degrees, from horizontal axis
                to major axis of ellipse.
                **8**:
                name of station (optional)

            Rotational wedges. *wedgescale* sets the size of the wedges.
            Values are multiplied by *wedgemag* before plotting. For
            example, setting *wedgemag* to 1.e7 works well for rotations of
            the order of 100 nanoradians/yr. Use **facecolor** to set the
            fill color or shade for the wedge, and **uncertainty_color**
            to set the color or shade for the uncertainty. Parameters are
            expected to be in the following columns:

                **1**,\\ **2**:
                longitude, latitude, of station (**-:** option interchanges
                order)
                **3**:
                rotation in radians
                **4**:
                rotation uncertainty in radians

        "**x**\\ *cross_scale*"

            gives Strain crosses. *cross_scale* sets the size of the cross.
            Parameters are expected to be in the following columns:

                **1**,\\ **2**:
                longitude, latitude, of station (**-:** option interchanges
                order)
                **3**:
                eps1, the most extensional eigenvalue of strain tensor,
                with extension taken positive.
                **4**:
                eps2, the most compressional eigenvalue of strain tensor,
                with extension taken positive.
                **5**:
                azimuth of eps2 in degrees CW from North.

    Other Parameters
    ----------------
    vector : bool or str
        Modify vector parameters. By default, the vector head outline is
        drawn (+p) and a vector head is placed at the end of the vector path
        (+e). For specifying additional attributes, see
        :gmt-docs:`supplements/geodesy/velo.html#vector-attributes`.
    {B}
    {CPT}
    rescale : str
        can be used to rescale the uncertainties of velocities
        (``scaling='e'`` and ``scaling='r'``) and rotations
        (``scaling='w'``). Can be combined with the confidence variable.
    uncertainty_color : str
        Sets the color or shade used for filling uncertainty wedges
        (``scaling='w'``) or velocity error ellipses (``scaling='e'`` or
        ``scaling='r'``). [If *uncertainty_color* is not specified, the
        uncertainty regions will be transparent]. More details on
        :gmt-docs:`cookbook/features.html#gfill-attrib`.
    facecolor : str
        Select color or pattern for filling of symbols or polygons
        [Default is no fill]. More details on
        :gmt-docs:cookbook/features.html#gfill-attrib`.
    {J}
    line: str
        Draw lines. Ellipses and fault planes will have their outlines
        drawn using current pen (see *pen*).
    no_clip: str
        Do NOT skip symbols that fall outside the frame boundary specified
        by *region*. [Default plots symbols inside frame only].
    {R}
    {U}
    {V}
    pen : str
        Set pen attributes for velocity arrows, ellipse circumference and fault
        plane edges. [Default: width = default, color = black, style = solid].
    {XY}
    {c}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    if "S" not in kwargs or ("S" in kwargs and not isinstance(kwargs["S"], str)):
        raise GMTInvalidInput("Scaling is a required argument and has to be a string.")

    if isinstance(data, np.ndarray) and not pd.api.types.is_numeric_dtype(data):
        raise GMTInvalidInput(
            "Text columns are not supported with numpy.ndarray type inputs. "
            "They are only supported with file or pandas.DataFrame inputs."
        )

    with Session() as lib:
        # Choose how data will be passed in to the module
        file_context = lib.virtualfile_from_data(check_kind="vector", data=data)

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("velo", arg_str)
