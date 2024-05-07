"""
Functions for downloading remote data files to cache.
"""

from pygmt.src import which


def cache_data():
    """
    Download GMT remote data files used in PyGMT tests and docs to cache folder.
    """
    # List of data files to download.
    datasets = [
        # List of GMT remote datasets.
        "@earth_age_01d_g",
        "@earth_day_01d_p",
        "@earth_faa_01d_g",
        "@earth_gebco_01d_g",
        "@earth_gebcosi_01d_g",
        "@earth_gebcosi_15m_p",
        "@earth_geoid_01d_g",
        "@earth_mag_01d_g",
        "@earth_mag4km_01d_g",
        "@earth_mask_01d_g",
        "@earth_relief_01d_g",
        "@earth_relief_01d_p",
        "@earth_relief_10m_g",
        "@earth_relief_10m_p",
        "@earth_relief_30m_g",
        "@earth_relief_30m_p",
        "@earth_relief_05m_g",
        "@earth_relief_05m_p",
        "@earth_synbath_01d_g",
        "@earth_vgg_01d_g",
        "@earth_wdmam_01d_g",
        "@mars_relief_01d_g",
        "@mercury_relief_01d_g",
        "@moon_relief_01d_g",
        "@pluto_relief_01d_g",
        "@venus_relief_01d_g",
        # List of tiled remote datasets.
        # Names like @N35E135.earth_relief_03s_g.nc are for internal use only.
        # The naming scheme may change. DO NOT USE IT IN YOUR SCRIPTS.
        "@N00W030.earth_age_01m_g.nc",
        "@N30E060.earth_age_01m_g.nc",
        "@N30E090.earth_age_01m_g.nc",
        "@N00W030.earth_faa_01m_p.nc",
        "@N00W030.earth_geoid_01m_g.nc",
        "@S30W060.earth_mag_02m_p.nc",
        "@S30W120.earth_mag4km_02m_p.nc",
        "@N00W090.earth_relief_03m_p.nc",
        "@N00E135.earth_relief_30s_g.nc",
        "@N00W010.earth_relief_15s_p.nc",
        "@N30W120.earth_relief_15s_p.nc",
        "@N04W010.earth_relief_03s_g.nc",
        "@N35E135.earth_relief_03s_g.nc",
        "@N37W120.earth_relief_03s_g.nc",
        "@S15W105.earth_synbath_30s_p.nc",
        "@N00W030.earth_vgg_01m_p.nc",
        "@S90E000.earth_wdmam_03m_g.nc",
        "@N00W030.mars_relief_01m_g.nc",
        "@N00W030.mercury_relief_01m_g.nc",
        "@N00W030.moon_relief_01m_g.nc",
        "@N00W030.pluto_relief_01m_g.nc",
        "@N00W030.venus_relief_01m_g.nc",
        # List of cache files.
        "@EGM96_to_36.txt",
        "@MaunaLoa_CO2.txt",
        "@RidgeTest.dbf",
        "@RidgeTest.prj",
        "@RidgeTest.shp",
        "@RidgeTest.shx",
        "@Table_5_11.txt",
        "@Table_5_11_mean.xyz",
        "@capitals.gmt",
        "@circuit.png",
        "@earth_relief_20m_holes.grd",
        "@fractures_06.txt",
        "@hotspots.txt",
        "@mars370d.txt",
        "@ridge.txt",
        "@srtm_tiles.nc",  # Needed for earth relief 03s and 01s data.
        "@static_earth_relief.nc",
        "@ternary.txt",
        "@test.dat.nc",
        "@tut_bathy.nc",
        "@tut_quakes.ngdc",
        "@tut_ship.xyz",
        "@usgs_quakes_22.txt",
    ]
    which(fname=datasets, download="a")
