"""
Define the Figure class that handles all plotting.
"""
import os
from tempfile import TemporaryDirectory

try:
    import IPython

    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False

from .clib import Session
from .base_plotting import BasePlotting
from .exceptions import GMTInvalidInput
from .helpers import (
    build_arg_string,
    fmt_docstring,
    use_alias,
    kwargs_to_strings,
    launch_external_viewer,
    unique_name,
)


# A registry of all figures that have had "show" called in this session.
# This is needed for the sphinx-gallery scraper in pygmt/sphinx_gallery.py
SHOWED_FIGURES = []
# Configuration options for Jupyter notebook support
SHOW_CONFIG = {"dpi": 200, "external": True, "display": False}
# If the environment variable is set to "false", disable the external viewer. Use this
# for running the tests and building the docs to avoid pop up windows.
if os.environ.get("PYGMT_EXTERNAL_VIEWER", "default") == "false":
    SHOW_CONFIG["external"] = False


def enable_notebook(dpi=200):
    """
    Enable extended support for the Jupyter notebook.

    Suppresses an external window from popping-up when :meth:`pygmt.Figure.show` is
    called. Can also control the resolution of displayed images in the notebook.

    Parameters
    ----------
    dpi : int
        Set the default DPI (dots-per-inch) used for PNG image previews that are
        inserted into the notebook.

    """
    SHOW_CONFIG["dpi"] = dpi
    SHOW_CONFIG["external"] = False
    SHOW_CONFIG["display"] = True


class Figure(BasePlotting):
    """
    A GMT figure to handle all plotting.

    Use the plotting methods of this class to add elements to the figure.  You
    can preview the figure using :meth:`pygmt.Figure.show` and save the figure to
    a file using :meth:`pygmt.Figure.savefig`.

    Unlike traditional GMT figures, no figure file is generated until you call
    :meth:`pygmt.Figure.savefig` or :meth:`pygmt.Figure.psconvert`.

    Examples
    --------

    >>> fig = Figure()
    >>> fig.basemap(region=[0, 360, -90, 90], projection='W7i', frame=True)
    >>> fig.savefig("my-figure.png")
    >>> # Make sure the figure file is generated and clean it up
    >>> import os
    >>> os.path.exists('my-figure.png')
    True
    >>> os.remove('my-figure.png')

    The plot region can be specified through ISO country codes (for example,
    ``'JP'`` for Japan):

    >>> fig = Figure()
    >>> fig.basemap(region='JP', projection="M3i", frame=True)
    >>> # The fig.region attribute shows the WESN bounding box for the figure
    >>> print(', '.join('{:.2f}'.format(i)  for i in fig.region))
    122.94, 145.82, 20.53, 45.52

    """

    def __init__(self):
        self._name = unique_name()
        self._preview_dir = TemporaryDirectory(prefix=self._name + "-preview-")
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
        :meth:`pygmt.Figure.savefig` or :meth:`pygmt.Figure.psconvert` must be made
        in order to get a file.
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
        "The geographic WESN bounding box for the current figure."
        self._activate_figure()
        with Session() as lib:
            wesn = lib.extract_region()
        return wesn

    @fmt_docstring
    @use_alias(F="prefix", T="fmt", A="crop", E="dpi")
    @kwargs_to_strings()
    def psconvert(self, **kwargs):
        """
        Convert [E]PS file(s) to other formats.

        Converts one or more PostScript files to other formats (BMP, EPS, JPEG,
        PDF, PNG, PPM, SVG, TIFF) using GhostScript.

        If no input files are given, will convert the current active figure
        (see :func:`pygmt.figure`). In this case, an output name must be given
        using parameter *F*.

        Full option list at :gmt-docs:`psconvert.html`

        {aliases}

        Parameters
        ----------
        A : str or bool
            Adjust the BoundingBox and HiResBoundingBox to the minimum required
            by the image content. Append ``u`` to first remove any GMT-produced
            time-stamps. Default is True.
        C : str
            Specify a single, custom option that will be passed on to
            GhostScript as is.
        E : int
            Set raster resolution in dpi. Default = 720 for PDF, 300 for
            others.
        F : str
            Force the output file name. By default output names are constructed
            using the input names as base, which are appended with an
            appropriate extension. Use this option to provide a different name,
            but without extension. Extension is still determined automatically.
        I : bool
            Enforce gray-shades by using ICC profiles.
        Q : str
            Set the anti-aliasing options for graphics or text. Append the size
            of the subsample box (1, 2, or 4) [4]. Default is no anti-aliasing
            (same as bits = 1).
        T : str
            Sets the output format, where b means BMP, e means EPS, E means EPS
            with PageSize command, f means PDF, F means multi-page PDF, j means
            JPEG, g means PNG, G means transparent PNG (untouched regions are
            transparent), m means PPM, s means SVG, and t means TIFF [default
            is JPEG]. To bjgt you can append - in order to get a grayscale
            image. The EPS format can be combined with any of the other
            formats. For example, ``'ef'`` creates both an EPS and a PDF file.
            The ``'F'`` creates a multi-page PDF file from the list of input PS
            or PDF files. It requires the *F* option.

        """
        kwargs = self._preprocess(**kwargs)
        # Default cropping the figure to True
        if "A" not in kwargs:
            kwargs["A"] = ""
        with Session() as lib:
            lib.call_module("psconvert", build_arg_string(kwargs))

    def savefig(self, fname, transparent=False, crop=True, anti_alias=True, **kwargs):
        """
        Save the figure to a file.

        This method implements a matplotlib-like interface for
        :meth:`~gmt.Figure.psconvert`.

        Supported formats: PNG (``.png``), JPEG (``.jpg``), PDF (``.pdf``),
        BMP (``.bmp``), TIFF (``.tif``), EPS (``.eps``), and KML (``.kml``).
        The KML output generates a companion PNG file.

        You can pass in any keyword arguments that :meth:`~gmt.Figure.psconvert`
        accepts.

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
            JPG, TIf). More specifically, uses options ``Qt=2, Qg=2`` in
            :meth:`~gmt.Figure.psconvert`. Ignored if creating vector graphics.
            Overrides values of ``Qt`` and ``Qg`` passed in through ``kwargs``.
        dpi : int
            Set raster resolution in dpi. Default is 720 for PDF, 300 for
            others.

        """
        # All supported formats
        fmts = dict(png="g", pdf="f", jpg="j", bmp="b", eps="e", tif="t", kml="g")

        prefix, ext = os.path.splitext(fname)
        ext = ext[1:]  # Remove the .
        if ext not in fmts:
            raise GMTInvalidInput("Unknown extension '.{}'".format(ext))
        fmt = fmts[ext]
        if transparent:
            if fmt != "g":
                raise GMTInvalidInput(
                    "Transparency unavailable for '{}', only for png.".format(ext)
                )
            fmt = fmt.upper()
        if anti_alias:
            kwargs["Qt"] = 2
            kwargs["Qg"] = 2
        if ext == "kml":
            kwargs["W"] = "+k"

        self.psconvert(prefix=prefix, fmt=fmt, crop=crop, **kwargs)

    def show(self):
        """
        Display a preview of the figure.

        By default, opens a PDF preview of the figure in the default PDF viewer. Behaves
        differently depending on the operating system:

        * Linux: Uses ``xdg-open`` (which might need to be installed).
        * Mac: Uses the ``open`` command.
        * Windows: Uses Python's :func:`os.startfile` function.

        If we can't determine your OS or ``xdg-open`` is not available on Linux, falls
        back to using the default web browser to open the file.

        If :func:`pygmt.enable_notebook` was called, will not open the external viewer
        and will instead use ``IPython.display.display`` to display the figure on th
        Jupyter notebook or IPython Qt console.

        The external viewer can also be disabled by setting the
        ``PYGMT_EXTERNAL_VIEWER`` environment variable to ``false``. This is mainly used
        for running our tests and building the documentation.
        """
        # Module level variable to know which figures had their show method called.
        # Needed for the sphinx-gallery scraper.
        SHOWED_FIGURES.append(self)

        if SHOW_CONFIG["external"]:
            pdf = self._preview(
                fmt="pdf", dpi=SHOW_CONFIG["dpi"], anti_alias=False, as_bytes=False
            )
            launch_external_viewer(pdf)
        if HAS_IPYTHON and SHOW_CONFIG["display"]:
            png = self._repr_png_()
            IPython.display.display(IPython.display.Image(data=png))

    def shift_origin(self, xshift=None, yshift=None):
        """
        Shift plot origin in x and/or y directions.

        This method shifts plot origin relative to the current origin by (*xshift*,*yshift*)
        and optionally append the length unit (**c**, **i**, or **p**).

        Prepend **a** to shift the origin back to the original position
        after plotting, prepend **c** to center the plot on the center of the
        paper (optionally add shift), prepend **f** to shift the origin relative
        to the fixed lower left corner of the page, or prepend **r** [Default] to
        move the origin relative to its current location.

        Detailed usage at :gmt-docs:`GMT_Docs.html#plot-positioning-and-layout-the-x-y-options`

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
            :meth:`~gmt.Figure.savefig` recognizes.
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
        fname = os.path.join(self._preview_dir.name, "{}.{}".format(self._name, fmt))
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
        png = self._preview(
            fmt="png", dpi=SHOW_CONFIG["dpi"], anti_alias=True, as_bytes=True
        )
        return png
