#!/usr/bin/env python

"""
Contains the projections supported by GMT, and the necessary mechanisms
to create a projection and output a valid GMT projection string.

>>> from pygmt import projection
>>> proj = projection.LambertAzimuthalEqualArea(lon0=30, lat0=-20, horizon=60, width="8i")
>>> proj
LambertAzimuthalEqualArea(lon0=30, lat0=-20, horizon=60, width='8i')
>>> print(proj)
A30/-20/60/8i
"""

from enum import Enum
import attr


class Supported(Enum):

    """
    The supported projections and their GMT code.
    """

    UNDEFINED = ""
    LAMBERT_AZIMUTH_EQUAL_AREA = "A"  # DONE
    ALBERS_CONIC_EQUAL_AREA = "B"  # DONE
    CASSINI_CYLINDRICAL = "C"  # DONE
    CYLINDRICAL_STEROGRAPHIC = "JCyl_stere/"  # includes `/` according to https://docs.generic-mapping-tools.org/latest/proj_codes.html  # DONE
    EQUIDISTANT_CONIC = "JD"  # DONE
    AZIMUTHAL_EQUIDISTANT = "E"  # DONE
    AZIMUTHAL_GNOMIC = "F"  # DONE
    AZIMUTHAL_ORTHOGRAPHIC = "G"  # DONE
    GENERAL_PERSPECTIVE = "G"  # DONE
    HAMMER_EQUAL_AREA = "H"
    SINUSOIDAL_EQUAL_AREA = "I"
    MILLER_CYLINDRICAL = "J"
    ECKERT_IV_EQUAL_AREA = "Kf"
    ECKERT_VI_EQUAL_AREA = "Ks"
    LAMBERT_CONIC_CONFORMAL = "L"
    MERCATOR_CYLINDRICAL = "M"  # DONE
    ROBINSON = "N"
    OBLIQUE_MERCATOR_1 = "Oa"
    OBLIQUE_MERCATOR_2 = "Ob"
    OBLIQUE_MERCATOR_3 = "Oc"
    POLAR = "P"
    POLYCONIC = "Poly"
    EQUIDISTANT_CYLINDRICAL = "Q"
    WINKEL_TRIPEL = "R"
    GENERAL_STEREOGRAPHIC = "S"  # DONE
    TRANSVERSE_MERCATOR = "T"
    UNIVERSAL_TRANSVERSE_MERCATOR = "U"
    VAN_DER_GRINTEN = "V"
    MOLLWEIDE = "W"
    LINEAR = "X"
    CYLINDRICAL_EQUAL_AREA = "Y"  # DONE


@attr.s()
class _Projection:

    """
    Base class for all projections.
    """

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False, default="{_code}")
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.UNDEFINED.value)

    def __str__(self):
        exclude = attr.fields(self.__class__)._fmt
        kwargs = attr.asdict(self, filter=attr.filters.exclude(exclude))
        return self._fmt.format(**kwargs)


@attr.s(kw_only=True)
class _Azimuthal(_Projection):

    """
    Base class for azimuthal projections.
    """

    lon0: float = attr.ib()
    lat0: float = attr.ib()
    horizon: float = attr.ib(default=90)
    width: str = attr.ib()

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False,
                        default="{_code}{lon0}/{lat0}/{horizon}/{width}")
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.UNDEFINED.value)

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value > 180:
            raise ValueError("horizon must be less than or equal to 180")


@attr.s(kw_only=True)
class _Cylindrical(_Projection):

    """
    Base class for cylindrical projections.
    """

    lon0: float = attr.ib()
    lat0: float = attr.ib()
    width: str = attr.ib()

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False,
                        default="{_code}{lon0}/{lat0}/{wdith}")
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.UNDEFINED.value)

@attr.s(kw_only=True)
class _Conic:

    """
    Base class for conic projections.
    """

    lon0: float = attr.ib()
    lat0: float = attr.ib()
    lat1: float = attr.ib()
    lat2: float = attr.ib()
    width: float = attr.ib()

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False,
                        default="{_code}{lon0}/{lat0}/{lat1}/{lat2}/{width}")


@attr.s(frozen=True)
class LambertAzimuthalEqualArea(_Azimuthal):

    """
    Definition for the lambert azimuthal equal area projection.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.LAMBERT_AZIMUTH_EQUAL_AREA.value)


@attr.s(frozen=True)
class AzimuthalEquidistant(_Azimuthal):

    """
    Definition for the azimuthal equidistant projection.
    """

    horizon: float = attr.ib(default=180, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.AZIMUTHAL_EQUIDISTANT.value)


@attr.s(frozen=True)
class AzimuthalGnomic(_Azimuthal):

    """
    Definition for the azimuthal gnomic projection.
    """

    horizon: float = attr.ib(default=60, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.AZIMUTHAL_EQUIDISTANT.value)

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value >= 90:
            raise ValueError("horizon must be less than 90")


@attr.s(frozen=True)
class AzimuthalOrthographic(_Azimuthal):

    """
    Definition for the azimuthal orthographic projection.
    """

    horizon: float = attr.ib(default=60, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.AZIMUTHAL_EQUIDISTANT.value)

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value > 90:
            raise ValueError("horizon must be less than or equal to 90")


@attr.s(frozen=True, kw_only=True)
class GeneralPerspective(_Projection):

    """
    Definition for the azimuthal general perspective projection.
    """

    lon0: float = attr.ib()
    lat0: float = attr.ib()
    altitude: float = attr.ib()
    azimuth: float = attr.ib()
    tilt: float = attr.ib()
    twist: float = attr.ib()
    Width: float = attr.ib()
    Height: float = attr.ib()
    width: float = attr.ib()

    # private; we don't want the user to care or know about
    _fmt: str = attr.ib(init=False, repr=False,
                        default=("{_code}{lon0}/{lat0}/{altitude}/{azimuth}/"
                                 "{tilt}/{twist}/{Width}/{Height}/{width}"))
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.GENERAL_PERSPECTIVE.value)


@attr.s(frozen=True)
class GeneralSterographic(_Azimuthal):

    """
    Definition for the azimuthal general sterographic projection.
    """

    horizon: float = attr.ib(default=90, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.GENERAL_STEREOGRAPHIC.value)

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value >= 180:
            raise ValueError("horizon must be less than 180")


@attr.s(frozen=True, kw_only=True)
class AlbersConicEqualArea(_Conic):

    """
    Definition for the albers conic equal area projection.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.ALBERS_CONIC_EQUAL_AREA.value)


@attr.s(frozen=True, kw_only=True)
class EquidistantConic(_Conic):

    """
    Definition for the equidistant conic projection.
    """

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.EQUIDISTANT_CONIC)


@attr.s(frozen=True)
class CassiniCylindrical(_Cylindrical):

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.CASSINI_CYLINDRICAL.value)


@attr.s(frozen=True)
class MercatorCylindrical(_Cylindrical):

    lon0: float = attr.ib(default=180, kw_only=True)
    lat0: float = attr.ib(default=0, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.MERCATOR_CYLINDRICAL.value)


@attr.s(frozen=True)
class CylindricalStereographic(_Cylindrical):

    lon0: float = attr.ib(default=180, kw_only=True)
    lat0: float = attr.ib(default=0, kw_only=True)

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.CYLINDRICAL_STEROGRAPHIC.value)


@attr.s(frozen=True)
class CylindricalEqualArea(_Cylindrical):

    # private; we don't want the user to care or know about
    _code: str = attr.ib(init=False, repr=False,
                         default=Supported.CYLINDRICAL_EQUAL_AREA.value)
