"""
Contains the projections supported by GMT, and the necessary mechanisms
to create a projection and output a valid GMT projection string.
"""

import numbers
from typing import Union
import attr


@attr.s()
class _Projection:
    """
    Base class for all projections.
    """

    _fmt: str = attr.ib(init=False, repr=False, default="{_code}")
    _code: str = attr.ib(init=False, repr=False, default="")

    def __str__(self):
        "Convert to the GMT-style projection code."
        exclude = attr.fields(self.__class__)._fmt
        kwargs = attr.asdict(self, filter=attr.filters.exclude(exclude))
        return f"{self._fmt.format(**kwargs)}"


@attr.s(kw_only=True)
class _Azimuthal(_Projection):
    """
    Base class for azimuthal projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    horizon: float = attr.ib(default=90)
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{horizon}/{width}{unit}",
    )

    @horizon.validator
    def check_horizon(self, attribute, value):
        """
        Validate the horizon attribute.
        """
        if value > 180:
            raise ValueError("horizon must be less than or equal to 180")


@attr.s(kw_only=True)
class _CylindricalRequired(_Projection):
    """
    Base class for cylindrical projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{width}{unit}",
    )


@attr.s(kw_only=True)
class _CylindricalOptionals(_Projection):
    """
    Base class for cylindrical projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_longitude: float = attr.ib(default=None)
    central_latitude: float = attr.ib(default=None)
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_lon0}{_lat0}{width}{unit}",
    )
    _lon0: str = attr.ib(init=False, repr=False, default="")
    _lat0: str = attr.ib(init=False, repr=False, default="")

    @central_latitude.validator
    def check_lon0(self, attribute, value):
        """
        If supplying the central latitude, then the central longitude is required.
        """
        msg = "central_longitude must be defined when defining central_latitude"
        if self.central_longitude is None and self.central_latitude is not None:
            raise ValueError(msg)

    def __attrs_post_init__(self):
        """
        The central longitude and latitude are optionals for some of the
        cylindrical projections. This work around is to preserve the
        original behaviour.
        """
        if self.central_longitude:
            object.__setattr__(self, "_lon0", f"{self.central_longitude}/")

        if self.central_latitude:
            object.__setattr__(self, "_lat0", f"{self.central_latitude}/")


@attr.s(kw_only=True)
class _Conic(_Projection):
    """
    Base class for conic projections.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    lat1: float = attr.ib()
    lat2: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{lat1}/{lat2}/{width}{unit}",
    )


@attr.s(kw_only=True)
class _Miscellaneous(_Projection):
    """
    Base class for miscellaneous projections.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_meridian: Union[float, str] = attr.ib(default="")
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_central_meridian}{width}{unit}",
    )
    _central_meridian: str = attr.ib(init=False, repr=False, default="")

    def __attrs_post_init__(self):
        """Handling the default case; not supplying a central meridian."""
        if self.central_meridian:
            cm_fmt = f"{self.central_meridian}/"
        else:
            cm_fmt = ""

        object.__setattr__(self, "_central_meridian", cm_fmt)


@attr.s(frozen=True, kw_only=True)
class _ObliqueMercator(_Projection):
    """
    Base class for the Oblique Mercator projection which has 3 config options.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    allow_southern_hemisphere : bool
        If set to True, then allow projection poles in the southern hemisphere.
        Default is to map any such poles to their antipodes in the northern
        hemisphere.
    align_yaxis : bool
        If set to True, then align the oblique with the y-axis.
        Default is to align with the x-axis.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="c")
    allow_southern_hemisphere: bool = attr.ib(default=False)
    align_yaxis: bool = attr.ib(default=False)

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="",
    )
    _code: str = attr.ib(init=False, repr=False, default="O")
    _sth_hem: str = attr.ib(init=False, repr=False, default="")
    _align_y: str = attr.ib(init=False, repr=False, default="")


@attr.s(frozen=True)
class LambertAzimuthalEqualArea(_Azimuthal):
    """
    Class definition for the Lambert azimuthal equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="A")


@attr.s(frozen=True)
class AzimuthalEquidistant(_Azimuthal):
    """
    Class definition for the azimuthal equidistant projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 180.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    horizon: float = attr.ib(default=180, kw_only=True)

    _code: str = attr.ib(init=False, repr=False, default="E")


@attr.s(frozen=True)
class AzimuthalGnomic(_Azimuthal):
    """
    Class definition for the azimuthal gnomic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 60.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    horizon: float = attr.ib(default=60, kw_only=True)

    _code: str = attr.ib(init=False, repr=False, default="F")

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
    Class definition for the azimuthal orthographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    horizon: float = attr.ib(default=90)

    _code: str = attr.ib(init=False, repr=False, default="G")

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
    Class definition for the azimuthal general perspective projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre (in degrees).
    central_latitude : float
        The latitude of the projection centre (in degrees).
    altitude : float
        The height in km of the viewpoint above local sea level.
    azimuth : float
        The direction (in degrees) in which you are looking is specified, measured clockwise from north.
    tilt : float
        The viewing angle relative to zenith (in degrees).
    twist : float
        The clockwise rotation of the image (in degrees).
    viewport_width : float
        The width of the viewing angle (in degrees).
    viewport_height : float
        The height of the viewing angle (in degrees).
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_longitude: float = attr.ib()
    central_latitude: float = attr.ib()
    altitude: float = attr.ib()
    azimuth: float = attr.ib()
    tilt: float = attr.ib()
    twist: float = attr.ib()
    viewport_width: float = attr.ib()
    viewport_height: float = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{central_latitude}/{altitude}/{azimuth}/{tilt}/{twist}/{viewport_width}/{viewport_height}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="G")


@attr.s(frozen=True)
class GeneralSterographic(_Azimuthal):
    """
    Class definition for the azimuthal general sterographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    horizon : float
        The max distance to the projection centre in degrees. Default is 90.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    horizon: float = attr.ib(default=90, kw_only=True)

    _code: str = attr.ib(init=False, repr=False, default="S")

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
    Class definition for the Albers conic equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="B")


@attr.s(frozen=True, kw_only=True)
class EquidistantConic(_Conic):
    """
    Class definition for the equidistant conic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="D")


@attr.s(frozen=True)
class CassiniCylindrical(_CylindricalRequired):
    """
    Class definition for the Cassini cylindrical projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="C")


@attr.s(frozen=True)
class MercatorCylindrical(_CylindricalOptionals):
    """
    Class definition for the Mercator cylindrical projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre. Default is 180.
    central_latitude : float
        The latitude of the projection centre. Default is 0.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="M")


@attr.s(frozen=True)
class CylindricalStereographic(_CylindricalOptionals):
    """
    Class definition for the cylindrical stereographic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre. Default is 180.
    central_latitude : float
        The latitude of the projection centre. Default is 0.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="Cyl_stere/")


@attr.s(frozen=True)
class CylindricalEqualArea(_CylindricalOptionals):
    """
    Class definition for the cylindrical equal area projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="Y")


@attr.s(frozen=True)
class HammerEqualArea(_Miscellaneous):
    """
    Class definition for the Hammer equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="H")


@attr.s(frozen=True)
class SinusoidalEqualArea(_Miscellaneous):
    """
    Class definition for the sinusoidal equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="I")


@attr.s(frozen=True)
class EckertIVEqualArea(_Miscellaneous):
    """
    Class definition for the Eckert IV equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="Kf")


@attr.s(frozen=True)
class EckertVIEqualArea(_Miscellaneous):
    """
    Class definition for the Eckert VI equal area projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="Ks")


@attr.s(frozen=True)
class Robinson(_Miscellaneous):
    """
    Class definition for the Robinson projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="N")


@attr.s(frozen=True)
class WinkelTripel(_Miscellaneous):
    """
    Class definition for the Winkel tripel projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="R")


@attr.s(frozen=True)
class Mollweide(_Miscellaneous):
    """
    Class definition for the Mollweide projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="W")


@attr.s(frozen=True)
class VanDerGrinten(_Miscellaneous):
    """
    Class definition for the Van der Grinten projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="V")


@attr.s(frozen=True)
class LambertConicConformal(_Conic):
    """
    Class definition for the Lambert conic conformal projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    lat1 : float
        The first standard parallel.
    lat2 : float
        The second standard parallel.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="L")


@attr.s(frozen=True, kw_only=True)
class Polyconic(_Projection):
    """
    Class definition for the (American) polyconic projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    # whilst this proj is part of the conic family, the params are different:
    # central lon/lat are optionals
    # two standard parallels are not defined in the proj code string
    central_longitude: float = attr.ib(default=None)
    central_latitude: float = attr.ib(default=None)
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_central_lon}{_central_lat}{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="Poly/")
    _central_lon = attr.ib(init=False, repr=False, default="")
    _central_lat = attr.ib(init=False, repr=False, default="")

    def __attrs_post_init__(self):
        """
        For frozen instances, we have to set using the traditonal way
        using object.__setattr__(self, key, value).
        """
        if self.central_longitude:
            object.__setattr__(self, "_central_lon", f"{self.central_longitude}/")

            if self.central_latitude:
                object.__setattr__(self, "_central_lat", f"{self.central_latitude}/")


@attr.s(frozen=True)
class Miller(_Miscellaneous):
    """
    Class definition for the Miller cylindrical projection.

    Parameters
    ----------
    central_meridian : float
        The central meridian/longitude to use as the centre of the map.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    # a cylindrical proj, but we're basing of miscellaneous as the
    # standard parallel param isn't defined in the code string for Miller
    _code: str = attr.ib(init=False, repr=False, default="J")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator1(_ObliqueMercator):
    """
    Class definition for the oblique Mercator 1 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    azimuth : float
        Azimuth of the oblique equator.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    allow_southern_hemisphere : bool
        If set to True, then allow projection poles in the southern hemisphere.
        Default is to map any such poles to their antipodes in the northern
        hemisphere.
    align_yaxis : bool
        If set to True, then align the oblique with the y-axis.
        Default is to align with the x-axis.
    """

    azimuth: float = attr.ib()

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_sth_hem}{central_longitude}/{central_latitude}/{azimuth}/{width}{unit}{_align_y}",
    )

    def __attrs_post_init__(self):
        """
        For frozen instances, we have to set using the traditonal way
        using object.__setattr__(self, key, value).
        """
        if self.allow_southern_hemisphere:
            object.__setattr__(self, "_sth_hem", "A")

        if self.align_yaxis:
            object.__setattr__(self, "_align_y", "+v")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator2(_ObliqueMercator):
    """
    Class definition for the oblique Mercator 2 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    oblique_longitude : float
        The longitude of the second point on an oblique equator.
    oblique_latitude : float
        The latitude of the second point on an oblique equator.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    allow_southern_hemisphere : bool
        If set to True, then allow projection poles in the southern hemisphere.
        Default is to map any such poles to their antipodes in the northern
        hemisphere.
    align_yaxis : bool
        If set to True, then align the oblique with the y-axis.
        Default is to align with the x-axis.
    """

    oblique_longitude: float = attr.ib()
    oblique_latitude: float = attr.ib()

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_sth_hem}{central_longitude}/{central_latitude}/{oblique_longitude}/{oblique_latitude}/{width}{unit}{_align_y}",
    )

    def __attrs_post_init__(self):
        """
        For frozen instances, we have to set using the traditonal way
        using object.__setattr__(self, key, value).
        """
        if self.allow_southern_hemisphere:
            object.__setattr__(self, "_sth_hem", "B")

        if self.align_yaxis:
            object.__setattr__(self, "_align_y", "+v")


@attr.s(frozen=True, kw_only=True)
class ObliqueMercator3(_ObliqueMercator):
    """
    Class definition for the oblique Mercator 3 projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    pole_longitude : float
        The longitude of the projection pole.
    pole_latitude : float
        The latitude of the projection pole.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    allow_southern_hemisphere : bool
        If set to True, then allow projection poles in the southern hemisphere.
        Default is to map any such poles to their antipodes in the northern
        hemisphere.
    align_yaxis : bool
        If set to True, then align the oblique with the y-axis.
        Default is to align with the x-axis.
    """

    pole_longitude: float = attr.ib()
    pole_latitude: float = attr.ib()

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{_sth_hem}{central_longitude}/{central_latitude}/{pole_longitude}/{pole_latitude}/{width}{unit}{_align_y}",
    )

    def __attrs_post_init__(self):
        """
        For frozen instances, we have to set using the traditonal way
        using object.__setattr__(self, key, value).
        """
        if self.allow_southern_hemisphere:
            object.__setattr__(self, "_sth_hem", "C")

        if self.align_yaxis:
            object.__setattr__(self, "_align_y", "+v")


@attr.s(frozen=True)
class TransverseMercator(_CylindricalRequired):
    """
    Class definition for the Transverse Mercator projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    central_latitude: float = attr.ib(default=None)

    _code: str = attr.ib(init=False, repr=False, default="T")
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{central_longitude}/{_lat0}{width}{unit}",
    )
    _lat0: str = attr.ib(init=False, repr=False, default="")

    def __attrs_post_init__(self):
        """
        The transverse mercator has the central meridan as an optional.
        """
        if self.central_latitude:
            object.__setattr__(self, "_lat0", f"{self.central_latitude}/")


@attr.s(frozen=True, kw_only=True)
class UniversalTransverseMercator(_Projection):
    """
    Class definition for the Universal Transverse Mercator projection.

    Parameters
    ----------
    zone : str
        The UTM zone {A, B, Y, Z, 1-60}. Use negative values for numerical
        zones in the southern hemisphere, or append the latitude modifiers
        {C-N, P-X} to specify and exact UTM grid zone.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    zone: str = attr.ib()
    width: float = attr.ib()
    unit: str = attr.ib(default="c")

    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{zone}/{width}{unit}",
    )
    _code: str = attr.ib(init=False, repr=False, default="U")


@attr.s(frozen=True)
class EquidistantCylindrical(_CylindricalOptionals):
    """
    Class definition for the equidistant cylindrical projection.

    Parameters
    ----------
    central_longitude : float
        The longitude of the projection centre.
    central_latitude : float
        The latitude of the projection centre.
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    """

    _code: str = attr.ib(init=False, repr=False, default="Q")


@attr.s(frozen=True, kw_only=True)
class Polar(_Projection):
    """
    Class definition for the Polar projection (theta, radial or r).

    Parameters
    ----------
    width : float
        The figure width.
    unit : str
        The unit for the figure width in ``i`` for inch, ``c`` for centimetre.
        Default is ``c``.
    clockwise : bool
        Set to True for azimuths clockwise from North instead of
        counter clockwise from East (default).
    flip : bool
        Set to True to flip the radial direction to point inwards.
    flip_options : str | int | float
        The string ``e`` indicates that ``r`` represents elevations in degrees.
        The string ``p`` will select current planetary radius as maximum radius north.
        A numerical value can be used to specify a custom radius.
    origin : float
        Origin in degrees so the angular value is aligned with the
        positive x-axis (or the azimuth to be aligned with the positive
        y-axis if theta is clockwise from north).
        Angular offset in degrees. Default is 0 (no offset).
    offset : float
        Radial offset to include in measurement units. Default is 0 (no offset).
    depth : bool
        To annotate depth rather than radius. Alternatively, if your ``r`` data
        are actually depths, then you ca
    depth_options : str | int | float
        The string ``p`` indicates that your data are actually depths.
        A numerical value ti get radial annotations ``r = radius - z`` instead.
    """

    clockwise: bool = attr.ib(default=False)
    flip: bool = attr.ib(default=False)
    flip_options = attr.ib(default="")
    width: float = attr.ib()
    unit: str = attr.ib(default="c")
    origin: float = attr.ib(default=0)
    offset: float = attr.ib(default=0)
    depth: bool = attr.ib(default=False)
    depth_options = attr.ib(default=False)

    _code: str = attr.ib(init=False, repr=False, default="P")
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{width}{unit}{_clockwise}{_flip}{_offset}{_origin}{_depth}",
    )

    # the polar projection has a more complicated/specific setup with mixed type
    # options. So private fields were necessary to do the post conversions.
    _clockwise: str = attr.ib(init=False, repr=False, default="")
    _flip: str = attr.ib(init=False, repr=False, default="")
    _offset: str = attr.ib(init=False, repr=False, default="")
    _origin: str = attr.ib(init=False, repr=False, default="")
    _depth: str = attr.ib(init=False, repr=False, default="")

    @flip_options.validator
    def check_flip_options(self, attribute, value):
        """
        Validate the options that are passed through the flip_options field.
        """
        msg = "flip_options must be 'e', 'p' or a number specifying the radius"
        if isinstance(value, str):
            if value not in ["e", "p", ""]:
                raise ValueError(msg)
        elif not isinstance(value, numbers.Number):
            raise ValueError(msg)

    @depth_options.validator
    def check_depth_options(self, attribute, value):
        """
        Validate the options that are passed through the depth_options field.
        """
        msg = "depth_options must be 'p' or a number specifying the radius"
        if isinstance(value, str):
            if value != "p":
                raise ValueError(msg)
        elif not isinstance(value, numbers.Number):
            raise ValueError(msg)

    def __attrs_post_init__(self):
        """
        For frozen instances, we have to set using the traditonal way
        using object.__setattr__(self, key, value).
        """
        if self.clockwise:
            object.__setattr__(self, "_clockwise", "+a")

        if self.offset:
            object.__setattr__(self, "_offset", f"+r{self.offset}")

        if self.origin:
            object.__setattr__(self, "_origin", f"+t{self.origin}")

        # flip and depth have an options field
        # two options if the user has provided options without depth=True;
        # 1. override user input with an empty str,
        # 2. raise an exception if the associated bool is not set to True

        if self.flip:
            flip_str = "+f"

            if self.flip_options:
                flip_str += f"{self.flip_options}"

            object.__setattr__(self, "_flip", flip_str)
        else:
            object.__setattr__(self, "_flip", "")  # override

        if self.depth:
            depth_str = "+z"

            if self.depth_options:
                depth_str += f"{self.depth_options}"

            object.__setattr__(self, "_depth", depth_str)
        else:
            object.__setattr__(self, "_depth", "")  # override


def _time_check(self, attribute, value):
    """
    Validate the time field for the linear projection.
    """
    msg = "time must be 't' or 'T' (relative to TIME_EPOCH or absolute time)."
    if isinstance(value, str):
        if value not in ["t", "T", ""]:  # empty str caters for default value
            raise ValueError(msg)
    else:
        raise ValueError(msg)


@attr.s(frozen=True, kw_only=True)
class Linear(_Projection):
    """
    Class definition for the linear coordinate transformations.

    Caters for regular floating point coordinates, geographic coordinates
    and calendar time coordinates.
    Additional scaling transformations include logarithmic and power.
    """

    width: float = attr.ib()
    height: float = attr.ib(default=False)
    unit: str = attr.ib(default="c")
    geographic: bool = attr.ib(default=False)
    log_x: bool = attr.ib(default=False)
    log_y: bool = attr.ib(default=False)
    power_x: float = attr.ib(default=False)
    power_y: float = attr.ib(default=False)
    time_x: str = attr.ib(default="", validator=_time_check)
    time_y: str = attr.ib(default="", validator=_time_check)

    _code: str = attr.ib(init=False, repr=False, default="X")
    _fmt: str = attr.ib(
        init=False,
        repr=False,
        default="{_code}{width}{unit}{_logx}{_powx}{_timex}{_height}{_logy}{_powy}{_timey}{_geog}",
    )

    # these private fields act as an alias for the main fields so the proj str
    # can be be generated from the aliases rather than the
    # original fields due to the handling complexity of this proj type
    _height: str = attr.ib(init=False, repr=False, default="")
    _timex: str = attr.ib(init=False, repr=False, default="")
    _timey: str = attr.ib(init=False, repr=False, default="")
    _powx: str = attr.ib(init=False, repr=False, default="")
    _powy: str = attr.ib(init=False, repr=False, default="")
    _logx: str = attr.ib(init=False, repr=False, default="")
    _logy: str = attr.ib(init=False, repr=False, default="")
    _geog: str = attr.ib(init=False, repr=False, default="")

    def __attrs_post_init__(self):
        """
        The linear projection has a lot of options that require more control
        and checking after initialisation.
        """
        if self.height:
            object.__setattr__(self, "_height", f"/{self.height}{self.unit}")

        # docs mention d | g, but the examples showed no difference
        if self.geographic:
            object.__setattr__(self, "_geog", "d")

        # docs indicate mutual exclusivity for log, power, time for both
        # x & y sections
        # -JXwidth[l|pexp|T|t][/height[l|pexp|T|t]][d]
        if any(
            [
                self.log_x and self.power_x,
                self.log_x and self.time_x,
                self.power_x and self.time_x,
            ]
        ):
            msg = "log_x, power_x and time_x are mutually exclusive"
            raise ValueError(msg)

        if any(
            [
                self.log_y and self.power_y,
                self.log_y and self.time_y,
                self.power_y and self.time_y,
            ]
        ):
            msg = "log_y, power_y and time_y are mutually exclusive"
            raise ValueError(msg)

        if self.log_y and not self.height:
            msg = "height must be defined when applying log scaling"
            raise ValueError(msg)

        if self.power_y and not self.height:
            msg = "height must be defined when applying power scaling"
            raise ValueError(msg)

        # Linear proj has a slightly more complicated str format to control;
        if self.log_x:
            object.__setattr__(self, "_logx", "l")

        if self.log_y:
            object.__setattr__(self, "_logy", "l")

        if self.time_x:
            object.__setattr__(self, "_timex", self.time_x)

        if self.time_y:
            object.__setattr__(self, "_timey", self.time_y)

        if self.power_x:
            object.__setattr__(self, "_powx", f"p{self.power_x}")

        if self.power_y:
            object.__setattr__(self, "_powy", f"p{self.power_y}")
