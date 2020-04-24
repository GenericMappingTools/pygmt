Changelog
=========

Release v0.1.0
--------------

*Released on: 2020/04/XX*

Highlights:

* 🎉 **First official release of PyGMT** 🎉  
* Python 3.8 is now supported (#398)
* PyGMT now uses the stable version of GMT 6.0.0 by default (#363)
* Use sphinx-gallery to manage examples and tutorials (#268)

New features:

* Wrap blockmedian (#349)
* Add pygmt.config() to change gmt defaults locally and globally (#293)
* Wrap grdview (#330)
* Wrap grdtrack (#308)
* Wrap colorbar (#332)
* Wrap text (#321)
* Wrap legend (#333)
* Wrap makecpt (#329)
* Add a new method to shift plot origins (#289)

Enhancements:

* Allow text accepting "frame" as an argument (#385)
* Allow for grids with negative lat/lon increments (#369)
* Allow passing in list to 'region' argument in surface (#378)
* Allow passing in scalar number to x and y in plot (#376)
* Implement default position/box for legend (#359)
* Add sequence_space converter in kwargs_to_string (#325)

Documentation:

* Update PyPI install instructions and API disclaimer message (#421)
* Fix the link to GMT documentation (#419)
* Use napoleon instead of numpydoc with sphinx (#383)
* Document using a list for repeated arguments (#361)
* Add legend gallery entry (#358)
* Update instructions to set GMT_LIBRARY_PATH (#324)
* Fix the link to the GMT homepage (#331)
* Split projections gallery by projection types (#318)
* Fix the link to GMT/Matlab API in the README (#297)
* Use shinx extlinks for linking GMT docs (#294)
* Comment about country code in projection examples (#290)
* Add an overview page listing presentations (#286)

Bug Fixes:

* Let surface return xr.DataArray instead of xr.Dataset (#408)
* Update GMT constant GMT_STR16 to GMT_VF_LEN for GMT API change in 6.1.0 (#397)
* Properly trigger pytest matplotlib image comparison (#352)
* Use uuid.uuid4 to generate unique names (#274)

Maintenance:

* Quickfix Zeit Now miniconda installer link to anaconda.com (#413)
* Fix Github Pages deployment from Travis (#410)
* Update and clean TravisCI configuration (#404)
* Quickfix min elevation for new SRTM15+V2.1 earth relief grids (#401)
* Wrap docstrings to 79 chars and check with flake8 (#384)
* Update continuous integration scripts to 1.2.0 (#355)
* Use Zeit Now to deploy doc builds from PRs (#344)
* Move gmt from requirements.txt to CI scripts instead (#343)
* Change py.test to pytest (#338)
* Add Google Analytics to measure site visitors (#314)
* Register mpl_image_compare marker to remove PytestUnknownMarkWarning (#323)
* Disable Windows CI builds before PR #313 is merged (#320)
* Enable Mac and Windows CI on Azure Pipelines (#312)
* Fixes for using GMT 6.0.0rc1 (#311)
* Assign authorship to "The PyGMT Developers" (#284)

Deprecations:

* Remove mention of gitter.im (#405)
* Remove portrait (-P) from common options (#339)
* Remove require.js since WorldWind was dropped (#278)
* Remove Web WorldWind support (#275)

This release contains contributions from:

* Dongdong Tian
* Wei Ji Leong
* Leonardo Uieda
* Liam Toney
* Brook Tozer
* Claudio Satriano
* Cody Woodson
* Mark Wieczorek
* Philipp Loose
* Kathryn Materna
