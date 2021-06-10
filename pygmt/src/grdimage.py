"""
grdimage - Plot grids or images.
"""
import contextlib

from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="img_out",
    B="frame",
    C="cmap",
    D="img_in",
    E="dpi",
    G="bit_color",
    I="shading",
    J="projection",
    M="monochrome",
    N="no_clip",
    Q="nan_transparent",
    R="region",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
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
    grid using :meth:`pygmt.grdgradient` and, optionally, modified by
    ``grdmath`` or ``grdhisteq``. If GMT is built with GDAL support, ``grid``
    can be an image file (geo-referenced or not). In this case the image can
    optionally be illuminated with the file provided via the ``shading``
    parameter. Here, if image has no coordinates then those of the intensity
    file will be used.

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

    Full parameter list at :gmt-docs:`grdimage.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name or a DataArray containing the input 2-D gridded data
        set or image to be plotted (See GRID FILE FORMATS at
        :gmt-docs:`grdimage.html#grid-file-formats`).
    img_out : str
        *out_img*\[=\ *driver*].
        Save an image in a raster format instead of PostScript. Use
        extension .ppm for a Portable Pixel Map format which is the only
        raster format GMT can natively write. For GMT installations
        configured with GDAL support there are more choices: Append
        *out_img* to select the image file name and extension. If the
        extension is one of .bmp, .gif, .jpg, .png, or .tif then no driver
        information is required. For other output formats you must append
        the required GDAL driver. The *driver* is the driver code name used
        by GDAL; see your GDAL installation's documentation for available
        drivers. Append a **+c**\ *args* string where *args* is a list
        of one or more concatenated number of GDAL **-co** arguments. For
        example, to write a GeoPDF with the TerraGo format use
        ``=PDF+cGEO_ENCODING=OGC_BP``. Notes: (1) If a tiff file (.tif) is
        selected then we will write a GeoTiff image if the GMT projection
        syntax translates into a PROJ syntax, otherwise a plain tiff file
        is produced. (2) Any vector elements will be lost.
    {B}
    {CPT}
    img_in : str
        [**r**].
        GMT will automatically detect standard image files (Geotiff, TIFF,
        JPG, PNG, GIF, etc.) and will read those via GDAL. For very obscure
        image formats you may need to explicitly set ``img_in``, which
        specifies that the grid is in fact an image file to be read via
        GDAL. Append **r** to assign the region specified by ``region``
        to the image. For example, if you have used ``region='d'`` then the
        image will be assigned a global domain. This mode allows you to
        project a raw image (an image without referencing coordinates).
    dpi : int
        [**i**\|\ *dpi*].
        Sets the resolution of the projected grid that will be created if a
        map projection other than Linear or Mercator was selected [100]. By
        default, the projected grid will be of the same size (rows and
        columns) as the input file. Specify **i** to use the PostScript
        image operator to interpolate the image at the device resolution.
    bit_color : str
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
        data grid via a call to :meth:`pygmt.grdgradient`; append
        **+a**\ *azimuth*, **+n**\ *args*, and **+m**\ *ambient* to specify
        azimuth, intensity, and ambient arguments for that module, or just give
        **+d** to select the default arguments (``+a-45+nt1+m0``). If you want
        a more specific intensity scenario then run :meth:`pygmt.grdgradient`
        separately first. If we should derive intensities from another file
        than grid, specify the file with suitable modifiers [Default is no
        illumination]. Note: If the input data is an *image* then an
        *intensfile* or constant *intensity* must be provided.
    {J}
    monochrome : bool
        Force conversion to monochrome image using the (television) YIQ
        transformation. Cannot be used with ``nan_transparent``.
    no_clip : bool
        Do not clip the image at the map boundary (only relevant for
        non-rectangular maps).
    nan_transparent : bool
        Make grid nodes with z = NaN transparent, using the color-masking
        feature in PostScript Level 3 (the PS device must support PS Level
        3).
    {R}
    {V}
    {XY}
    {c}
    {f}
    {n}
    {p}
    {t}
    {x}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
        with contextlib.ExitStack() as stack:
            # shading using an xr.DataArray
            if "I" in kwargs and data_kind(kwargs["I"]) == "grid":
                shading_context = lib.virtualfile_from_grid(kwargs["I"])
                kwargs["I"] = stack.enter_context(shading_context)

            fname = stack.enter_context(file_context)
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("grdimage", arg_str)
