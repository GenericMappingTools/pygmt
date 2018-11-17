"""
Define the Figure class that handles all plotting.
"""
import os
from tempfile import TemporaryDirectory
import base64

try:
    from IPython.display import Image
except ImportError:
    Image = None

from .clib import Session
from .base_plotting import BasePlotting
from .exceptions import GMTError, GMTInvalidInput
from .helpers import (
    build_arg_string,
    fmt_docstring,
    use_alias,
    kwargs_to_strings,
    launch_external_viewer,
    unique_name,
    worldwind_show,
)


_figures = dict()


class Figure(BasePlotting):
    """
    A GMT figure to handle all plotting.

    Use the plotting methods of this class to add elements to the figure.  You
    can preview the figure using :meth:`gmt.Figure.show` and save the figure to
    a file using :meth:`gmt.Figure.savefig`.

    Unlike traditional GMT figures, no figure file is generated until you call
    :meth:`gmt.Figure.savefig` or :meth:`gmt.Figure.psconvert`.

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
        _figures[self._name] = self

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
        :meth:`gmt.Figure.savefig` or :meth:`gmt.Figure.psconvert` must be made
        in order to get a file.
        """
        # Passing format '-' tells gmt.end to not produce any files.
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
        (see :func:`gmt.figure`). In this case, an output name must be given
        using parameter *F*.

        {gmt_module_docs}

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

    def savefig(
        self, fname, transparent=False, crop=True, anti_alias=True, show=False, **kwargs
    ):
        """
        Save the figure to a file.

        This method implements a matplotlib-like interface for
        :meth:`~gmt.Figure.psconvert`.

        Supported formats: PNG (``.png``), JPEG (``.jpg``), PDF (``.pdf``),
        BMP (``.bmp``), TIFF (``.tif``), EPS (``.eps``), and KML (``.kml``).
        The KML output generates a companion PNG file.

        You can pass in any keyword arguments that
        :meth:`~gmt.Figure.psconvert` accepts.

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
        if show:
            launch_external_viewer(fname)

    def show(self, dpi=300, width=500, method="static", globe_center=None):
        """
        Display a preview of the figure.

        Inserts the preview in the Jupyter notebook output. You will need to
        have IPython installed for this to work. You should have it if you are
        using the notebook.

        If ``method='external'``, makes PDF preview instead and opens it in the
        default viewer for your operating system (falls back to the default web
        browser). Note that the external viewer does not block the current
        process, so this won't work in a script.

        If using the ``'globe'`` preview, use a Cartesian projection (``'X'``)
        and specify degrees as size units (e.g. ``projection='X3id/3id'``).
        Otherwise, the figure may not align with the globe.

        Parameters
        ----------
        dpi : int
            The image resolution (dots per inch).
        width : int
            Width of the figure shown in the notebook in pixels. Ignored if
            ``method='external'``.
        method : str
            How the figure will be displayed. Options are (1) ``'static'``: PNG
            preview (default); (2) ``'external'``: PDF preview in an external
            program; (3) ``'globe'``: interactive 3D globe in the notebook
            using `NASA WorldWind Web <https://worldwind.arc.nasa.gov>`__ (only
            use if plotting lon/lat data).
        globe_center : None or tuple = (lon, lat, height[m])
            The coordinates used to set the view point for the globe preview.
            If None, will automatically determine a view based on the plot
            region. Only used if ``method='globe'``.

        Returns
        -------
        img : IPython.display.Image or IPython.display.Javascript
            Only if ``method != 'external'``.

        """
        if method not in ["static", "external", "globe"]:
            raise GMTInvalidInput("Invalid show method '{}'.".format(method))
        if method == "globe":
            png = self._preview(
                fmt="png", dpi=dpi, anti_alias=True, as_bytes=True, transparent=True
            )
            img = worldwind_show(
                image=png,
                width=width,
                region=self.region,
                canvas_id=self._name,
                globe_center=globe_center,
            )
        elif method == "external":
            pdf = self._preview(fmt="pdf", dpi=dpi, anti_alias=False, as_bytes=False)
            launch_external_viewer(pdf)
            img = None
        elif method == "static":
            png = self._preview(
                fmt="png", dpi=dpi, anti_alias=True, as_bytes=True, transparent=True
            )
            if Image is None:
                raise GMTError(
                    " ".join(
                        [
                            "Cannot find IPython.",
                            "Make sure you have it installed",
                            "or use 'external=True' to open in an external viewer.",
                        ]
                    )
                )
            img = Image(data=png, width=width)
        return img

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
