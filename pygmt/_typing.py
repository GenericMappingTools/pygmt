"""
Type aliases for type hints.
"""

import contextlib
import importlib
import os
from collections.abc import Sequence
from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr

# Anchor codes
AnchorCode = Literal["TL", "TC", "TR", "ML", "MC", "MR", "BL", "BC", "BR"]

# String array types
StringArrayTypes = Sequence[str] | np.ndarray
with contextlib.suppress(ImportError):
    StringArrayTypes |= importlib.import_module(name="pyarrow").StringArray

# PathLike and TableLike types
PathLike = str | os.PathLike
TableLike = dict | np.ndarray | pd.DataFrame | xr.Dataset
with contextlib.suppress(ImportError):
    TableLike |= importlib.import_module(name="geopandas").GeoDataFrame
