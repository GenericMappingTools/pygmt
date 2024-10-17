"""
Utilities for dealing with temporary file management.
"""

import io
import uuid
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
from packaging.version import Version


def unique_name() -> str:
    """
    Generate a unique name.

    Useful for generating unique names for figures. Otherwise GMT will plot everything
    on the same figure instead of creating a new one.

    Returns
    -------
    name
        A unique name generated by :func:`uuid.uuid4`.
    """
    return uuid.uuid4().hex


class GMTTempFile:
    """
    Context manager for creating closed temporary files.

    This class does not return a file-like object. So, you can't iterate over the object
    like ``for line in GMTTempFile()``, or pass it to things that need a file object.

    Parameters
    ----------
    prefix
        The temporary file name begins with the prefix.
    suffix
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
    0.0 1.0 2.0
    0.0 1.0 2.0
    0.0 1.0 2.0
    <BLANKLINE>
    [0. 0. 0.] [1. 1. 1.] [2. 2. 2.]
    """

    def __init__(self, prefix: str = "pygmt-", suffix: str = ".txt"):
        """
        Initialize the object.
        """
        with NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False) as tmpfile:
            self.name = tmpfile.name

    def __enter__(self):
        """
        Do nothing but return the object.
        """
        return self

    def __exit__(self, *args):
        """
        Remove the temporary file.
        """
        Path(self.name).unlink(missing_ok=True)

    def read(self, keep_tabs: bool = False) -> str:
        """
        Read the entire contents of the file as a Unicode string.

        Parameters
        ----------
        keep_tabs
            If False, replace the tabs that GMT uses with spaces.

        Returns
        -------
        content
            Content of the temporary file as a Unicode string.
        """
        content = Path(self.name).read_text(encoding="utf8")
        if not keep_tabs:
            content = content.replace("\t", " ")
        return content

    def loadtxt(self, **kwargs) -> np.ndarray:
        """
        Load data from the temporary file using numpy.loadtxt.

        Parameters
        ----------
        kwargs
            Any keyword arguments that can be passed to :func:`np.loadtxt`.

        Returns
        -------
        ndarray
            Data read from the text file.
        """
        return np.loadtxt(self.name, **kwargs)


@contextmanager
def tempfile_from_geojson(geojson):
    """
    Saves any geo-like Python object which implements ``__geo_interface__`` (e.g. a
    geopandas.GeoDataFrame or shapely.geometry) to a temporary OGR_GMT text file.

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
        import geopandas as gpd

        Path(tmpfile.name).unlink()  # Ensure file is deleted first
        ogrgmt_kwargs = {"filename": tmpfile.name, "driver": "OGR_GMT", "mode": "w"}
        try:
            # OGR_GMT only supports 32-bit integers. We need to map int/int64
            # types to int32/float types depending on if the column has an
            # 32-bit integer overflow issue. Related issues:
            # https://github.com/geopandas/geopandas/issues/967#issuecomment-842877704
            # https://github.com/GenericMappingTools/pygmt/issues/2497

            int32_info = np.iinfo(np.int32)

            if Version(gpd.__version__).major < 1:  # GeoPandas v0.x
                # The default engine 'fiona' supports the 'schema' parameter.
                if geojson.index.name is None:
                    geojson.index.name = "index"
                geojson = geojson.reset_index(drop=False)
                schema = gpd.io.file.infer_schema(geojson)
                for col, dtype in schema["properties"].items():
                    if dtype in {"int", "int64"}:
                        overflow = (
                            geojson[col].max() > int32_info.max
                            or geojson[col].min() < int32_info.min
                        )
                        schema["properties"][col] = "float" if overflow else "int32"
                        geojson[col] = geojson[col].astype(schema["properties"][col])
                ogrgmt_kwargs["schema"] = schema
            else:  # GeoPandas v1.x.
                # The default engine "pyogrio" doesn't support the 'schema' parameter
                # but we can change the dtype directly.
                for col in geojson.columns:
                    if geojson[col].dtype.name in {"int", "int64", "Int64"}:
                        overflow = (
                            geojson[col].max() > int32_info.max
                            or geojson[col].min() < int32_info.min
                        )
                        dtype = "float" if overflow else "int32"
                        geojson[col] = geojson[col].astype(dtype)
            # Using geopandas.to_file to directly export to OGR_GMT format
            geojson.to_file(**ogrgmt_kwargs)
        except AttributeError:
            # Other 'geo' formats which implement __geo_interface__
            import json

            jsontext = json.dumps(geojson.__geo_interface__)
            gpd.read_file(filename=io.StringIO(jsontext)).to_file(**ogrgmt_kwargs)

        yield tmpfile.name


@contextmanager
def tempfile_from_image(image):
    """
    Saves a 3-band :class:`xarray.DataArray` to a temporary GeoTIFF file via rioxarray.

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
        Path(tmpfile.name).unlink()  # Ensure file is deleted first
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
