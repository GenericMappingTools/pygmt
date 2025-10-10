"""
Define the Figure class that handles all plotting.
"""

import base64
import os
import warnings
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, overload

from pygmt._typing import PathLike

try:
    import IPython

    _HAS_IPYTHON = True
except ImportError:
    _HAS_IPYTHON = False

import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import launch_external_viewer, unique_name


def _get_default_display_method() -> Literal["external", "notebook", "none"]:
    """
    Get the default method to display preview images.

    The function checks the current environment and determines the most suitable method
    to display preview images when calling :meth:`pygmt.Figure.show`. Valid display
    methods are:

    - ``"external"``: External PDF preview using the default PDF viewer
    - ``"notebook"``: Inline PNG preview in the current notebook
    - ``"none"``: Disable image preview

    The default display method is ``"notebook"`` in the Jupyter notebook environment,
    and ``"external"`` in other cases.

    Setting environment variable :term:`PYGMT_USE_EXTERNAL_DISPLAY` to ``"false"`` can
    disable image preview in external viewers. It's useful when running the tests and
    building the documentation to avoid popping up windows.

    Returns
    -------
    method
        The default display method.
    """
    # Check if an IPython kernel is running.
    if _HAS_IPYTHON and (ipy := IPython.get_ipython()) and "IPKernelApp" in ipy.config:
        return "notebook"
    # Check if the environment variable PYGMT_USE_EXTERNAL_DISPLAY is set to "false".
    if os.environ.get("PYGMT_USE_EXTERNAL_DISPLAY", "true").lower() == "false":
        return "none"
    # Fallback to using the external viewer.
    return "external"


# A registry of all figures that have had "show" called in this session.
# This is needed for the sphinx-gallery scraper in pygmt/sphinx_gallery.py
SHOWED_FIGURES = []
# Configurations for figure display.
SHOW_CONFIG = {
    "method": _get_default_display_method(),  # The image preview display method.
}


class Figure:
    """
    A GMT figure to handle all plotting.

    Use the plotting methods of this class to add elements to the figure. You can
    preview the figure using :meth:`pygmt.Figure.show` and save the figure to a file
    using :meth:`pygmt.Figure.savefig`.

    Examples
    --------

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 360, -90, 90], projection="W15c", frame=True)
    >>> fig.savefig("my-figure.png")
    >>> # Make sure the figure file is generated and clean it up
    >>> from pathlib import Path
    >>> assert Path("my-figure.png").exists()
    >>> Path("my-figure.png").unlink()

    The plot region can be specified through ISO country codes (for example, ``"JP"``
    for Japan):

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="JP", projection="M7c", frame=True)
    >>> # The fig.region attribute shows the WESN bounding box for the figure
    >>> print(", ".join(f"{i:.2f}" for i in fig.region))
    122.94, 145.82, 20.53, 45.52
    """

    def __init__(self) -> None:
        self._name = unique_name()
        self._preview_dir = TemporaryDirectory(prefix=f"{self._name}-preview-")
        self._activate_figure()

    def __del__(self) -> None:
        """
        Clean up the temporary directory that stores the previews.
        """
        if hasattr(self, "_preview_dir"):
            self._preview_dir.cleanup()

    def _activate_figure(self) -> None:
        """
        Start and/or activate the current figure.

        All plotting commands run afterward will append to this figure.
        """
        fmt = "-"  # Passing format "-" tells pygmt.end to not produce any files.
        with Session() as lib:
            lib.call_module(module="figure", args=[self._name, fmt])

    # TODO(PyGMT>=v0.18.0):  Remove the _preprocess method.
    def _preprocess(self, **kwargs):
        """
        Call the ``figure`` module before each plotting command to ensure we're plotting
        to this particular figure.
        """
        self._activate_figure()
        warnings.warn(
            "The Figure._preprocess() method is deprecated since v0.16.0 and will be "
            "removed in v0.18.0. Use Figure._activate_figure() instead.",
            FutureWarning,
            stacklevel=2,
        )
        return kwargs

    @property
    def region(self) -> np.ndarray:
        """
        The geographic WESN bounding box for the current figure.
        """
        self._activate_figure()
        with Session() as lib:
            wesn = lib.extract_region()
        return wesn

    def savefig(
        self,
        fname: PathLike,
        transparent: bool = False,
        crop: bool = True,
        anti_alias: bool = True,
        show: bool = False,
        worldfile: bool = False,
        **kwargs,
    ) -> None:
        """
        Save the figure to an image file.

        Supported image formats and their extensions:

        **Raster image formats**

        - BMP (``.bmp``)
        - JPEG (``.jpg`` or ``.jpeg``)
        - GeoTIFF (``.tiff``)
        - PNG (``.png``)
        - PPM (``.ppm``)
        - TIFF (``.tif``)

        **Vector image formats**

        - EPS (``.eps``)
        - PDF (``.pdf``)

        Besides the above formats, you can also save the figure to a KML file
        (``.kml``), with a companion PNG file generated automatically. The KML file can
        be viewed in Google Earth.

        You can pass in any keyword arguments that :meth:`pygmt.Figure.psconvert`
        accepts.

        Parameters
        ----------
        fname
            The desired figure file name, including the extension. See the list of
            supported formats and their extensions above.
        transparent
            Use a transparent background for the figure. Only valid for PNG format and
            the PNG file asscoiated with KML format.
        crop
            Crop the figure canvas (page) to the plot area.
        anti_alias
            Use anti-aliasing when creating raster images. Ignored if creating vector
            images. More specifically, it passes the arguments ``"t2"`` and ``"g2"`` to
            the ``anti_aliasing`` parameter of :meth:`pygmt.Figure.psconvert`.
        show
            Display the figure in an external viewer.
        worldfile
            Create a companion `world file <https://en.wikipedia.org/wiki/World_file>`__
            for the figure. The world file will have the same name as the figure file
            but with different extension (e.g., ``.tfw`` for ``.tif``). See
            https://en.wikipedia.org/wiki/World_file#Filename_extension for the
            convention of world file extensions. This parameter only works for raster
            image formats (except GeoTIFF).
        **kwargs : dict
            Additional keyword arguments passed to :meth:`pygmt.Figure.psconvert`. Valid
            parameters are ``dpi``, ``gs_path``, ``gs_option``, ``resize``,
            ``bb_style``, and ``verbose``.
        """
        # All supported formats
        fmts = {
            "bmp": "b",
            "eps": "e",
            "jpg": "j",
            "kml": "G" if transparent is True else "g",
            "pdf": "f",
            "png": "G" if transparent is True else "g",
            "ppm": "m",
            "tif": "t",
            "tiff": None,  # GeoTIFF doesn't need the -T option
        }

        fname = Path(fname)
        prefix, suffix = fname.with_suffix("").as_posix(), fname.suffix
        ext = suffix[1:].lower()  # Remove the . and normalize to lowercase

        match ext:
            case "jpeg":  # Alias jpeg to jpg
                ext = "jpg"
            case "tiff":  # GeoTIFF
                kwargs["W"] = "+g"
            case "kml":  # KML
                kwargs["W"] = "+k"
            case "ps":
                raise GMTValueError(
                    ext,
                    description="file extension",
                    reason="Extension '.ps' is not supported. Use '.eps' or '.pdf' instead.",
                )
            case ext if ext not in fmts:
                raise GMTValueError(
                    ext, description="file extension", choices=fmts.keys()
                )

        if transparent and ext not in {"kml", "png"}:
            raise GMTValueError(
                transparent,
                description="value for parameter 'transparent'",
                reason=f"Transparency unavailable for '{ext}', only for png and kml.",
            )
        if anti_alias:
            kwargs["Qt"] = 2
            kwargs["Qg"] = 2

        if worldfile:
            if ext in {"eps", "kml", "pdf", "tiff"}:
                raise GMTValueError(
                    ext,
                    description="file extension",
                    choices=["eps", "kml", "pdf", "tiff"],
                    reason="Saving a world file is not supported for this format.",
                )
            kwargs["W"] = True

        # pytest-mpl v0.17.0 added the "metadata" parameter to Figure.savefig, which is
        # not recognized. So remove it before calling Figure.psconvert.
        kwargs.pop("metadata", None)
        self.psconvert(prefix=prefix, fmt=fmts[ext], crop=crop, **kwargs)

        # Rename if file extension doesn't match the input file suffix.
        if ext != suffix[1:]:
            fname.with_suffix("." + ext).rename(fname)

        if show:
            launch_external_viewer(str(fname))

    def show(
        self,
        method: Literal["external", "notebook", "none", None] = None,
        dpi: int = 300,
        width: int = 500,
        waiting: float = 0.5,
        **kwargs,
    ) -> None:
        """
        Display a preview of the figure.

        Inserts the preview in the Jupyter notebook output if available, otherwise opens
        it in the default viewer for your operating system (falls back to the default
        web browser).

        Use :func:`pygmt.set_display` to select the default display method
        (``"notebook"``, ``"external"``, ``"none"`` or ``None``).

        The ``method`` parameter allows to override the default display method for the
        current figure. The parameters ``dpi`` and ``width`` can be used to control the
        resolution and dimension of the figure in the notebook.

        The external viewer can be disabled by setting the environment variable
        :term:`PYGMT_USE_EXTERNAL_DISPLAY` to ``"false"``. This is useful when running
        tests and building the documentation to avoid popping up windows.

        The external viewer does not block the current process, thus it's necessary to
        suspend the execution of the current process for a short while after launching
        the external viewer, so that the preview image won't be deleted before the
        external viewer tries to open it. Set the ``waiting`` parameter to a larger
        number if the image viewer on your computer is slow to open the figure.

        Parameters
        ----------
        method
            The method to display the current image preview. Choose from:

            - ``"external"``: External PDF preview using the default PDF viewer
            - ``"notebook"``: Inline PNG preview in the current notebook
            - ``"none"``: Disable image preview
            - ``None``: Reset to the default display method

            The default display method is ``"external"`` in Python consoles and
            ``"notebook"`` in Jupyter notebooks, but can be changed by
            :func:`pygmt.set_display`.

        dpi
            The image resolution (dots per inch) in Jupyter notebooks.
        width
            The image width (in pixels) in Jupyter notebooks.
        waiting
            Suspend the execution of the current process for a given number of seconds
            after launching an external viewer. Only works if ``method="external"``.
        **kwargs : dict
            Additional keyword arguments passed to :meth:`pygmt.Figure.psconvert`. Valid
            parameters are ``gs_path``, ``gs_option``, ``resize``, ``bb_style``, and
            ``verbose``.
        """
        # Module level variable to know which figures had their show method called.
        # Needed for the sphinx-gallery scraper.
        SHOWED_FIGURES.append(self)

        # Set the display method
        if method is None:
            method = SHOW_CONFIG["method"]

        match method:
            case "notebook":
                if not _HAS_IPYTHON:
                    msg = (
                        "Notebook display is selected, but IPython is not available. "
                        "Make sure you have IPython installed, "
                        "or run the script in a Jupyter notebook."
                    )
                    raise ImportError(msg)
                png = self._preview(
                    fmt="png", dpi=dpi, anti_alias=True, as_bytes=True, **kwargs
                )
                IPython.display.display(IPython.display.Image(data=png, width=width))
            case "external":
                pdf = self._preview(
                    fmt="pdf", dpi=dpi, anti_alias=False, as_bytes=False, **kwargs
                )
                launch_external_viewer(pdf, waiting=waiting)
            case "none":
                pass  # Do nothing
            case _:
                raise GMTValueError(
                    method,
                    description="display method",
                    choices=["external", "notebook", "none", None],
                )

    @overload
    def _preview(
        self, fmt: str, dpi: int, as_bytes: Literal[True] = True, **kwargs
    ) -> bytes: ...
    @overload
    def _preview(
        self, fmt: str, dpi: int, as_bytes: Literal[False] = False, **kwargs
    ) -> str: ...
    def _preview(self, fmt: str, dpi: int, as_bytes: bool = False, **kwargs):
        """
        Grab a preview of the figure.

        Parameters
        ----------
        fmt
            The image format. Can be any extension that :meth:`pygmt.Figure.savefig`
            recognizes.
        dpi
            The image resolution (dots per inch).
        as_bytes
            If ``True``, will load the binary contents of the image as a bytes object,
            and return that instead of the file name.

        Returns
        -------
        preview
            If ``as_bytes = False``, this is the file name of the preview image file.
            Otherwise, it is the file content loaded as a bytes object.
        """
        fname = Path(self._preview_dir.name) / f"{self._name}.{fmt}"
        self.savefig(fname, dpi=dpi, **kwargs)
        if as_bytes:
            return fname.read_bytes()
        return fname

    def _repr_png_(self) -> bytes:
        """
        Show a PNG preview if the object is returned in an interactive shell.

        For the Jupyter notebook or IPython Qt console.
        """
        png = self._preview(fmt="png", dpi=70, anti_alias=True, as_bytes=True)
        return png

    def _repr_html_(self) -> str:
        """
        Show the PNG image embedded in HTML with a controlled width.

        Looks better than the raw PNG.
        """
        raw_png = self._preview(fmt="png", dpi=300, anti_alias=True, as_bytes=True)
        base64_png = base64.encodebytes(raw_png)
        html = '<img src="data:image/png;base64,{image}" width="{width}px">'
        return html.format(image=base64_png.decode("utf-8"), width=500)

    from pygmt.src import (  # type: ignore[misc] # noqa: PLC0415
        basemap,
        coast,
        colorbar,
        contour,
        grdcontour,
        grdimage,
        grdview,
        histogram,
        hlines,
        image,
        inset,
        legend,
        logo,
        meca,
        plot,
        plot3d,
        psconvert,
        rose,
        set_panel,
        shift_origin,
        solar,
        subplot,
        ternary,
        text,
        tilemap,
        timestamp,
        velo,
        vlines,
        wiggle,
    )


def set_display(method: Literal["external", "notebook", "none", None] = None) -> None:
    """
    Set the display method when calling :meth:`pygmt.Figure.show`.

    Parameters
    ----------
    method
        The method to display an image preview. Choose from:

        - ``"external"``: External PDF preview using the default PDF viewer
        - ``"notebook"``: Inline PNG preview in the current notebook
        - ``"none"``: Disable image preview
        - ``None``: Reset to the default display method, which is either ``"external"``
          in Python consoles or ``"notebook"`` in Jupyter notebooks.

    Examples
    --------
    Let's assume that you're using a Jupyter Notebook:

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/5c", frame=True)
    >>> fig.show()  # Will display a PNG image in the current notebook
    >>>
    >>> # Set the display method to "external"
    >>> pygmt.set_display(method="external")  # doctest: +SKIP
    >>> fig.show()  # Will display a PDF image using the default PDF viewer
    >>>
    >>> # Set the display method to "none"
    >>> pygmt.set_display(method="none")
    >>> fig.show()  # Will not show any image
    >>>
    >>> # Reset to the default display method
    >>> pygmt.set_display(method=None)
    >>> fig.show()  # Again, will show a PNG image in the current notebook
    """
    match method:
        case "external" | "notebook" | "none":
            SHOW_CONFIG["method"] = method
        case None:
            SHOW_CONFIG["method"] = _get_default_display_method()
        case _:
            raise GMTValueError(
                method,
                description="display method",
                choices=["external", "notebook", "none", None],
            )
