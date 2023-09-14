"""
Test the _load_remote_dataset function.
"""
import pytest
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.exceptions import GMTInvalidInput


def load_remote_dataset_wrapper(resolution="01d", region=None, registration=None):
    """
    Wrapper for _load_remote_dataset using the earth age dataset as an example.
    """
    return _load_remote_dataset(
        dataset_name="earth_age",
        dataset_prefix="earth_age_",
        resolution=resolution,
        region=region,
        registration=registration,
    )


def test_load_remote_dataset_invalid_resolutions():
    """
    Make sure _load_remote_dataset fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_remote_dataset_wrapper(resolution=resolution)
