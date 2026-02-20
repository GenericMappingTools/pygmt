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
        assert str(self.prj) == "D145/-35/-30/-40/12c"


class TestCassiniCylindrical:
    """
    Tests for the Cassini Cylindrical projection.
    """

    prj = projection.CassiniCylindrical(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "C145/-35/12c"


class TestMercatorCylindrical:
    """
    Tests for the Mercator Cylindrical projection.
    """

    prj1 = projection.MercatorCylindrical(
        central_longitude=145, central_latitude=-35, width=12
    )
    prj2 = projection.MercatorCylindrical(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "M145/-35/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "M12c"


class TestCylindricalStereographic:
    """
    Tests for the Cylindrical Stereographic projection.
    """

    prj1 = projection.CylindricalStereographic(
        central_longitude=145, central_latitude=-35, width=12
    )
    prj2 = projection.CylindricalStereographic(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Cyl_stere/145/-35/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Cyl_stere/12c"


class TestCylindricalEqualArea:
    """
    Tests for the Cylindrical Equal Area projection.
    """

    prj1 = projection.CylindricalEqualArea(
        central_longitude=145, central_latitude=-35, width=12
    )
    prj2 = projection.CylindricalEqualArea(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Y145/-35/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Y12c"


class TestHammerEqualArea:
    """
    Tests for the Hammer Equal Area projection.
    """

    prj1 = projection.HammerEqualArea(central_meridian=145, width=12)
    prj2 = projection.HammerEqualArea(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "H145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "H12c"


class TestSinusoidalEqualArea:
    """
    Tests for the Sinusoidal Equal Area projection.
    """

    prj1 = projection.SinusoidalEqualArea(central_meridian=145, width=12)
    prj2 = projection.SinusoidalEqualArea(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "I145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "I12c"


class TestEckertIVEqualArea:
    """
    Tests for the Eckert IV Equal Area projection.
    """

    prj1 = projection.EckertIVEqualArea(central_meridian=145, width=12)
    prj2 = projection.EckertIVEqualArea(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Kf145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Kf12c"


class TestEckertVIEqualArea:
    """
    Tests for the Eckert VI Equal Area projection.
    """

    prj1 = projection.EckertVIEqualArea(central_meridian=145, width=12)
    prj2 = projection.EckertVIEqualArea(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Ks145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Ks12c"


class TestRobinson:
    """
    Tests for the Robinson projection.
    """

    prj1 = projection.Robinson(central_meridian=145, width=12)
    prj2 = projection.Robinson(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "N145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "N12c"


class TestWinkelTripel:
    """
    Tests for the Winkel Tripel projection.
    """

    prj1 = projection.WinkelTripel(central_meridian=145, width=12)
    prj2 = projection.WinkelTripel(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "R145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "R12c"


class TestMollweide:
    """
    Tests for the Mollweide projection.
    """

    prj1 = projection.Mollweide(central_meridian=145, width=12)
    prj2 = projection.Mollweide(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "W145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "W12c"


class TestVanDerGrinten:
    """
    Tests for the Van Der Grinten projection.
    """

    prj1 = projection.VanDerGrinten(central_meridian=145, width=12)
    prj2 = projection.VanDerGrinten(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "V145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "V12c"


class TestLambertConicConformal:
    """
    Tests for the Lambert Conic Conformal projection.
    """

    prj = projection.LambertConicConformal(
        central_longitude=145, central_latitude=-35, lat1=-30, lat2=-40, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj.unit == "c"

    def test_string_conversion(self):
        "Test the string representation of the projection class"
        assert str(self.prj) == "L145/-35/-30/-40/12c"


class TestPolyconic:
    """
    Tests for the Polyconic projection.
    """

    prj1 = projection.Polyconic(central_longitude=145, central_latitude=-35, width=12)
    prj2 = projection.Polyconic(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Poly/145/-35/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Poly/12c"


class TestMiller:
    """
    Tests for the Miller projection.
    """

    prj1 = projection.Miller(central_meridian=145, width=12)
    prj2 = projection.Miller(width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "J145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "J12c"


class TestObliqueMercator1:
    """
    Tests for the Oblique Mercator projection (option 1).
    """

    prj1 = projection.ObliqueMercator1(
        central_longitude=145, central_latitude=-35, azimuth=45, width=12
    )
    prj2 = projection.ObliqueMercator1(
        central_longitude=145,
        central_latitude=-35,
        azimuth=45,
        allow_southern_hemisphere=True,
        width=12,
    )
    prj3 = projection.ObliqueMercator1(
        central_longitude=145,
        central_latitude=-35,
        azimuth=45,
        align_yaxis=True,
        width=12,
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "O145/-35/45/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "OA145/-35/45/12c"

    def test_string_conversion3(self):
        "Test the string representation of the projection class"
        assert str(self.prj3) == "O145/-35/45/12c+v"


class TestObliqueMercator2:
    """
    Tests for the Oblique Mercator projection (option 2).
    """

    prj1 = projection.ObliqueMercator2(
        central_longitude=145,
        central_latitude=-35,
        oblique_longitude=110,
        oblique_latitude=-20,
        width=12,
    )
    prj2 = projection.ObliqueMercator2(
        central_longitude=145,
        central_latitude=-35,
        oblique_longitude=110,
        oblique_latitude=-20,
        allow_southern_hemisphere=True,
        width=12,
    )
    prj3 = projection.ObliqueMercator2(
        central_longitude=145,
        central_latitude=-35,
        oblique_longitude=110,
        oblique_latitude=-20,
        align_yaxis=True,
        width=12,
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "O145/-35/110/-20/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "OB145/-35/110/-20/12c"

    def test_string_conversion3(self):
        "Test the string representation of the projection class"
        assert str(self.prj3) == "O145/-35/110/-20/12c+v"


class TestObliqueMercator3:
    """
    Tests for the Oblique Mercator projection (option 3).
    """

    prj1 = projection.ObliqueMercator3(
        central_longitude=145,
        central_latitude=-35,
        pole_longitude=110,
        pole_latitude=-20,
        width=12,
    )
    prj2 = projection.ObliqueMercator3(
        central_longitude=145,
        central_latitude=-35,
        pole_longitude=110,
        pole_latitude=-20,
        allow_southern_hemisphere=True,
        width=12,
    )
    prj3 = projection.ObliqueMercator3(
        central_longitude=145,
        central_latitude=-35,
        pole_longitude=110,
        pole_latitude=-20,
        align_yaxis=True,
        width=12,
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "O145/-35/110/-20/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "OC145/-35/110/-20/12c"

    def test_string_conversion3(self):
        "Test the string representation of the projection class"
        assert str(self.prj3) == "O145/-35/110/-20/12c+v"


class TestTransverseMercator:
    """
    Tests for the Transverse Mercator projection.
    """

    prj1 = projection.TransverseMercator(central_longitude=145, width=12)
    prj2 = projection.TransverseMercator(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "T145/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "T145/-35/12c"


class TestUniversalTransverseMercator:
    """
    Tests for the Universal Transverse Mercator projection.
    """

    prj1 = projection.UniversalTransverseMercator(zone="-55", width=12)
    prj2 = projection.UniversalTransverseMercator(zone="55H", width=12)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "U-55/12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "U55H/12c"


class TestEquidistantCylindrical:
    """
    Tests for the Equidistant Cylindrical projection.
    """

    prj1 = projection.EquidistantCylindrical(width=12)
    prj2 = projection.EquidistantCylindrical(central_longitude=145, width=12)
    prj3 = projection.EquidistantCylindrical(
        central_longitude=145, central_latitude=-35, width=12
    )

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the projection class"
        assert str(self.prj1) == "Q12c"

    def test_string_conversion2(self):
        "Test the string representation of the projection class"
        assert str(self.prj2) == "Q145/12c"

    def test_string_conversion3(self):
        "Test the string representation of the projection class"
        assert str(self.prj3) == "Q145/-35/12c"


class TestPolar:
    """
    Tests for the Polar projection.
    """

    prj1 = projection.Polar(width=10)
    prj2 = projection.Polar(width=10, clockwise=True, origin=45, offset=10)
    prj3 = projection.Polar(width=10, flip=True, flip_options=33)
    prj4 = projection.Polar(width=10, depth=True, depth_options=33)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the polar projection class"
        assert str(self.prj1) == "P10c"

    def test_string_conversion2(self):
        "Test the string representation of the polar projection class"
        assert str(self.prj2) == "P10c+a+r10+t45"

    def test_string_conversion3(self):
        "Test the string representation of the polar projection class"
        assert str(self.prj3) == "P10c+f33"

    def test_string_conversion4(self):
        "Test the string representation of the polar projection class"
        assert str(self.prj4) == "P10c+z33"

    def test_assert_depth_options(self):
        "Test that a ValueError assertion is raised for the depth options"
        with pytest.raises(ValueError):
            projection.Polar(width=10, depth=True, depth_options="ep")

    def test_assert_flip_options(self):
        "Test that a ValueError assertion is raised for the flip options"
        with pytest.raises(ValueError):
            projection.Polar(width=10, flip=True, flip_options="ep")


class TestLinear:
    """
    Tests for the Linear projection.
    """

    prj1 = projection.Linear(width=10)
    prj2 = projection.Linear(width=10, geographic=True)
    prj3 = projection.Linear(width=10, log_x=True)
    prj4 = projection.Linear(width=10, log_x=True, height=35, log_y=True)
    prj5 = projection.Linear(width=10, power_x=0.5, height=35, power_y=3)
    prj6 = projection.Linear(width=10, time_x="t", height=35, power_y=3)

    def test_default_unit(self):
        "Test the default value for the figure units"
        assert self.prj1.unit == "c"

    def test_string_conversion1(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj1) == "X10c"

    def test_string_conversion2(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj2) == "X10cd"

    def test_string_conversion3(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj3) == "X10cl"

    def test_string_conversion4(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj4) == "X10cl/35cl"

    def test_string_conversion5(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj5) == "X10cp0.5/35cp3"

    def test_string_conversion6(self):
        "Test the string representation of the linear projection class"
        assert str(self.prj6) == "X10ct/35cp3"

    def test_assert_log_y(self):
        "Test that setting log_y without setting height raises a ValueError"
        with pytest.raises(ValueError, match=r"height .* log scaling"):
            projection.Linear(width=10, log_x=True, log_y=True)

    def test_assert_power_y(self):
        "Test that setting power_y without setting height raises a ValueError"
        with pytest.raises(ValueError, match=r"height .* power scaling"):
            projection.Linear(width=10, power_y=True)

    def test_assert_time_code(self):
        "Test that setting an incorrect time code raises a ValueError"
        with pytest.raises(ValueError):
            projection.Linear(width=10, time_x="s")

    def test_assert_log_power(self):
        "Test that setting both log_x and power_x keywords raises a ValueError"
        with pytest.raises(ValueError, match=r".* are mutually exclusive"):
            projection.Linear(width=10, log_x=True, power_x=0.5)

    def test_assert_power_time(self):
        "Test that setting both power_x and time_x keywords raises a ValueError"
        with pytest.raises(ValueError, match=r".* are mutually exclusive"):
            projection.Linear(width=10, power_x=0.5, time_x="t")

    def test_assert_log_time(self):
        "Test that setting both log_x and time_x keywords raises a ValueError"
        with pytest.raises(ValueError, match=r".* are mutually exclusive"):
            projection.Linear(width=10, log_x=True, time_x="t")
