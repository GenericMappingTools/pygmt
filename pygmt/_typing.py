"""
Type aliases for type hints.
"""

import contextlib
import importlib
from collections.abc import Sequence
from typing import Literal

import numpy as np

# Anchor codes
AnchorCode = Literal["TL", "TC", "TR", "ML", "MC", "MR", "BL", "BC", "BR"]

# String array types
StringArrayTypes = Sequence[str] | np.ndarray
with contextlib.suppress(ImportError):
    StringArrayTypes |= importlib.import_module(name="pyarrow").StringArray
