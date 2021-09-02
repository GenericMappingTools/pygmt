"""
grdmix - Blending and transforming grids and images.
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    C="construct",
    D="deconstruct",
    G="outgrid",
    N="normalize",
    V="verbose",
    f="coltypes",
)
@kwargs_to_strings(R="sequence")
def grdmix(grid=None, outgrid=None, **kwargs):
    r"""
    Blending and transforming grids and images.

    This function will perform various operations involving images and grids.
    We either use an *alpha* grid, image, or constant to add a new alpha
    (transparency) layer to the image given as *raster1*, or we will blend
    the two *raster1* and *raster2* (grids or images) using the *weights* for
    *raster1* and the complementary *1 - weights* for *raster2* and save to
    *outgrid*. Alternatively, we will deconstruct an image into its component
    (red, green, blue or gray) grid layers or we construct an image from its
    normalized component grids. All operations support adjusting the final
    color image via an *intensity* grid, converting a color image to
    monochrome, or strip off the alpha layer. All *raster?*, *alpha*,
    *intensity* and *weights* files must have the same dimensions. The optional
    *alpha*, *intensity* and *weights* files may be replaced by constant values
    instead.

    Full option list at :gmt-docs:`grdmix.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray or list
        *raster?*.
        The file name of the input grid(s) or the grid(s) loaded as a single
        DataArray. If only one is given and **construct** is not set then
        *raster1* must be an image. If two are given then *raster1* and
        *raster2* must both be either images or grids. If three are given then
        they must all be grids and **construct** must be set.
    outgrid : str or None
        The name for the output raster. For images, use one of these
        extensions: tif (GeoTIFF), gif, png, jpg, bmp, or ppm. For grids, see
        :gmt-docs:`Grid File Formats <grdimage.html#grid-file-formats>`.
    construct : bool
        Construct an output image from one or three normalized input grids;
        these grids must all have values in the 0-1 range only (see
        ``normalize="i"`` if they don't).
    deconstruct : bool
        Deconstruct a single image into one or three output grids. An extra
        grid will be written if the image contains an alpha (transparency
        layer). All grids written will reflect the original image values in the
        0-255 range exclusively; however, you can use ``normalize="o"`` to
        normalize the values to the 0-1 range. The output names uses the name
        template given by **outgrid** which must contain the C-format string
        "%c". This code is replaced by the codes R, G, B and A for color images
        and g, A for gray-scale images.
    normalize : str
        [**i**\|\ **o**][*divisor*].
        Normalize all input grids from 0-255 to 0-1 and all output grids from
        0-1 to 0-255. To only turn on normalization for input *or* output, use
        ``normalize="i"`` or ``normalize="o"`` instead. To divide by another
        value than 255, append an optional *divisor*.
    {R}
    {V}
    {f}
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdmix", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
