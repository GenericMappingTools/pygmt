"""
velo - Plot velocity vectors, crosses, anisotropy bars, and wedges.
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
    H="scale",
    I="intensity",
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
    Z="zvalue",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def velo(self, data=None, **kwargs):
    r"""
    Plot velocity vectors, crosses, anisotropy bars, and wedges.

    Reads data values from files, :class:`numpy.ndarray` or
    :class:`pandas.DataFrame` and will plot the selected geodesy symbol on a
    map. You may choose from velocity vectors
    and their uncertainties, rotational wedges and their uncertainties,
    anisotropy bars, or strain crosses. Symbol fills or their outlines may be
    colored based on constant parameters or via color lookup tables.

    Must provide ``data`` and ``scaling``.

    Full option list at :gmt-docs:`supplements/geodesy/velo.html`

    {aliases}

    Parameters
    ----------
    data : str or numpy.ndarray or pandas.DataFrame
        Either a file name, a 2D :class:`numpy.ndarray` or a
        :class:`pandas.DataFrame` with the tabular data. Note that text columns
        are only supported with file or pandas DataFrame inputs.

    scaling: str
        Selects the meaning of the columns in the data file and the figure
        to be plotted. In all cases, the scales are in data units per length
        unit and sizes are in length units (default length unit is controlled
        by :gmt-term:`PROJ_LENGTH_UNIT` unless **c**, **i**, or **p** is
        appended).

        - **e**\ [*velscale*/]\ *confidence*\ [**+f**\ *font*]

          Velocity ellipses in (N,E) convention. The *velscale* sets the
          scaling of the velocity arrows. If *velscale* is not given then we
          read it from the data file as an extra column. The *confidence* sets
          the 2-dimensional confidence limit for the ellipse, e.g. 0.95 for 95%
          confidence ellipse. Use **+f** to set the font and size of the text
          [Default is 9p,Helvetica,black]; give **+f**\ 0 to deactivate
          labeling. The arrow will be drawn with the pen attributes specified
          by the ``pen`` option and the arrow-head can be colored via
          ``facecolor``. The ellipse will be filled with the color or shade
          specified by the ``uncertainty_color`` option [Default is
          transparent], and its outline will be drawn if ``line`` is selected
          using the pen selected (by ``pen`` if not given by ``line``).
          Parameters are expected to be in the following columns:

            - **1**,\ **2**: longitude, latitude of station
            - **3**,\ **4**: eastward, northward velocity
            - **5**,\ **6**: uncertainty of eastward, northward velocities
              (1-sigma)
            - **7**: correlation between eastward and northward components
            - **Trailing text**: name of station (optional)

        - **n**\ [*barscale*]

          Anisotropy bars. *barscale* sets the scaling of the bars. If
          *barscale* is not given then we read it from the data file as an
          extra column. Parameters are expected to be in the following columns:

            - **1**,\ **2**: longitude, latitude of station
            - **3**,\ **4**: eastward, northward components of anisotropy
              vector

        - **r**\ [*velscale*/]\ *confidence*\ [**+f**\ *font*]

          Velocity ellipses in rotated convention. The *velscale* sets the
          scaling of the velocity arrows. If *velscale* is not given then we
          read it from the data file as an extra column. The *confidence* sets
          the 2-dimensional confidence limit for the ellipse, e.g. 0.95 for 95%
          confidence ellipse. Use **+f** to set the font and size of the text
          [Default is 9p,Helvetica,black]; give **+f**\ 0 to deactivate
          labeling. The arrow will be drawn with the pen attributes specified
          by the ``pen`` option and the arrow-head can be colored via
          ``facecolor``. The ellipse will be filled with the color or shade
          specified by the ``uncertainty_color`` option [Default is
          transparent], and its outline will be drawn if ``line`` is selected
          using the pen selected (by ``pen`` if not given by ``line``).
          Parameters are expected to be in the following columns:

            - **1**,\ **2**: longitude, latitude of station
            - **3**,\ **4**: eastward, northward velocity
            - **5**,\ **6**: semi-major, semi-minor axes
            - **7**: counter-clockwise angle, in degrees, from horizontal axis
              to major axis of ellipse.
            - **Trailing text**: name of station (optional)

        - **w**\ [*wedgescale*/]\ *wedgemag*

          Rotational wedges. The *wedgescale* sets the size of the wedges. If
          *wedgescale* is not given then we read it from the data file as an
          extra column. Rotation values are multiplied by *wedgemag* before
          plotting. For example, setting *wedgemag* to 1.e7 works well for
          rotations of the order of 100 nanoradians/yr. Use ``facecolor`` to
          set the fill color or shade for the wedge, and ``uncertainty_color``
          to set the color or shade for the uncertainty. Parameters are
          expected to be in the following columns:

            - **1**,\ **2**: longitude, latitude of station
            - **3**: rotation in radians
            - **4**: rotation uncertainty in radians

        - **x**\ [*cross_scale*]

          gives Strain crosses. The *cross_scale* sets the size of the cross.
          If *cross_scale* is not given then we read it from the data file as
          an extra column. Parameters are expected to be in the following
          columns:

            - **1**,\ **2**: longitude, latitude of station
            - **3**: eps1, the most extensional eigenvalue of strain tensor,
              with extension taken positive.
            - **4**: eps2, the most compressional eigenvalue of strain tensor,
              with extension taken positive.
            - **5**: azimuth of eps2 in degrees CW from North.

    vector : bool or str
        Modify vector parameters. For vector heads, append vector head *size*
        [Default is 9p]. See
        :gmt-docs:`supplements/geodesy/velo.html#vector-attributes` for
        specifying additional attributes.
    {B}
    {CPT}
    rescale : str
        can be used to rescale the uncertainties of velocities
        (``scaling='e'`` and ``scaling='r'``) and rotations
        (``scaling='w'``). Can be combined with the ``confidence`` variable.
    uncertainty_color : str
        Sets the color or shade used for filling uncertainty wedges
        (``scaling='w'``) or velocity error ellipses (``scaling='e'`` or
        ``scaling='r'``). If ``uncertainty_color`` is not specified, the
        uncertainty regions will be transparent. **Note**: Using ``cmap`` and
        ``zvalue='+e'`` will update the uncertainty fill color based on the
        selected measure in ``zvalue`` [magnitude error]. More details at
        :gmt-docs:`cookbook/features.html#gfill-attrib`.
    facecolor : str
        Select color or pattern for filling of symbols [Default is no fill].
        **Note**: Using ``cmap`` (and optionally ``zvalue``) will update the
        symbol fill color based on the selected measure in ``zvalue``
        [magnitude]. More details at
        :gmt-docs:`cookbook/features.html#gfill-attrib`.
    scale : float or bool
        [*scale*].
        Scale symbol sizes and pen widths on a per-record basis using the
        *scale* read from the data set, given as the first column after the
        (optional) *z* and *size* columns [Default is no scaling]. The symbol
        size is either provided by ``scaling`` or via the input *size* column.
        Alternatively, append a constant *scale* that should be used instead of
        reading a scale column.
    intensity : float or bool
        *intens*.
        Use the supplied *intens* value (nominally in the -1 to +1 range) to
        modulate the symbol fill color by simulating illumination [Default is
        none]. If no intensity is provided we will instead read *intens* from
        an extra data column after the required input columns determined by
        ``scaling``.
    {J}
    line: str
        [*pen*\ [**+c**\ [**f**\|\ **l**]]].
        Draw lines. Ellipses and rotational wedges will have their outlines
        drawn using the current pen (see ``pen``).  Alternatively, append a
        separate pen to use for the error outlines. If the modifier **+cl** is
        appended then the color of the pen is updated from the CPT (see
        ``cmap``). If instead modifier **+cf** is appended then the color from
        the cpt file is applied to error fill only [Default]. Use just **+c**
        to set both pen and fill color.
    no_clip: bool or str
        Do NOT skip symbols that fall outside the frame boundary specified
        by ``region``. [Default plots symbols inside frame only].
    {R}
    {U}
    {V}
    pen : str
        [*pen*][**+c**\ [**f**\|\ **l**]].
        Set pen attributes for velocity arrows, ellipse circumference and fault
        plane edges. [Defaults: width = default, color = black, style = solid].
        If the modifier **+cl** is appended then the color of the pen are
        updated from the CPT (see ``cmap``). If instead modifier **+cf** is
        appended then the color from the cpt file is applied to symbol fill
        only [Default].  Use just **+c** to set both pen and fill color.
    {XY}
    zvalue : str
        [**m**\|\ **e**\|\ **n**\|\ **u**\ ][**+e**].
        Select the quantity that will be used with the CPT given via ``cmap``
        to set the fill color.  Choose from **m**\ agnitude (vector magnitude
        or rotation magnitude), **e**\ ast-west velocity, **n**\ orth-south
        velocity, or **u**\ ser-supplied data column (supplied after the
        required columns). To instead use the corresponding error estimates
        (i.e., vector or rotation uncertainty) to lookup the color and paint
        the error ellipse or wedge instead, append **+e**.
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
