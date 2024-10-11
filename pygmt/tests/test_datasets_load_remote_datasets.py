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
        name="earth_age",
        prefix="earth_age",
        resolution=resolution,
        region=region,
        registration=registration,
    )


@pytest.mark.benchmark
def test_load_remote_dataset_benchmark_with_region():
    """
    Benchmark loading a remote dataset with 'region'.
    """
    data = load_remote_dataset_wrapper(resolution="01d", region=[-10, 10, -5, 5])
    assert data.name == "z"
    assert data.attrs["long_name"] == "ages (Myr)"
    assert data.attrs["units"] == "Myr"
    assert data.attrs["horizontal_datum"] == "WGS84"
    assert data.gmt.registration == 0
    assert data.shape == (11, 21)
    # Can't access the cpt attribute using virtual files
    # assert data.attrs["cpt"] == "@earth_age.cpt"


def test_load_remote_dataset_invalid_resolutions():
    """
    Make sure _load_remote_dataset fails for invalid resolutions.
    """
    resolutions = "1m 1d bla 60d 001m 03".split()
    resolutions.append(60)
    for resolution in resolutions:
        with pytest.raises(GMTInvalidInput):
            load_remote_dataset_wrapper(resolution=resolution)


def test_load_remote_dataset_invalid_registration():
    """
    Make sure _load_remote_dataset fails for invalid registrations.
    """
    with pytest.raises(GMTInvalidInput):
        load_remote_dataset_wrapper(registration="improper_type")


def test_load_remote_dataset_tiled_grid_without_region():
    """
    Make sure _load_remote_dataset fails when trying to load a tiled grid without
    specifying a region.
    """
    with pytest.raises(GMTInvalidInput):
        load_remote_dataset_wrapper(resolution="01m")


def test_load_remote_dataset_incorrect_resolution_registration():
    """
    Make sure _load_remote_dataset fails when trying to load a grid registration with an
    unavailable resolution.
    """
    with pytest.raises(GMTInvalidInput):
        load_remote_dataset_wrapper(
            resolution="01m", region=[0, 1, 3, 5], registration="pixel"
        )
