"""
conftest.py for pytest.
"""

import numpy as np
from packaging.version import Version

# Keep this until we require numpy to be >=2.0
# Address https://github.com/GenericMappingTools/pygmt/issues/2628.
if Version(np.__version__) >= Version("2.0.0.dev0+git20230726"):
    np.set_printoptions(legacy="1.25")  # type: ignore[arg-type]
