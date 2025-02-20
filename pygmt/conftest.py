"""
conftest.py for pytest.
"""

import numpy as np
from packaging.version import Version

# TODO(NumPy>=2.0): Remove the conftest.py file.
# Address https://github.com/GenericMappingTools/pygmt/issues/2628.
if Version(np.__version__) >= Version("2.0.0.dev0+git20230726"):
    np.set_printoptions(legacy="1.25")  # type: ignore[arg-type]
