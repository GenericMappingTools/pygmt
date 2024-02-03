"""
Functions for downloading remote data files to cache.
"""
from pygmt.src import which


def cache_data():
    """
    Download GMT remote data files used in PyGMT tests and docs to cache folder.
    """
    # List of datasets to download
    datasets = [
        # Earth relief grids
        "@earth_gebco_01d_g",
        "@earth_gebcosi_01d_g",
        "@earth_gebcosi_15m_p",
        "@earth_relief_01d_p",
        "@earth_relief_01d_g",
        "@earth_relief_30m_p",
        "@earth_relief_30m_g",
        "@earth_relief_10m_p",
        "@earth_relief_10m_g",
        "@earth_relief_05m_p",
        "@earth_relief_05m_g",
        "@earth_synbath_01d_g",
        # List of tiles of 03s srtm data.
        # Names like @N35E135.earth_relief_03s_g.nc are for internal use only.
        # The naming scheme may change. DO NOT USE IT IN YOUR SCRIPTS.
        "@N30W120.earth_relief_15s_p.nc",
        "@N35E135.earth_relief_03s_g.nc",
        "@N37W120.earth_relief_03s_g.nc",
        "@N00W090.earth_relief_03m_p.nc",
        "@N00E135.earth_relief_30s_g.nc",
        "@N00W010.earth_relief_15s_p.nc",  # Specific grid for 15s test
        "@N04W010.earth_relief_03s_g.nc",  # Specific grid for 03s test
        # Earth synbath relief grid
        "@S15W105.earth_synbath_30s_p.nc",
        # Earth seafloor age grids
        "@earth_age_01d_g",
        "@N00W030.earth_age_01m_g.nc",  # Specific grid for 01m test
        # Earth geoid grids
        "@earth_geoid_01d_g",
        "@N00W030.earth_geoid_01m_g.nc",  # Specific grid for 01m test
        # Earth magnetic anomaly grids
        "@earth_mag_01d_g",
        "@S30W060.earth_mag_02m_p.nc",  # Specific grid for 02m test
        "@earth_mag4km_01d_g",
        "@S30W120.earth_mag4km_02m_p.nc",  # Specific grid for 02m test
        # Earth mask grid
        "@earth_mask_01d_g",
        # Earth free-air anomaly grids
        "@earth_faa_01d_g",
        "@N00W030.earth_faa_01m_p.nc",  # Specific grid for 01m test
        # Earth vertical gravity gradient grids
        "@earth_vgg_01d_g",
        "@N00W030.earth_vgg_01m_p.nc",  # Specific grid for 01m test
        # Earth WDMAM grids
        "@earth_wdmam_01d_g",
        "@S90E000.earth_wdmam_03m_g.nc",  # Specific grid for 03m test
        # Earth day/night images
        "@earth_day_01d_p",
        # Mars relief grids
        "@mars_relief_01d_g",
        "@N00W030.mars_relief_01m_g.nc",  # Specific grid for 01m tes
        # Mercury relief grids
        "@mercury_relief_01d_g",
        "@N00W030.mercury_relief_01m_p.nc",  # Specific grid for 01m test
        # Moon relief grids
        "@moon_relief_01d_g",
        "@N00W030.moon_relief_01m_p.nc",  # Specific grid for 01m test
        # Pluto relief grids
        "@pluto_relief_01d_g",
        "@N00W030.pluto_relief_01m_p.nc",  # Specific grid for 01m test
        # Venus relief grids
        "@venus_relief_01d_g",
        "@N00W030.venus_relief_01m_g.nc",  # Specific grid for 01m test
        # Other cache files
        "@capitals.gmt",
        "@circuit.png",
        "@earth_relief_20m_holes.grd",
        "@EGM96_to_36.txt",
        "@MaunaLoa_CO2.txt",
        "@RidgeTest.shp",
        "@RidgeTest.shx",
        "@RidgeTest.dbf",
        "@RidgeTest.prj",
        "@Table_5_11.txt",
        "@Table_5_11_mean.xyz",
        "@fractures_06.txt",
        "@hotspots.txt",
        "@ridge.txt",
        "@mars370d.txt",
        "@srtm_tiles.nc",  # needed for 03s and 01s relief data
        "@static_earth_relief.nc",
        "@ternary.txt",
        "@test.dat.nc",
        "@tut_bathy.nc",
        "@tut_quakes.ngdc",
        "@tut_ship.xyz",
        "@usgs_quakes_22.txt",
    ]
    which(fname=datasets, download="a")
