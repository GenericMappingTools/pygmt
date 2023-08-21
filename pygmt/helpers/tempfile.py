"""
Utilities for dealing with temporary file management.
"""
import os
import uuid
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import numpy as np


def unique_name():
    """
    Generate a unique name.

    Useful for generating unique names for figures (otherwise GMT will plot
    everything on the same figure instead of creating a new one).

    Returns
    -------
    name : str
        A unique name generated by :func:`uuid.uuid4`
    """
    return uuid.uuid4().hex


class GMTTempFile:
    """
    Context manager for creating closed temporary files.

    This class does not return a file-like object. So, you can't do
    ``for line in GMTTempFile()``, for example, or pass it to things that
    need file objects.

    Parameters
    ----------
    prefix : str
        The temporary file name begins with the prefix.
    suffix : str
        The temporary file name ends with the suffix.

    Examples
    --------
    >>> import numpy as np
    >>> with GMTTempFile() as tmpfile:
    ...     # write data to temporary file
    ...     x = y = z = np.arange(0, 3, 1)
    ...     np.savetxt(tmpfile.name, (x, y, z), fmt="%.1f")
    ...     lines = tmpfile.read()
    ...     print(lines)
    ...     nx, ny, nz = tmpfile.loadtxt(unpack=True, dtype=float)
    ...     print(nx, ny, nz)
    ...
    0.0 1.0 2.0
    0.0 1.0 2.0
    0.0 1.0 2.0
    <BLANKLINE>
    [0. 0. 0.] [1. 1. 1.] [2. 2. 2.]
    """

    def __init__(self, prefix="pygmt-", suffix=".txt"):
        with NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False) as tmpfile:
            self.name = tmpfile.name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if os.path.exists(self.name):
            os.remove(self.name)

    def read(self, keep_tabs=False):
        """
        Read the entire contents of the file as a Unicode string.

        Parameters
        ----------
        keep_tabs : bool
            If False, replace the tabs that GMT uses with spaces.

        Returns
        -------
        content : str
            Content of the temporary file as a Unicode string.
        """
        with open(self.name, mode="r", encoding="utf8") as tmpfile:
            content = tmpfile.read()
            if not keep_tabs:
                content = content.replace("\t", " ")
            return content

    def loadtxt(self, **kwargs):
        """
        Load data from the temporary file using numpy.loadtxt.

        Parameters
        ----------
        kwargs : dict
            Any keyword arguments that can be passed to numpy.loadtxt.

        Returns
        -------
        ndarray
            Data read from the text file.
        """
        return np.loadtxt(self.name, **kwargs)


@contextmanager
def tempfile_from_geojson(geojson):
    """
    Saves any geo-like Python object which implements ``__geo_interface__``
    (e.g. a geopandas.GeoDataFrame or shapely.geometry) to a temporary OGR_GMT
    text file.

    Parameters
    ----------
    geojson : geopandas.GeoDataFrame
        A geopandas GeoDataFrame, or any geo-like Python object which
        implements __geo_interface__, i.e. a GeoJSON.

    Yields
    ------
    tmpfilename : str
        A temporary OGR_GMT format file holding the geographical data.
        E.g. '1a2b3c4d5e6.gmt'.
    """
    with GMTTempFile(suffix=".gmt") as tmpfile:
        # pylint: disable=import-outside-toplevel
        import geopandas as gpd

        os.remove(tmpfile.name)  # ensure file is deleted first
        ogrgmt_kwargs = {"filename": tmpfile.name, "driver": "OGR_GMT", "mode": "w"}
        try:
            # Map int/int64 to int32 since OGR_GMT only supports 32-bit integer
            # https://github.com/geopandas/geopandas/issues/967#issuecomment-842877704
            # https://github.com/GenericMappingTools/pygmt/issues/2497
            if geojson.index.name is None:
                geojson.index.name = "index"
            geojson = geojson.reset_index(drop=False)
            schema = gpd.io.file.infer_schema(geojson)
            for col, dtype in schema["properties"].items():
                if dtype in ("int", "int64"):
                    schema["properties"][col] = "int32"
            ogrgmt_kwargs["schema"] = schema
            # Using geopandas.to_file to directly export to OGR_GMT format
            geojson.to_file(**ogrgmt_kwargs)
        except AttributeError:
            # Other 'geo' formats which implement __geo_interface__
            import json

            import fiona

            with fiona.Env():
                jsontext = json.dumps(geojson.__geo_interface__)
                # Do Input/Output via Fiona virtual memory
                with fiona.io.MemoryFile(file_or_bytes=jsontext.encode()) as memfile:
                    geoseries = gpd.GeoSeries.from_file(filename=memfile)
                    geoseries.to_file(**ogrgmt_kwargs)

        yield tmpfile.name


@contextmanager
def tempfile_from_image(image):
    """
    Saves a 3-band :class:`xarray.DataArray` to a temporary GeoTIFF file via
    rioxarray.

    Parameters
    ----------
    image : xarray.DataArray
        An xarray.DataArray with three dimensions, having a shape like
        (3, Y, X).

    Yields
    ------
    tmpfilename : str
        A temporary GeoTIFF file holding the image data. E.g. '1a2b3c4d5.tif'.
    """
    with GMTTempFile(suffix=".tif") as tmpfile:
        os.remove(tmpfile.name)  # ensure file is deleted first
        try:
            image.rio.to_raster(raster_path=tmpfile.name)
        except AttributeError as e:  # object has no attribute 'rio'
            raise ImportError(
                "Package `rioxarray` is required to be installed to use this function. "
                "Please use `python -m pip install rioxarray` or "
                "`mamba install -c conda-forge rioxarray` "
                "to install the package."
            ) from e
        yield tmpfile.name
