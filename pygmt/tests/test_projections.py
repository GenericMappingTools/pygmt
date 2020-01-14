"""
Test the projection configuration classes.
"""
import pytest

from .. import projection


class TestLambertAzimuthalEqualArea:
    """
    Tests for the Lambert Azimuthal Equal Area projection.
    """

    prj = projection.LambertAzimuthalEqualArea(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_horizon(self):
        "Test the default value for the horizon"
        assert self.prj.horizon == 90

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "A145/-35/90/12c"


class TestAzimuthalEquidistant:
    """
    Tests for the Azimuth Equidistant projection.
    """

    prj = projection.AzimuthalEquidistant(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_horizon(self):
        "Test the default value for the horizon"
        assert self.prj.horizon == 180

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "E145/-35/180/12c"


class TestAzimuthalGnomic:
    """
    Tests for the Azimuth Gnomic projection.
    """

    prj = projection.AzimuthalGnomic(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_horizon(self):
        "Test the default value for the horizon"
        assert self.prj.horizon == 60

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "F145/-35/60/12c"

    def test_horizon_upper_limit(self):
        "Test that the horizon is < 90"
        with pytest.raises(ValueError):
            projection.AzimuthalGnomic(
                central_longitude=145, central_latitude=-35, horizon=90, width=12
            )


class TestAzimuthalOrthographic:
    """
    Tests for the Azimuth Orthographic projection.
    """

    prj = projection.AzimuthalOrthographic(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_horizon(self):
        "Test the default value for the horizon"
        assert self.prj.horizon == 90

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "G145/-35/90/12c"

    def test_horizon_upper_limit(self):
        "Test that the horizon is < 90"
        with pytest.raises(ValueError):
            projection.AzimuthalOrthographic(
                central_longitude=145, central_latitude=-35, horizon=90.0001, width=12
            )


class TestGeneralPerspective:
    """
    Tests for the General Perspective projection.
    """

    prj = projection.GeneralPerspective(
        central_longitude=145,
        central_latitude=-35,
        width=12,
        altitude=10,
        azimuth=270,
        tilt=10,
        twist=5,
        viewport_width=9,
        viewport_height=7,
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "G145/-35/10/270/10/5/9/7/12c"


class TestGeneralSterographic:
    """
    Tests for the General Sterographic projection.
    """

    prj = projection.GeneralSterographic(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_horizon(self):
        "Test the default value for the horizon"
        assert self.prj.horizon == 90

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "S145/-35/90/12c"

    def test_horizon_upper_limit(self):
        "Test that the horizon is < 180"
        with pytest.raises(ValueError):
            projection.GeneralSterographic(
                central_longitude=145, central_latitude=-35, horizon=180, width=12
            )


class TestAlbersConicEqualArea:
    """
    Tests for the Albers Conic Equal Area projection.
    """

    prj = projection.AlbersConicEqualArea(
        central_longitude=145, central_latitude=-35, lat1=-30, lat2=-40, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "B145/-35/-30/-40/12c"


class TestEquidistantConic:
    """
    Tests for the Equidistant Conic projection.
    """

    prj = projection.EquidistantConic(
        central_longitude=145, central_latitude=-35, lat1=-30, lat2=-40, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "JD145/-35/-30/-40/12c"
