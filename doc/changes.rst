Changelog
=========

Release v0.2.1 (2020/11/14)
---------------------------

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4253459.svg
   :alt: Digital Object Identifier for the Zenodo archive
   :target: https://doi.org/10.5281/zenodo.4253459

Highlights

* 🎉 **Patch release with more tutorials and gallery examples!** 🎉
* 🐍 Support Python 3.9 (`#689 <https://github.com/GenericMappingTools/pygmt/pull/689>`__)
* 📹 Add `Liam <https://github.com/liamtoney>`__'s `ROSES 2020 PyGMT talk <https://www.youtube.com/watch?v=SSIGJEe0BIk>`__ (`#643 <https://github.com/GenericMappingTools/pygmt/pull/643>`__)

New Features

* Wrap plot3d (`#471 <https://github.com/GenericMappingTools/pygmt/pull/471>`__)
* Wrap grdfilter (`#616 <https://github.com/GenericMappingTools/pygmt/pull/616>`__)

Enhancements

* Allow np.object dtypes into virtualfile_from_vectors (`#684 <https://github.com/GenericMappingTools/pygmt/pull/684>`__)
* Let plot() accept record-by-record transparency (`#626 <https://github.com/GenericMappingTools/pygmt/pull/626>`__)
* Refactor info to allow datetime inputs from xarray.Dataset and pandas.DataFrame tables (`#619 <https://github.com/GenericMappingTools/pygmt/pull/619>`__)

Tutorials & Gallery

* Add tutorial for pygmt.config (`#482 <https://github.com/GenericMappingTools/pygmt/pull/482>`__)
* Add an example for different line styles (`#604 <https://github.com/GenericMappingTools/pygmt/pull/604>`__, `#664 <https://github.com/GenericMappingTools/pygmt/pull/664>`__)
* Add a gallery example for varying transparent points (`#654 <https://github.com/GenericMappingTools/pygmt/pull/654>`__)
* Add tutorial for pygmt.Figure.text (`#480 <https://github.com/GenericMappingTools/pygmt/pull/480>`__)
* Add an example for scatter plots with auto legends (`#607 <https://github.com/GenericMappingTools/pygmt/pull/607>`__)
* Improve colorbar gallery example (`#596 <https://github.com/GenericMappingTools/pygmt/pull/596>`__)

Documentation Improvements

* doc: Fix the description of grdcontour -G option (`#681 <https://github.com/GenericMappingTools/pygmt/pull/681>`__)
* Refresh Code of Conduct from v1.4 to v2.0 (`#673 <https://github.com/GenericMappingTools/pygmt/pull/673>`__)
* Add PyGMT Zenodo BibTeX entry to main README.md (`#678 <https://github.com/GenericMappingTools/pygmt/pull/678>`__)
* Complete most of documentation for makecpt (`#676 <https://github.com/GenericMappingTools/pygmt/pull/676>`__)
* Complete documentation for plot (`#666 <https://github.com/GenericMappingTools/pygmt/pull/666>`__)
* Add "no_clip" to plot, text, contour and meca (`#661 <https://github.com/GenericMappingTools/pygmt/pull/661>`__)
* Add common alias "verbose" (V) to all functions (`#662 <https://github.com/GenericMappingTools/pygmt/pull/662>`__)
* Improve documentation of Figure.logo() (`#651 <https://github.com/GenericMappingTools/pygmt/pull/651>`__)
* Add mini-galleries for methods and functions (`#648 <https://github.com/GenericMappingTools/pygmt/pull/648>`__)
* Complete documentation of grdimage (`#620 <https://github.com/GenericMappingTools/pygmt/pull/620>`__)
* Add common alias perspective (p) for plotting 3D illustrations (`#627 <https://github.com/GenericMappingTools/pygmt/pull/627>`__)
* Add common aliases xshift (X) and yshift (Y) (`#624 <https://github.com/GenericMappingTools/pygmt/pull/624>`__)
* Add common alias cores (x) for grdimage and other multi-threaded modules (`#625 <https://github.com/GenericMappingTools/pygmt/pull/625>`__)
* Enable switching different versions of documentation (`#621 <https://github.com/GenericMappingTools/pygmt/pull/621>`__)
* Add common alias transparency (-t) to all plotting functions (`#614 <https://github.com/GenericMappingTools/pygmt/pull/614>`__)

Bug Fixes

* Disallow passing arguments like -XNone to GMT (`#639 <https://github.com/GenericMappingTools/pygmt/pull/639>`__)

Maintenance

* Migrate PyPI release to GitHub Actions (`#679 <https://github.com/GenericMappingTools/pygmt/pull/679>`__)
* Upload artifacts showing diff images on test failure (`#675 <https://github.com/GenericMappingTools/pygmt/pull/675>`__)
* Add slash command "/format" to automatically format PRs (`#646 <https://github.com/GenericMappingTools/pygmt/pull/646>`__)
* Add instructions to run specific tests (`#660 <https://github.com/GenericMappingTools/pygmt/pull/660>`__)
* Add more tests for xarray grid shading (`#650 <https://github.com/GenericMappingTools/pygmt/pull/650>`__)
* Refactor xfail tests to avoid storing baseline images (`#603 <https://github.com/GenericMappingTools/pygmt/pull/603>`__)
* Add blackdoc to format Python codes in docstrings (`#641 <https://github.com/GenericMappingTools/pygmt/pull/641>`__)
* Check and lint sphinx configuration file doc/conf.py (`#630 <https://github.com/GenericMappingTools/pygmt/pull/630>`__)
* Improve Makefile to clean ``__pycache__`` directory recursively (`#611 <https://github.com/GenericMappingTools/pygmt/pull/611>`__)
* Update release process and checklist template (`#602 <https://github.com/GenericMappingTools/pygmt/pull/602>`__)

This release contains contributions from:

* `Dongdong Tian <https://github.com/seisman>`__
* `Wei Ji Leong <https://github.com/weiji14>`__
* `Conor Bacon <https://github.com/hemmelig>`__
* `carocamargo <https://github.com/carocamargo>`__

Release v0.2.0 (2020/09/12)
---------------------------

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4025418.svg
   :alt: Digital Object Identifier for the Zenodo archive
   :target: https://doi.org/10.5281/zenodo.4025418

Highlights:

* 🎉 **Second minor release of PyGMT** 🎉
* Minimum required GMT version is now 6.1.1 or newer (`#577 <https://github.com/GenericMappingTools/pygmt/pull/577>`__)
* Plotting xarray grids using grdimage and grdview should not crash anymore and works for most cases (`#560 <https://github.com/GenericMappingTools/pygmt/pull/560>`__)
* Easier time-series plots with support for datetime-like inputs to plot (`#464 <https://github.com/GenericMappingTools/pygmt/pull/464>`__) and the region argument (`#562 <https://github.com/GenericMappingTools/pygmt/pull/562>`__)

New Features:

* Wrap GMT_Put_Strings to pass str columns into GMT C API directly (`#520 <https://github.com/GenericMappingTools/pygmt/pull/520>`__)
* Wrap meca (`#516 <https://github.com/GenericMappingTools/pygmt/pull/516>`__)
* Wrap x2sys_init and x2sys_cross (`#546 <https://github.com/GenericMappingTools/pygmt/pull/546>`__)
* Let grdcut() accept xarray.DataArray as input (`#541 <https://github.com/GenericMappingTools/pygmt/pull/541>`__)
* Initialize a GMTDataArrayAccessor (`#500 <https://github.com/GenericMappingTools/pygmt/pull/500>`__)

Enhancements:

* Allow passing in pandas dataframes to x2sys_cross (`#591 <https://github.com/GenericMappingTools/pygmt/pull/591>`__)
* Sensible array outputs for pygmt info (`#575 <https://github.com/GenericMappingTools/pygmt/pull/575>`__)
* Allow pandas.DataFrame table and 1D/2D numpy array inputs into pygmt.info (`#574 <https://github.com/GenericMappingTools/pygmt/pull/574>`__)
* Add auto-legend feature to grdcontour and contour (`#568 <https://github.com/GenericMappingTools/pygmt/pull/568>`__)
* Add common alias verbose (V) (`#550 <https://github.com/GenericMappingTools/pygmt/pull/550>`__)
* Let load_earth_relief() support all resolutions and optional subregion (`#542 <https://github.com/GenericMappingTools/pygmt/pull/542>`__)
* Allow load_earth_relief() to load pixel or gridline registered data (`#509 <https://github.com/GenericMappingTools/pygmt/pull/509>`__)

Documentation:

* Link to try-gmt binder repository (`#598 <https://github.com/GenericMappingTools/pygmt/pull/598>`__)
* Improve docstring of data_kind() to include xarray grid (`#588 <https://github.com/GenericMappingTools/pygmt/pull/588>`__)
* Improve the documentation of Figure.shift_origin() (`#536 <https://github.com/GenericMappingTools/pygmt/pull/536>`__)
* Add shading to grdview gallery example (`#506 <https://github.com/GenericMappingTools/pygmt/pull/506>`__)

Bug Fixes:

* Ensure surface and grdcut loads GMTDataArray accessor info into xarray (`#539 <https://github.com/GenericMappingTools/pygmt/pull/539>`__)
* Raise an error if short- and long-form arguments coexist (`#537 <https://github.com/GenericMappingTools/pygmt/pull/537>`__)
* Fix the grdtrack example to avoid crashes on macOS (`#531 <https://github.com/GenericMappingTools/pygmt/pull/531>`__)
* Properly allow for either pixel or gridline registered grids (`#476 <https://github.com/GenericMappingTools/pygmt/pull/476>`__)

Maintenance:

* Add a test for xarray shading (`#581 <https://github.com/GenericMappingTools/pygmt/pull/581>`__)
* Remove expected failures on grdview tests (`#589 <https://github.com/GenericMappingTools/pygmt/pull/589>`__)
* Redesign check_figures_equal testing function to be more explicit (`#590 <https://github.com/GenericMappingTools/pygmt/pull/590>`__)
* Cut Windows CI build time in half to 15 min (`#586 <https://github.com/GenericMappingTools/pygmt/pull/586>`__)
* Add a test for Session.write_data() writing netCDF grids (`#583 <https://github.com/GenericMappingTools/pygmt/pull/583>`__)
* Add a test to make sure shift_origin does not crash (`#580 <https://github.com/GenericMappingTools/pygmt/pull/580>`__)
* Add testing.check_figures_equal to avoid storing baseline images (`#555 <https://github.com/GenericMappingTools/pygmt/pull/555>`__)
* Eliminate unnecessary jobs from Travis CI (`#567 <https://github.com/GenericMappingTools/pygmt/pull/567>`__) and Azure Pipelines (`#513 <https://github.com/GenericMappingTools/pygmt/pull/513>`__)
* Improve the workflow to test both GMT master (`#485 <https://github.com/GenericMappingTools/pygmt/pull/485>`__) and 6.1 branches (`#554 <https://github.com/GenericMappingTools/pygmt/pull/554>`__)
* Automatically cancel in-progress CI runs of old commits (`#544 <https://github.com/GenericMappingTools/pygmt/pull/544>`__)
* Remove the Stickler CI configuration file (`#538 <https://github.com/GenericMappingTools/pygmt/pull/538>`__), run style checks using GitHub Actions (`#519 <https://github.com/GenericMappingTools/pygmt/pull/519>`__)
* Cache GMT remote data as artifacts on GitHub (`#530 <https://github.com/GenericMappingTools/pygmt/pull/530>`__)
* Let pytest generate both HTML and XML coverage reports (`#512 <https://github.com/GenericMappingTools/pygmt/pull/512>`__)
* Run Continuous Integration tests on GitHub Actions (`#475 <https://github.com/GenericMappingTools/pygmt/pull/475>`__)

Contributors:

* `Dongdong Tian <https://github.com/seisman>`__
* `Wei Ji Leong <https://github.com/weiji14>`__
* `Tyler Newton <https://github.com/tjnewton>`__
* `Liam Toney <https://github.com/liamtoney>`__

----

Release v0.1.2 (2020/07/07)
---------------------------

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3930577.svg
   :alt: Digital Object Identifier for the Zenodo archive
   :target: https://doi.org/10.5281/zenodo.3930577

Highlights:

* Patch release in preparation for the SciPy 2020 sprint session
* Last version to support GMT 6.0, future PyGMT versions will require GMT 6.1 or newer

New Features:

* Wrap grdcut (`#492 <https://github.com/GenericMappingTools/pygmt/pull/492>`__)
* Add show_versions() function for printing debugging information used in issue reports (`#466 <https://github.com/GenericMappingTools/pygmt/pull/466>`__)

Enhancements:

* Change load_earth_relief()'s default resolution to 01d (`#488 <https://github.com/GenericMappingTools/pygmt/pull/488>`__)
* Enhance text with extra functionality and aliases (`#481 <https://github.com/GenericMappingTools/pygmt/pull/481>`__)

Documentation:

* Add gallery example for grdview (`#502 <https://github.com/GenericMappingTools/pygmt/pull/502>`__)
* Turn all short aliases into long form (`#474 <https://github.com/GenericMappingTools/pygmt/pull/474>`__)
* Update the plotting example using the colormap generated by pygmt.makecpt (`#472 <https://github.com/GenericMappingTools/pygmt/pull/472>`__)
* Add instructions to view the test coverage reports locally (`#468 <https://github.com/GenericMappingTools/pygmt/pull/468>`__)
* Update the instructions for testing pygmt install (`#459 <https://github.com/GenericMappingTools/pygmt/pull/459>`__)

Bug Fixes:

* Fix a bug when passing data to GMT in Session.open_virtual_file() (`#490 <https://github.com/GenericMappingTools/pygmt/pull/490>`__)

Maintenance:

* Temporarily expect failures for some grdcontour and grdview tests (`#503 <https://github.com/GenericMappingTools/pygmt/pull/503>`__)
* Fix several failures due to updates of earth relief data (`#498 <https://github.com/GenericMappingTools/pygmt/pull/498>`__)
* Unpin pylint version and fix some lint warnings (`#484 <https://github.com/GenericMappingTools/pygmt/pull/484>`__)
* Separate tests of gmtinfo and grdinfo (`#461 <https://github.com/GenericMappingTools/pygmt/pull/461>`__)
* Fix the test for GMT_COMPATIBILITY=6 (`#454 <https://github.com/GenericMappingTools/pygmt/pull/454>`__)
* Update baseline images for updates of earth relief data (`#452 <https://github.com/GenericMappingTools/pygmt/pull/452>`__)
* Simplify PyGMT Release process (`#446 <https://github.com/GenericMappingTools/pygmt/pull/446>`__)

Contributors:

* `Dongdong Tian <https://github.com/seisman>`__
* `Wei Ji Leong <https://github.com/weiji14>`__
* `Liam Toney <https://github.com/liamtoney>`__

----

Release v0.1.1 (2020/05/22)
---------------------------

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3837197.svg
   :alt: Digital Object Identifier for the Zenodo archive
   :target: https://doi.org/10.5281/zenodo.3837197

Highlights:

* 🏁Windows users rejoice, this bugfix release is for you!🏁
* Let PyGMT work with the conda GMT package on Windows (`#434 <https://github.com/GenericMappingTools/pygmt/pull/434>`__)

Enhancements:

* Handle setting special parameters without default settings for config (`#411 <https://github.com/GenericMappingTools/pygmt/pull/411>`__)

Documentation:

* Update install instructions (`#430 <https://github.com/GenericMappingTools/pygmt/pull/430>`__)
* Add PyGMT AGU 2019 poster to website (`#425 <https://github.com/GenericMappingTools/pygmt/pull/425>`__)
* Redirect www.pygmt.org to latest, instead of dev (`#423 <https://github.com/GenericMappingTools/pygmt/pull/423>`__)

Bug Fixes:

* Set GMT_COMPATIBILITY to 6 when pygmt session starts (`#432 <https://github.com/GenericMappingTools/pygmt/pull/432>`__)
* Improve how PyGMT finds the GMT library (`#440 <https://github.com/GenericMappingTools/pygmt/pull/440>`__)

Maintenance:

* Finalize fixes on Windows test suite for v0.1.1 (`#441 <https://github.com/GenericMappingTools/pygmt/pull/441>`__)
* Cache test data on Azure Pipelines (`#438 <https://github.com/GenericMappingTools/pygmt/pull/438>`__)

This release contains contributions from:

* `Dongdong Tian <https://github.com/seisman>`__
* `Wei Ji Leong <https://github.com/weiji14>`__
* `Jason K. Moore <https://github.com/moorepants>`__

----

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
* Fix GitHub Pages deployment from Travis (`#410 <https://github.com/GenericMappingTools/pygmt/pull/410>`__)
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
