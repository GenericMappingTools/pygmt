"""
grdimage - Plot grids or images.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdimage"]


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    D="img_in",
    E="dpi",
    G="bitcolor",
    I="shading",
    J="projection",
    M="monochrome",
    N="no_clip",
    Q="nan_transparent",
    R="region",
    V="verbose",
    n="interpolation",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
    x="cores",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def grdimage(self, grid, **kwargs):
    r"""
    Project and plot grids or images.

    Reads a 2-D grid file and produces a gray-shaded (or colored) map by
    building a rectangular image and assigning pixels a gray-shade (or color)
    based on the z-value and the CPT file. Optionally, illumination may be
    added by providing a file with intensities in the (-1,+1) range or
    instructions to derive intensities from the input data grid. Values outside
    this range will be clipped. Such intensity files can be created from the
    grid using :func:`pygmt.grdgradient` and, optionally, modified by
    :gmt-docs:`grdmath.html` or :class:`pygmt.grdhisteq`. Alternatively, pass
    *image* which can be an image file (geo-referenced or not). In this case
    the image can optionally be illuminated with the file provided via the
    ``shading`` parameter. Here, if image has no coordinates then those of the
    intensity file will be used.

    When using map projections, the grid is first resampled on a new
    rectangular grid with the same dimensions. Higher resolution images can
    be obtained by using the ``dpi`` parameter. To obtain the resampled value
    (and hence shade or color) of each map pixel, its location is inversely
    projected back onto the input grid after which a value is interpolated
    between the surrounding input grid values. By default bi-cubic
    interpolation is used. Aliasing is avoided by also forward projecting
    the input grid nodes. If two or more nodes are projected onto the same
    pixel, their average will dominate in the calculation of the pixel
    value. Interpolation and aliasing is controlled with the
    ``interpolation`` parameter.

    The ``region`` parameter can be used to select a map region larger or
    smaller than that implied by the extent of the grid.

    Full option list at :gmt-docs:`grdimage.html`

    {aliases}

    Parameters
    ----------
    {grid}
    {frame}
    {cmap}
    img_in : str
        [**r**].
        GMT will automatically detect standard image files (Geotiff, TIFF,
        JPG, PNG, GIF, etc.) and will read those via GDAL. For very obscure
        image formats you may need to explicitly set ``img_in``, which
        specifies that the grid is in fact an image file to be read via
        GDAL. Append **r** to assign the region specified by ``region``
        to the image. For example, if you have used ``region="d"`` then
        the image will be assigned a global domain. This mode allows you
        to project a raw image (an image without referencing coordinates).
    dpi : int
        [**i**\|\ *dpi*].
        Set the resolution of the projected grid that will be created if a
        map projection other than Linear or Mercator was selected [Default
        is ``100`` dpi]. By default, the projected grid will be of the
        same size (rows and columns) as the input file. Specify **i** to
        use the PostScript image operator to interpolate the image at the
        device resolution.
    bitcolor : str
        *color*\ [**+b**\|\ **f**\].
        This parameter only applies when a resulting 1-bit image otherwise
        would consist of only two colors: black (0) and white (255). If so,
        this parameter will instead use the image as a transparent mask and
        paint the mask with the given color. Append **+b** to paint the
        background pixels (1) or **+f** for the foreground pixels
        [Default is **+f**].
    shading : str or xarray.DataArray
        [*intensfile*\|\ *intensity*\|\ *modifiers*].
        Give the name of a grid file or a DataArray with intensities in the
        (-1,+1) range, or a constant intensity to apply everywhere (affects the
        ambient light). Alternatively, derive an intensity grid from the input
        data grid via a call to :func:`pygmt.grdgradient`; append
        **+a**\ *azimuth*, **+n**\ *args*, and **+m**\ *ambient* to specify
        azimuth, intensity, and ambient arguments for that function, or just
        give **+d** to select the default arguments (``+a-45+nt1+m0``). If you
        want a more specific intensity scenario then run
        :func:`pygmt.grdgradient` separately first. If we should derive
        intensities from another file than grid, specify the file with
        suitable modifiers [Default is no illumination]. **Note**: If the
        input data represent an *image* then an *intensfile* or constant
        *intensity* must be provided.
    {projection}
    monochrome : bool
        Force conversion to monochrome image using the (television) YIQ
        transformation. Cannot be used with ``nan_transparent``.
    no_clip : bool
        Do **not** clip the image at the frame boundaries (only relevant
        for non-rectangular maps) [Default is ``False``].
    nan_transparent : bool or str
        [**+z**\ *value*][*color*]
        Make grid nodes with z = NaN transparent, using the color-masking
        feature in PostScript Level 3 (the PS device must support PS Level
        3). If the input is a grid, use **+z** to select another grid value
        than NaN. If input is instead an image, append an alternate *color* to
        select another pixel value to be transparent [Default is ``"black"``].
    {region}
    {verbose}
    {panel}
    {coltypes}
    {interpolation}
    {perspective}
    {transparency}
    {cores}

    Example
    -------
    >>> import pygmt
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = pygmt.datasets.load_earth_relief("30m", registration="gridline")
    >>> # create a new plot with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # pass in the grid and set the CPT to "geo"
    >>> # set the projection to Mollweide and the size to 10 cm
    >>> fig.grdimage(grid=grid, cmap="geo", projection="W10c", frame="ag")
    >>> # show the plot
    >>> fig.show()
    """
    kwargs = self._preprocess(**kwargs)

    # Do not support -A option
    if any(kwargs.get(arg) is not None for arg in ["A", "img_out"]):
        raise GMTInvalidInput(
            "Parameter 'img_out'/'A' is not implemented. "
            "Please consider submitting a feature request to us."
        )

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_in(
                check_kind="raster", data=kwargs.get("I"), required_data=False
            ) as vshadegrid,
        ):
            kwargs["I"] = vshadegrid
            lib.call_module(
                module="grdimage", args=build_arg_list(kwargs, infile=vingrd)
            )
