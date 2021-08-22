"""
Define the Figure class that handles all plotting.
"""
import base64
import os
from tempfile import TemporaryDirectory

try:
    import IPython
except ModuleNotFoundError:
    IPython = None  # pylint: disable=invalid-name


from pygmt.clib import Session
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    launch_external_viewer,
    unique_name,
    use_alias,
)

# A registry of all figures that have had "show" called in this session.
# This is needed for the sphinx-gallery scraper in pygmt/sphinx_gallery.py
SHOWED_FIGURES = []

# Configurations for figure display
SHOW_CONFIG = {
    "method": "external",  # Open in an external viewer by default
}

# Show figures in Jupyter notebooks if available
if IPython:
    get_ipython = IPython.get_ipython()  # pylint: disable=invalid-name
    if get_ipython and "IPKernelApp" in get_ipython.config:  # Jupyter Notebook enabled
        SHOW_CONFIG["method"] = "notebook"

# Set environment variable PYGMT_USE_EXTERNAL_DISPLAY to 'false' to disable
# external display. Use it when running the tests and building the docs to
# avoid popping up windows.
if os.environ.get("PYGMT_USE_EXTERNAL_DISPLAY", "true").lower() == "false":
    SHOW_CONFIG["method"] = "none"


class Figure:
    """
    A GMT figure to handle all plotting.

    Use the plotting methods of this class to add elements to the figure.  You
    can preview the figure using :meth:`pygmt.Figure.show` and save the figure
    to a file using :meth:`pygmt.Figure.savefig`.

    Unlike traditional GMT figures, no figure file is generated until you call
    :meth:`pygmt.Figure.savefig` or :meth:`pygmt.Figure.psconvert`.

    Examples
    --------

    >>> fig = Figure()
    >>> fig.basemap(region=[0, 360, -90, 90], projection="W7i", frame=True)
    >>> fig.savefig("my-figure.png")
    >>> # Make sure the figure file is generated and clean it up
    >>> import os
    >>> os.path.exists("my-figure.png")
    True
    >>> os.remove("my-figure.png")

    The plot region can be specified through ISO country codes (for example,
    ``'JP'`` for Japan):

    >>> fig = Figure()
    >>> fig.basemap(region="JP", projection="M3i", frame=True)
    >>> # The fig.region attribute shows the WESN bounding box for the figure
    >>> print(", ".join("{:.2f}".format(i) for i in fig.region))
    122.94, 145.82, 20.53, 45.52
    """

    def __init__(self):
        self._name = unique_name()
        self._preview_dir = TemporaryDirectory(  # pylint: disable=consider-using-with
            prefix=f"{self._name}-preview-"
        )
        self._activate_figure()

    def __del__(self):
        # Clean up the temporary directory that stores the previews
        if hasattr(self, "_preview_dir"):
            self._preview_dir.cleanup()

    def _activate_figure(self):
        """
        Start and/or activate the current figure.

        All plotting commands run afterward will append to this figure.

        Unlike the command-line version (``gmt figure``), this method does not
        trigger the generation of a figure file. An explicit call to
        :meth:`pygmt.Figure.savefig` or :meth:`pygmt.Figure.psconvert` must be
        made in order to get a file.
        """
        # Passing format '-' tells pygmt.end to not produce any files.
        fmt = "-"
        with Session() as lib:
            lib.call_module("figure", "{} {}".format(self._name, fmt))

    def _preprocess(self, **kwargs):
        """
        Call the ``figure`` module before each plotting command to ensure we're
        plotting to this particular figure.
        """
        self._activate_figure()
        return kwargs

    @property
    def region(self):
        """
        The geographic WESN bounding box for the current figure.
        """
        self._activate_figure()
        with Session() as lib:
            wesn = lib.extract_region()
        return wesn

    @fmt_docstring
    @use_alias(
        A="crop",
        C="gs_option",
        E="dpi",
        F="prefix",
        I="icc_gray",
        T="fmt",
        Q="anti_aliasing",
        V="verbose",
    )
    @kwargs_to_strings()
    def psconvert(self, **kwargs):
        r"""
        Convert [E]PS file(s) to other formats.

        Converts one or more PostScript files to other formats (BMP, EPS, JPEG,
        PDF, PNG, PPM, SVG, TIFF) using GhostScript.

        If no input files are given, will convert the current active figure
        (see :func:`pygmt.figure`). In this case, an output name must be given
        using parameter *prefix*.

        Full option list at :gmt-docs:`psconvert.html`

        {aliases}

        Parameters
        ----------
        crop : str or bool
            Adjust the BoundingBox and HiResBoundingBox to the minimum required
            by the image content. Append ``u`` to first remove any GMT-produced
            time-stamps. Default is True.
        gs_option : str
            Specify a single, custom option that will be passed on to
            GhostScript as is.
        dpi : int
            Set raster resolution in dpi. Default = 720 for PDF, 300 for
            others.
        prefix : str
            Force the output file name. By default output names are constructed
            using the input names as base, which are appended with an
            appropriate extension. Use this option to provide a different name,
            but without extension. Extension is still determined automatically.
        icc_gray : bool
            Enforce gray-shades by using ICC profiles.
        anti_aliasing : str
            [**g**\|\ **p**\|\ **t**\][**1**\|\ **2**\|\ **4**].
            Set the anti-aliasing options for **g**\ raphics or **t**\ ext.
            Append the size of the subsample box (1, 2, or 4) [4]. [Default is
            no anti-aliasing (same as bits = 1)].
        fmt : str
            Sets the output format, where **b** means BMP, **e** means EPS,
            **E** means EPS with PageSize command, **f** means PDF, **F** means
            multi-page PDF, **j** means JPEG, **g** means PNG, **G** means
            transparent PNG (untouched regions are transparent), **m** means
            PPM, **s** means SVG, and **t** means TIFF [default is JPEG]. To
            **b**\|\ **j**\|\ **g**\|\ **t**\ , optionally append **+m** in
            order to get a monochrome (grayscale) image. The EPS format can be
            combined with any of the other formats. For example, **ef** creates
            both an EPS and a PDF file. Using **F** creates a multi-page PDF
            file from the list of input PS or PDF files. It requires the
            ``prefix`` parameter.
        {V}
        """
        kwargs = self._preprocess(**kwargs)
        # Default cropping the figure to True
        if "A" not in kwargs:
            kwargs["A"] = ""
        # allow for spaces in figure name
        kwargs["F"] = f'"{kwargs.get("F")}"' if kwargs.get("F") else None
        with Session() as lib:
            lib.call_module("psconvert", build_arg_string(kwargs))

    def savefig(
        self, fname, transparent=False, crop=True, anti_alias=True, show=False, **kwargs
    ):
        """
        Save the figure to a file.

        This method implements a matplotlib-like interface for
        :meth:`pygmt.Figure.psconvert`.

        Supported formats: PNG (``.png``), JPEG (``.jpg``), PDF (``.pdf``),
        BMP (``.bmp``), TIFF (``.tif``), EPS (``.eps``), and KML (``.kml``).
        The KML output generates a companion PNG file.

        You can pass in any keyword arguments that
        :meth:`pygmt.Figure.psconvert` accepts.

        Parameters
        ----------
        fname : str
            The desired figure file name, including the extension. See the list
            of supported formats and their extensions above.
        transparent : bool
            If True, will use a transparent background for the figure. Only
            valid for PNG format.
        crop : bool
            If True, will crop the figure canvas (page) to the plot area.
        anti_alias: bool
            If True, will use anti aliasing when creating raster images (PNG,
            JPG, TIFF). More specifically, it passes arguments ``t2``
            and ``g2`` to the ``anti_aliasing`` parameter of
            :meth:`pygmt.Figure.psconvert`. Ignored if creating vector
            graphics.
        show: bool
            If True, will open the figure in an external viewer.
        dpi : int
            Set raster resolution in dpi. Default is 720 for PDF, 300 for
            others.
        """
        # All supported formats
        fmts = dict(png="g", pdf="f", jpg="j", bmp="b", eps="e", tif="t", kml="g")

        prefix, ext = os.path.splitext(fname)
        ext = ext[1:]  # Remove the .
        if ext not in fmts:
            if ext == "ps":
                raise GMTInvalidInput(
                    "Extension '.ps' is not supported. "
                    "Please use '.eps' or '.pdf' instead."
                )
            raise GMTInvalidInput(f"Unknown extension '.{ext}'.")
        fmt = fmts[ext]
        if transparent:
            if fmt != "g":
                raise GMTInvalidInput(
                    f"Transparency unavailable for '{ext}', only for png."
                )
            fmt = fmt.upper()
        if anti_alias:
            kwargs["Qt"] = 2
            kwargs["Qg"] = 2
        if ext == "kml":
            kwargs["W"] = "+k"

        self.psconvert(prefix=prefix, fmt=fmt, crop=crop, **kwargs)
        if show:
            launch_external_viewer(fname)

    def show(self, dpi=300, width=500, method=None):
        """
        Display a preview of the figure.

        Inserts the preview in the Jupyter notebook output if available,
        otherwise opens it in the default viewer for your operating system
        (falls back to the default web browser).

        :func:`pygmt.set_display` can select the default display method
        (**notebook**, **external**, or **none**).

        The ``method`` parameter can also override the default display method
        for the current figure. Parameters ``dpi`` and ``width`` can be used
        to control the resolution and dimension of the figure in the notebook.

        Note: The external viewer can be disabled by setting the
        PYGMT_USE_EXTERNAL_DISPLAY environment variable to **false**.
        This is useful when running unit tests and building the documentation
        in consoles without a Graphical User Interface.

        Note that the external viewer does not block the current process.

        Parameters
        ----------
        dpi : int
            The image resolution (dots per inch) in Jupyter notebooks.
        width : int
            The image width (in pixels) in Jupyter notebooks.
        method : str
            How the current figure will be displayed. Options are

            - **external**: PDF preview in an external program [default]
            - **notebook**: PNG preview [default in Jupyter notebooks]
            - **none**: Disable image preview
        """
        # Module level variable to know which figures had their show method
        # called. Needed for the sphinx-gallery scraper.
        SHOWED_FIGURES.append(self)

        # Set the display method
        if method is None:
            method = SHOW_CONFIG["method"]

        if method not in ["external", "notebook", "none"]:
            raise GMTInvalidInput(
                (
                    f"Invalid display method '{method}', "
                    "should be either 'notebook', 'external', or 'none'."
                )
            )

        if method in ["notebook", "none"]:
            if IPython is None:
                raise GMTError(
                    (
                        "Notebook display is selected, but IPython is not available. "
                        "Make sure you have IPython installed, "
                        "or run the script in a Jupyter notebook."
                    )
                )
            png = self._preview(fmt="png", dpi=dpi, anti_alias=True, as_bytes=True)
            IPython.display.display(IPython.display.Image(data=png, width=width))

        if method == "external":
            pdf = self._preview(fmt="pdf", dpi=dpi, anti_alias=False, as_bytes=False)
            launch_external_viewer(pdf)

    def shift_origin(self, xshift=None, yshift=None):
        """
        Shift plot origin in x and/or y directions.

        This method shifts plot origin relative to the current origin by
        (*xshift*, *yshift*) and optionally append the length unit (**c**,
        **i**, or **p**).

        Prepend **a** to shift the origin back to the original position after
        plotting, prepend **c** to center the plot on the center of the paper
        (optionally add shift), prepend **f** to shift the origin relative to
        the fixed lower left corner of the page, or prepend **r** [Default] to
        move the origin relative to its current location.

        Detailed usage at
        :gmt-docs:`cookbook/options.html#plot-positioning-and-layout-the-x-y-options`

        Parameters
        ----------
        xshift : str
            Shift plot origin in x direction.
        yshift : str
            Shift plot origin in y direction.
        """
        self._preprocess()
        args = ["-T"]
        if xshift:
            args.append("-X{}".format(xshift))
        if yshift:
            args.append("-Y{}".format(yshift))

        with Session() as lib:
            lib.call_module("plot", " ".join(args))

    def _preview(self, fmt, dpi, as_bytes=False, **kwargs):
        """
        Grab a preview of the figure.

        Parameters
        ----------
        fmt : str
            The image format. Can be any extension that
            :meth:`pygmt.Figure.savefig` recognizes.
        dpi : int
            The image resolution (dots per inch).
        as_bytes : bool
            If ``True``, will load the image as a bytes string and return that
            instead of the file name.

        Returns
        -------
        preview : str or bytes
            If ``as_bytes=False``, this is the file name of the preview image
            file. Else, it is the file content loaded as a bytes string.
        """
        fname = os.path.join(self._preview_dir.name, f"{self._name}.{fmt}")
        self.savefig(fname, dpi=dpi, **kwargs)
        if as_bytes:
            with open(fname, "rb") as image:
                preview = image.read()
            return preview
        return fname

    def _repr_png_(self):
        """
        Show a PNG preview if the object is returned in an interactive shell.

        For the Jupyter notebook or IPython Qt console.
        """
        png = self._preview(fmt="png", dpi=70, anti_alias=True, as_bytes=True)
        return png

    def _repr_html_(self):
        """
        Show the PNG image embedded in HTML with a controlled width.

        Looks better than the raw PNG.
        """
        raw_png = self._preview(fmt="png", dpi=300, anti_alias=True, as_bytes=True)
        base64_png = base64.encodebytes(raw_png)
        html = '<img src="data:image/png;base64,{image}" width="{width}px">'
        return html.format(image=base64_png.decode("utf-8"), width=500)

    from pygmt.src import (  # pylint: disable=import-outside-toplevel
        basemap,
        coast,
        colorbar,
        contour,
        grdcontour,
        grdimage,
        grdview,
        histogram,
        image,
        inset,
        legend,
        logo,
        meca,
        plot,
        plot3d,
        rose,
        set_panel,
        solar,
        subplot,
        text,
        velo,
        wiggle,
    )


def set_display(method=None):
    """
    Set the display method.

    Parameters
    ----------
    method : str or None
        The method to display an image. Choose from:

        - **external**: PDF preview in an external program [default]
        - **notebook**: PNG preview [default in Jupyter notebooks]
        - **none**: Disable image preview
    """
    if method in ["notebook", "external", "none"]:
        SHOW_CONFIG["method"] = method
    elif method is not None:
        raise GMTInvalidInput(
            (
                f"Invalid display mode '{method}', "
                "should be either 'notebook', 'external' or 'none'."
            )
        )
