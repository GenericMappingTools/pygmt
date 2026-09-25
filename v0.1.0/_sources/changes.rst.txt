Changelog
=========

Release v0.1.0 (2020/05/03)
---------------------------

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3782862.svg
   :alt: Digital Object Identifier for the Zenodo archive
   :target: https://doi.org/10.5281/zenodo.3782862

Highlights:

* 🎉 **First official release of PyGMT** 🎉
* Python 3.8 is now supported (`#398 <https://github.com/GenericMappingTools/pygmt/pull/398>`__)
* PyGMT now uses the stable version of GMT 6.0.0 by default (`#363 <https://github.com/GenericMappingTools/pygmt/pull/363>`__)
* Use sphinx-gallery to manage examples and tutorials (`#268 <https://github.com/GenericMappingTools/pygmt/pull/268>`__)

New features:

* Wrap blockmedian (`#349 <https://github.com/GenericMappingTools/pygmt/pull/349>`__)
* Add pygmt.config() to change gmt defaults locally and globally (`#293 <https://github.com/GenericMappingTools/pygmt/pull/293>`__)
* Wrap grdview (`#330 <https://github.com/GenericMappingTools/pygmt/pull/330>`__)
* Wrap grdtrack (`#308 <https://github.com/GenericMappingTools/pygmt/pull/308>`__)
* Wrap colorbar (`#332 <https://github.com/GenericMappingTools/pygmt/pull/332>`__)
* Wrap text (`#321 <https://github.com/GenericMappingTools/pygmt/pull/321>`__)
* Wrap legend (`#333 <https://github.com/GenericMappingTools/pygmt/pull/333>`__)
* Wrap makecpt (`#329 <https://github.com/GenericMappingTools/pygmt/pull/329>`__)
* Add a new method to shift plot origins (`#289 <https://github.com/GenericMappingTools/pygmt/pull/289>`__)

Enhancements:

* Allow text accepting "frame" as an argument (`#385 <https://github.com/GenericMappingTools/pygmt/pull/385>`__)
* Allow for grids with negative lat/lon increments (`#369 <https://github.com/GenericMappingTools/pygmt/pull/369>`__)
* Allow passing in list to 'region' argument in surface (`#378 <https://github.com/GenericMappingTools/pygmt/pull/378>`__)
* Allow passing in scalar number to x and y in plot (`#376 <https://github.com/GenericMappingTools/pygmt/pull/376>`__)
* Implement default position/box for legend (`#359 <https://github.com/GenericMappingTools/pygmt/pull/359>`__)
* Add sequence_space converter in kwargs_to_string (`#325 <https://github.com/GenericMappingTools/pygmt/pull/325>`__)

Documentation:

* Update PyPI install instructions and API disclaimer message (`#421 <https://github.com/GenericMappingTools/pygmt/pull/421>`__)
* Fix the link to GMT documentation (`#419 <https://github.com/GenericMappingTools/pygmt/pull/419>`__)
* Use napoleon instead of numpydoc with sphinx (`#383 <https://github.com/GenericMappingTools/pygmt/pull/383>`__)
* Document using a list for repeated arguments (`#361 <https://github.com/GenericMappingTools/pygmt/pull/361>`__)
* Add legend gallery entry (`#358 <https://github.com/GenericMappingTools/pygmt/pull/358>`__)
* Update instructions to set GMT_LIBRARY_PATH (`#324 <https://github.com/GenericMappingTools/pygmt/pull/324>`__)
* Fix the link to the GMT homepage (`#331 <https://github.com/GenericMappingTools/pygmt/pull/331>`__)
* Split projections gallery by projection types (`#318 <https://github.com/GenericMappingTools/pygmt/pull/318>`__)
* Fix the link to GMT/Matlab API in the README (`#297 <https://github.com/GenericMappingTools/pygmt/pull/297>`__)
* Use shinx extlinks for linking GMT docs (`#294 <https://github.com/GenericMappingTools/pygmt/pull/294>`__)
* Comment about country code in projection examples (`#290 <https://github.com/GenericMappingTools/pygmt/pull/290>`__)
* Add an overview page listing presentations (`#286 <https://github.com/GenericMappingTools/pygmt/pull/286>`__)

Bug Fixes:

* Let surface return xr.DataArray instead of xr.Dataset (`#408 <https://github.com/GenericMappingTools/pygmt/pull/408>`__)
* Update GMT constant GMT_STR16 to GMT_VF_LEN for GMT API change in 6.1.0 (`#397 <https://github.com/GenericMappingTools/pygmt/pull/397>`__)
* Properly trigger pytest matplotlib image comparison (`#352 <https://github.com/GenericMappingTools/pygmt/pull/352>`__)
* Use uuid.uuid4 to generate unique names (`#274 <https://github.com/GenericMappingTools/pygmt/pull/274>`__)

Maintenance:

* Quickfix Zeit Now miniconda installer link to anaconda.com (`#413 <https://github.com/GenericMappingTools/pygmt/pull/413>`__)
* Fix Github Pages deployment from Travis (`#410 <https://github.com/GenericMappingTools/pygmt/pull/410>`__)
* Update and clean TravisCI configuration (`#404 <https://github.com/GenericMappingTools/pygmt/pull/404>`__)
* Quickfix min elevation for new SRTM15+V2.1 earth relief grids (`#401 <https://github.com/GenericMappingTools/pygmt/pull/401>`__)
* Wrap docstrings to 79 chars and check with flake8 (`#384 <https://github.com/GenericMappingTools/pygmt/pull/384>`__)
* Update continuous integration scripts to 1.2.0 (`#355 <https://github.com/GenericMappingTools/pygmt/pull/355>`__)
* Use Zeit Now to deploy doc builds from PRs (`#344 <https://github.com/GenericMappingTools/pygmt/pull/344>`__)
* Move gmt from requirements.txt to CI scripts instead (`#343 <https://github.com/GenericMappingTools/pygmt/pull/343>`__)
* Change py.test to pytest (`#338 <https://github.com/GenericMappingTools/pygmt/pull/338>`__)
* Add Google Analytics to measure site visitors (`#314 <https://github.com/GenericMappingTools/pygmt/pull/314>`__)
* Register mpl_image_compare marker to remove PytestUnknownMarkWarning (`#323 <https://github.com/GenericMappingTools/pygmt/pull/323>`__)
* Disable Windows CI builds before PR `#313 <https://github.com/GenericMappingTools/pygmt/pull/313>`__ is merged (`#320 <https://github.com/GenericMappingTools/pygmt/pull/320>`__)
* Enable Mac and Windows CI on Azure Pipelines (`#312 <https://github.com/GenericMappingTools/pygmt/pull/312>`__)
* Fixes for using GMT 6.0.0rc1 (`#311 <https://github.com/GenericMappingTools/pygmt/pull/311>`__)
* Assign authorship to "The PyGMT Developers" (`#284 <https://github.com/GenericMappingTools/pygmt/pull/284>`__)

Deprecations:

* Remove mention of gitter.im (`#405 <https://github.com/GenericMappingTools/pygmt/pull/405>`__)
* Remove portrait (-P) from common options (`#339 <https://github.com/GenericMappingTools/pygmt/pull/339>`__)
* Remove require.js since WorldWind was dropped (`#278 <https://github.com/GenericMappingTools/pygmt/pull/278>`__)
* Remove Web WorldWind support (`#275 <https://github.com/GenericMappingTools/pygmt/pull/275>`__)

This release contains contributions from:

* `Dongdong Tian <https://github.com/seisman>`__
* `Wei Ji Leong <https://github.com/weiji14>`__
* `Leonardo Uieda <https://github.com/leouieda>`__
* `Liam Toney <https://github.com/liamtoney>`__
* `Brook Tozer <https://github.com/btozer>`__
* `Claudio Satriano <https://github.com/claudiodsf>`__
* `Cody Woodson <https://github.com/Dovacody>`__
* `Mark Wieczorek <https://github.com/MarkWieczorek>`__
* `Philipp Loose <https://github.com/phloose>`__
* `Kathryn Materna <https://github.com/kmaterna>`__
