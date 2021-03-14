# Changelog

## Release v0.3.1 (2021/03/14)

[![Digital Object Identifier for PyGMT v0.3.1](https://zenodo.org/badge/DOI/10.5281/zenodo.4592991.svg)](https://doi.org/10.5281/zenodo.4592991)

### Highlights

* 🎉 **Multiple bug fixes and a reorganized gallery** 🎉
* A reorganization of the gallery examples ([#995](https://github.com/GenericMappingTools/pygmt/pull/995))
* New gallery examples of plotting vectors ([#950](https://github.com/GenericMappingTools/pygmt/pull/950) and [#890](https://github.com/GenericMappingTools/pygmt/pull/890))
* This is the last PyGMT version to support GMT 6.1.1; the next release will require GMT 6.2

### Enhancements

* Support passing a sequence to the spacing parameter of pygmt.info() ([#1031](https://github.com/GenericMappingTools/pygmt/pull/1031))

### Bug Fixes

* Fix issues in loading GMT's shared library ([#977](https://github.com/GenericMappingTools/pygmt/pull/977))
* Let pygmt.info load datetime columns into a str dtype array ([#960](https://github.com/GenericMappingTools/pygmt/pull/960))
* Check invalid combinations of resolution and registration in load_earth_relief() ([#965](https://github.com/GenericMappingTools/pygmt/pull/965))
* Open figures using the associated application on Windows ([#952](https://github.com/GenericMappingTools/pygmt/pull/952))
* Fix bug that stops Figure.coast from plotting with only dcw parameter ([#910](https://github.com/GenericMappingTools/pygmt/pull/910))

### Documentation

* Add a gallery example showing different line front styles ([#1022](https://github.com/GenericMappingTools/pygmt/pull/1022))
* Add a gallery example for a double y-axes graph ([#1019](https://github.com/GenericMappingTools/pygmt/pull/1019))
* Add a gallery example of inset map showing a rectangle region ([#1020](https://github.com/GenericMappingTools/pygmt/pull/1020))
* Add a gallery example to show coloring of points by categories ([#1006](https://github.com/GenericMappingTools/pygmt/pull/1006))
* Add gallery example showing different polar projection use cases ([#955](https://github.com/GenericMappingTools/pygmt/pull/955))
* Add underscore guideline to CONTRIBUTING.md ([#1034](https://github.com/GenericMappingTools/pygmt/pull/1034))
* Add instructions to upgrade installed PyGMT version ([#1029](https://github.com/GenericMappingTools/pygmt/pull/1029))
* Improve the docstring of the pygmt package ([#1016](https://github.com/GenericMappingTools/pygmt/pull/1016))
* Add common alias coltypes (-f) for specifying i/o data types ([#994](https://github.com/GenericMappingTools/pygmt/pull/994))
* Expand documentation linking in CONTRIBUTING.md ([#802](https://github.com/GenericMappingTools/pygmt/pull/802))
* Write changelog in markdown using MyST ([#941](https://github.com/GenericMappingTools/pygmt/pull/941))
* Update web font to Atkinson Hyperlegible ([#938](https://github.com/GenericMappingTools/pygmt/pull/938))
* Improve the gallery example for datetime inputs ([#919](https://github.com/GenericMappingTools/pygmt/pull/919))

### Maintenance

* Refactor plot and plot3d to use virtualfile_from_data ([#990](https://github.com/GenericMappingTools/pygmt/pull/990))
* Explicitly exclude unnecessary files in source distributions ([#999](https://github.com/GenericMappingTools/pygmt/pull/999))
* Refactor grd modules to use virtualfile_from_data ([#992](https://github.com/GenericMappingTools/pygmt/pull/992))
* Refactor info and grdinfo to use virtualfile_from_data ([#961](https://github.com/GenericMappingTools/pygmt/pull/961))
* Onboarding maintainer checklist ([#773](https://github.com/GenericMappingTools/pygmt/pull/773))
* Add comprehensive tests for pygmt.clib.loading.clib_full_names ([#872](https://github.com/GenericMappingTools/pygmt/pull/872))
* Add a workflow checking links in plaintext and HTML files ([#634](https://github.com/GenericMappingTools/pygmt/pull/634))
* Remove nbsphinx extension ([#931](https://github.com/GenericMappingTools/pygmt/pull/931))
* Improve the error message for loading an old version of the GMT library ([#925](https://github.com/GenericMappingTools/pygmt/pull/925))
* Move requirements-dev.txt dependencies to environment.yml ([#812](https://github.com/GenericMappingTools/pygmt/pull/812))
* Ensure proper non-dev version string when publishing to PyPI ([#900](https://github.com/GenericMappingTools/pygmt/pull/900))
* Run tests in a single CI job (Ubuntu + Python 3.9) for draft PRs ([#906](https://github.com/GenericMappingTools/pygmt/pull/906))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Jiayuan Yao](https://github.com/core-man)
* [Wei Ji Leong](https://github.com/weiji14)
* [Meghan Jones](https://github.com/meghanrjones)
* [Michael Grund](https://github.com/michaelgrund)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Liam Toney](https://github.com/liamtoney)
* [Kathryn Materna](https://github.com/kmaterna)
* [Alicia Ngoc Diep Ha](https://github.com/aliciaha1997)
* [Tawanda Moyo](https://github.com/tawandamoyo)

----

## Release v0.3.0 (2021/02/15)

[![Digital Object Identifier for PyGMT v0.3.0](https://zenodo.org/badge/DOI/10.5281/zenodo.4522136.svg)](https://doi.org/10.5281/zenodo.4522136)

### Highlights

* 🎉 **Third minor release of PyGMT** 🎉
* Wrap inset ([#788](https://github.com/GenericMappingTools/pygmt/pull/788)) for making overview maps and subplot ([#822](https://github.com/GenericMappingTools/pygmt/pull/822)) for multi-panel figures
* Apply standardized formatting conventions ([#775](https://github.com/GenericMappingTools/pygmt/pull/775)) across most documentation pages
* Drop Python 3.6 support ([#699](https://github.com/GenericMappingTools/pygmt/pull/699)) so PyGMT now requires Python 3.7 or newer

### New Features

* Wrap grd2cpt ([#803](https://github.com/GenericMappingTools/pygmt/pull/803))
* Let Figure.text support record-by-record transparency ([#716](https://github.com/GenericMappingTools/pygmt/pull/716))
* Provide basic support for FreeBSD ([#700](https://github.com/GenericMappingTools/pygmt/pull/700), [#878](https://github.com/GenericMappingTools/pygmt/pull/878))

### Enhancements

* Let load_earth_relief support the 'region' parameter for all resolutions ([#873](https://github.com/GenericMappingTools/pygmt/pull/873))
* Improve how PyGMT finds the GMT library ([#702](https://github.com/GenericMappingTools/pygmt/pull/702))
* Add common alias panel (-c) to all plotting functions ([#853](https://github.com/GenericMappingTools/pygmt/pull/853))
* Add aliases dcw ([#765](https://github.com/GenericMappingTools/pygmt/pull/765)) and lakes ([#781](https://github.com/GenericMappingTools/pygmt/pull/781)) to Figure.coast
* Add alias shading to Figure.colorbar ([#752](https://github.com/GenericMappingTools/pygmt/pull/752))
* Add alias annotation (A) to Figure.contour ([#883](https://github.com/GenericMappingTools/pygmt/pull/883))
* Wrap Figure.grdinfo aliases ([#799](https://github.com/GenericMappingTools/pygmt/pull/799))
* Add aliases frame and cmap to Figure.colorbar ([#709](https://github.com/GenericMappingTools/pygmt/pull/709))
* Add alias frame to Figure.grdview ([#707](https://github.com/GenericMappingTools/pygmt/pull/707))
* Improve the error message when PyGMT fails to load the GMT library ([#814](https://github.com/GenericMappingTools/pygmt/pull/814))
* Add GMTInvalidInput error to Figure.coast ([#787](https://github.com/GenericMappingTools/pygmt/pull/787))

### Documentation

* Add authorship policy ([#726](https://github.com/GenericMappingTools/pygmt/pull/726))
* Update PyGMT development installation instructions ([#865](https://github.com/GenericMappingTools/pygmt/pull/865))
* Add a tutorial for adding a map title ([#720](https://github.com/GenericMappingTools/pygmt/pull/720))
* Add a tutorial for plotting Earth relief ([#712](https://github.com/GenericMappingTools/pygmt/pull/712))
* Add a tutorial for 3D perspective image ([#743](https://github.com/GenericMappingTools/pygmt/pull/743))
* Add a tutorial for contour maps ([#705](https://github.com/GenericMappingTools/pygmt/pull/705))
* Add a tutorial for plotting lines ([#741](https://github.com/GenericMappingTools/pygmt/pull/741))
* Add a tutorial for the region argument ([#800](https://github.com/GenericMappingTools/pygmt/pull/800))
* Add a gallery example for datetime inputs ([#779](https://github.com/GenericMappingTools/pygmt/pull/779))
* Add a gallery example for Figure.logo ([#823](https://github.com/GenericMappingTools/pygmt/pull/823))
* Add a gallery example for plotting multi-parameter symbols ([#772](https://github.com/GenericMappingTools/pygmt/pull/772))
* Add a gallery example for Figure.image ([#777](https://github.com/GenericMappingTools/pygmt/pull/777))
* Add a gallery example for setting line colors with a custom CPT ([#774](https://github.com/GenericMappingTools/pygmt/pull/774))
* Add more gallery examples for projections ([#761](https://github.com/GenericMappingTools/pygmt/pull/761), [#721](https://github.com/GenericMappingTools/pygmt/pull/721), [#757](https://github.com/GenericMappingTools/pygmt/pull/757), [#723](https://github.com/GenericMappingTools/pygmt/pull/723), [#762](https://github.com/GenericMappingTools/pygmt/pull/762), [#742](https://github.com/GenericMappingTools/pygmt/pull/742), [#728](https://github.com/GenericMappingTools/pygmt/pull/728), [#727](https://github.com/GenericMappingTools/pygmt/pull/727))
* Update the docstrings in the plotting modules ([#881](https://github.com/GenericMappingTools/pygmt/pull/881))
* Update the docstrings in the non-plotting modules ([#882](https://github.com/GenericMappingTools/pygmt/pull/882))
* Update Figure.coast docstrings ([#798](https://github.com/GenericMappingTools/pygmt/pull/798))
* Update the docstrings of common aliases ([#862](https://github.com/GenericMappingTools/pygmt/pull/862))
* Add sphinx-copybutton extension to easily copy codes ([#838](https://github.com/GenericMappingTools/pygmt/pull/838))
* Choose the best figures in tutorials for thumbnails ([#826](https://github.com/GenericMappingTools/pygmt/pull/826))
* Update axis label explanation in frames tutorial ([#820](https://github.com/GenericMappingTools/pygmt/pull/820))
* Add guidelines for types of tests to write ([#796](https://github.com/GenericMappingTools/pygmt/pull/796))
* Recommend using SI units in documentation ([#795](https://github.com/GenericMappingTools/pygmt/pull/795))
* Add a table for compatibility of PyGMT with Python and GMT ([#763](https://github.com/GenericMappingTools/pygmt/pull/763))
* Add description for the "columns" arguments ([#766](https://github.com/GenericMappingTools/pygmt/pull/766))
* Add a table of the available projections ([#753](https://github.com/GenericMappingTools/pygmt/pull/753))
* Add projection description for Lambert Azimuthal Equal-Area ([#760](https://github.com/GenericMappingTools/pygmt/pull/760))
* Change text when GMTInvalidInput error is raised for basemap ([#729](https://github.com/GenericMappingTools/pygmt/pull/729))

### Bug Fixes

* Fix a bug of Figure.text when "text" is a non-string array ([#724](https://github.com/GenericMappingTools/pygmt/pull/724))
* Fix the error message when IPython is not available ([#701](https://github.com/GenericMappingTools/pygmt/pull/701))

### Maintenance

* Add dependabot to keep GitHub Actions up to date ([#861](https://github.com/GenericMappingTools/pygmt/pull/861))
* Skip workflows in PRs if only non-source-code files are changed ([#839](https://github.com/GenericMappingTools/pygmt/pull/839))
* Add slash command '/test-gmt-dev' to test GMT dev version ([#831](https://github.com/GenericMappingTools/pygmt/pull/831))
* Check files for UNIX-style line breaks and 644 permission ([#736](https://github.com/GenericMappingTools/pygmt/pull/736))
* Rename vercel configuration file from now.json to vercel.json ([#738](https://github.com/GenericMappingTools/pygmt/pull/738))
* Add a CI job testing GMT master branch on Windows ([#756](https://github.com/GenericMappingTools/pygmt/pull/756))
* Migrate documentation deployment from Travis CI to GitHub Actions ([#713](https://github.com/GenericMappingTools/pygmt/pull/713))
* Move Figure.meca into a standalone module ([#686](https://github.com/GenericMappingTools/pygmt/pull/686))
* Move plotting functions to separate modules ([#808](https://github.com/GenericMappingTools/pygmt/pull/808))
* Move non-plotting modules to separate modules ([#832](https://github.com/GenericMappingTools/pygmt/pull/832))
* Add isort to sort imports alphabetically ([#745](https://github.com/GenericMappingTools/pygmt/pull/745))
* Convert relative imports to absolute imports ([#754](https://github.com/GenericMappingTools/pygmt/pull/754))
* Switch from versioneer to setuptools-scm ([#695](https://github.com/GenericMappingTools/pygmt/pull/695))
* Add docformatter to format plain text in docstrings ([#642](https://github.com/GenericMappingTools/pygmt/pull/642))
* Migrate pytest configurations to pyproject.toml ([#725](https://github.com/GenericMappingTools/pygmt/pull/725))
* Migrate coverage configurations to pyproject.toml ([#667](https://github.com/GenericMappingTools/pygmt/pull/667))
* Show test execution times in pytest ([#835](https://github.com/GenericMappingTools/pygmt/pull/835))
* Add tests for grdfilter ([#809](https://github.com/GenericMappingTools/pygmt/pull/809))
* Add tests for GMTInvalidInput of Figure.savefig and Figure.show ([#810](https://github.com/GenericMappingTools/pygmt/pull/810))
* Add args_in_kwargs function ([#791](https://github.com/GenericMappingTools/pygmt/pull/791))
* Add a Makefile target 'distclean' for deleting project metadata files ([#744](https://github.com/GenericMappingTools/pygmt/pull/744))
* Add a test for Figure.basemap map_scale ([#739](https://github.com/GenericMappingTools/pygmt/pull/739))
* Use args_in_kwargs for Figure.basemap error raising ([#797](https://github.com/GenericMappingTools/pygmt/pull/797))

### Contributors

* [Will Schlitzer](https://github.com/willschlitzer)
* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Liam Toney](https://github.com/liamtoney)
* [Meghan Jones](https://github.com/meghanrjones)

----

## Release v0.2.1 (2020/11/14)

[![Digital Object Identifier for PyGMT v0.2.1](https://zenodo.org/badge/DOI/10.5281/zenodo.4253459.svg)](https://doi.org/10.5281/zenodo.4253459)

### Highlights

* 🎉 **Patch release with more tutorials and gallery examples!** 🎉
* 🐍 Support Python 3.9 ([#689](https://github.com/GenericMappingTools/pygmt/pull/689))
* 📹 Add [Liam](https://github.com/liamtoney)'s [ROSES 2020 PyGMT talk](https://www.youtube.com/watch?v=SSIGJEe0BIk) ([#643](https://github.com/GenericMappingTools/pygmt/pull/643))

### New Features

* Wrap plot3d ([#471](https://github.com/GenericMappingTools/pygmt/pull/471))
* Wrap grdfilter ([#616](https://github.com/GenericMappingTools/pygmt/pull/616))

### Enhancements

* Allow np.object dtypes into virtualfile_from_vectors ([#684](https://github.com/GenericMappingTools/pygmt/pull/684))
* Let plot() accept record-by-record transparency ([#626](https://github.com/GenericMappingTools/pygmt/pull/626))
* Refactor info to allow datetime inputs from xarray.Dataset and pandas.DataFrame tables ([#619](https://github.com/GenericMappingTools/pygmt/pull/619))

### Tutorials & Gallery

* Add tutorial for pygmt.config ([#482](https://github.com/GenericMappingTools/pygmt/pull/482))
* Add an example for different line styles ([#604](https://github.com/GenericMappingTools/pygmt/pull/604), [#664](https://github.com/GenericMappingTools/pygmt/pull/664))
* Add a gallery example for varying transparent points ([#654](https://github.com/GenericMappingTools/pygmt/pull/654))
* Add tutorial for pygmt.Figure.text ([#480](https://github.com/GenericMappingTools/pygmt/pull/480))
* Add an example for scatter plots with auto legends ([#607](https://github.com/GenericMappingTools/pygmt/pull/607))
* Improve colorbar gallery example ([#596](https://github.com/GenericMappingTools/pygmt/pull/596))

### Documentation Improvements

* doc: Fix the description of grdcontour -G option ([#681](https://github.com/GenericMappingTools/pygmt/pull/681))
* Refresh Code of Conduct from v1.4 to v2.0 ([#673](https://github.com/GenericMappingTools/pygmt/pull/673))
* Add PyGMT Zenodo BibTeX entry to main README.md ([#678](https://github.com/GenericMappingTools/pygmt/pull/678))
* Complete most of documentation for makecpt ([#676](https://github.com/GenericMappingTools/pygmt/pull/676))
* Complete documentation for plot ([#666](https://github.com/GenericMappingTools/pygmt/pull/666))
* Add "no_clip" to plot, text, contour and meca ([#661](https://github.com/GenericMappingTools/pygmt/pull/661))
* Add common alias "verbose" (V) to all functions ([#662](https://github.com/GenericMappingTools/pygmt/pull/662))
* Improve documentation of Figure.logo() ([#651](https://github.com/GenericMappingTools/pygmt/pull/651))
* Add mini-galleries for methods and functions ([#648](https://github.com/GenericMappingTools/pygmt/pull/648))
* Complete documentation of grdimage ([#620](https://github.com/GenericMappingTools/pygmt/pull/620))
* Add common alias perspective (p) for plotting 3D illustrations ([#627](https://github.com/GenericMappingTools/pygmt/pull/627))
* Add common aliases xshift (X) and yshift (Y) ([#624](https://github.com/GenericMappingTools/pygmt/pull/624))
* Add common alias cores (x) for grdimage and other multi-threaded modules ([#625](https://github.com/GenericMappingTools/pygmt/pull/625))
* Enable switching different versions of documentation ([#621](https://github.com/GenericMappingTools/pygmt/pull/621))
* Add common alias transparency (-t) to all plotting functions ([#614](https://github.com/GenericMappingTools/pygmt/pull/614))

### Bug Fixes

* Disallow passing arguments like -XNone to GMT ([#639](https://github.com/GenericMappingTools/pygmt/pull/639))

### Maintenance

* Migrate PyPI release to GitHub Actions ([#679](https://github.com/GenericMappingTools/pygmt/pull/679))
* Upload artifacts showing diff images on test failure ([#675](https://github.com/GenericMappingTools/pygmt/pull/675))
* Add slash command "/format" to automatically format PRs ([#646](https://github.com/GenericMappingTools/pygmt/pull/646))
* Add instructions to run specific tests ([#660](https://github.com/GenericMappingTools/pygmt/pull/660))
* Add more tests for xarray grid shading ([#650](https://github.com/GenericMappingTools/pygmt/pull/650))
* Refactor xfail tests to avoid storing baseline images ([#603](https://github.com/GenericMappingTools/pygmt/pull/603))
* Add blackdoc to format Python codes in docstrings ([#641](https://github.com/GenericMappingTools/pygmt/pull/641))
* Check and lint sphinx configuration file doc/conf.py ([#630](https://github.com/GenericMappingTools/pygmt/pull/630))
* Improve Makefile to clean ``__pycache__`` directory recursively ([#611](https://github.com/GenericMappingTools/pygmt/pull/611))
* Update release process and checklist template ([#602](https://github.com/GenericMappingTools/pygmt/pull/602))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Conor Bacon](https://github.com/hemmelig)
* [carocamargo](https://github.com/carocamargo)

----

## Release v0.2.0 (2020/09/12)

[![Digital Object Identifier for PyGMT v0.2.0](https://zenodo.org/badge/DOI/10.5281/zenodo.4025418.svg)](https://doi.org/10.5281/zenodo.4025418)

### Highlights

* 🎉 **Second minor release of PyGMT** 🎉
* Minimum required GMT version is now 6.1.1 or newer ([#577](https://github.com/GenericMappingTools/pygmt/pull/577))
* Plotting xarray grids using grdimage and grdview should not crash anymore and works for most cases ([#560](https://github.com/GenericMappingTools/pygmt/pull/560))
* Easier time-series plots with support for datetime-like inputs to plot ([#464](https://github.com/GenericMappingTools/pygmt/pull/464)) and the region argument ([#562](https://github.com/GenericMappingTools/pygmt/pull/562))

### New Features

* Wrap GMT_Put_Strings to pass str columns into GMT C API directly ([#520](https://github.com/GenericMappingTools/pygmt/pull/520))
* Wrap meca ([#516](https://github.com/GenericMappingTools/pygmt/pull/516))
* Wrap x2sys_init and x2sys_cross ([#546](https://github.com/GenericMappingTools/pygmt/pull/546))
* Let grdcut() accept xarray.DataArray as input ([#541](https://github.com/GenericMappingTools/pygmt/pull/541))
* Initialize a GMTDataArrayAccessor ([#500](https://github.com/GenericMappingTools/pygmt/pull/500))

### Enhancements

* Allow passing in pandas dataframes to x2sys_cross ([#591](https://github.com/GenericMappingTools/pygmt/pull/591))
* Sensible array outputs for pygmt info ([#575](https://github.com/GenericMappingTools/pygmt/pull/575))
* Allow pandas.DataFrame table and 1D/2D numpy array inputs into pygmt.info ([#574](https://github.com/GenericMappingTools/pygmt/pull/574))
* Add auto-legend feature to grdcontour and contour ([#568](https://github.com/GenericMappingTools/pygmt/pull/568))
* Add common alias verbose (V) ([#550](https://github.com/GenericMappingTools/pygmt/pull/550))
* Let load_earth_relief() support all resolutions and optional subregion ([#542](https://github.com/GenericMappingTools/pygmt/pull/542))
* Allow load_earth_relief() to load pixel or gridline registered data ([#509](https://github.com/GenericMappingTools/pygmt/pull/509))

### Documentation

* Link to try-gmt binder repository ([#598](https://github.com/GenericMappingTools/pygmt/pull/598))
* Improve docstring of data_kind() to include xarray grid ([#588](https://github.com/GenericMappingTools/pygmt/pull/588))
* Improve the documentation of Figure.shift_origin() ([#536](https://github.com/GenericMappingTools/pygmt/pull/536))
* Add shading to grdview gallery example ([#506](https://github.com/GenericMappingTools/pygmt/pull/506))

### Bug Fixes

* Ensure surface and grdcut loads GMTDataArray accessor info into xarray ([#539](https://github.com/GenericMappingTools/pygmt/pull/539))
* Raise an error if short- and long-form arguments coexist ([#537](https://github.com/GenericMappingTools/pygmt/pull/537))
* Fix the grdtrack example to avoid crashes on macOS ([#531](https://github.com/GenericMappingTools/pygmt/pull/531))
* Properly allow for either pixel or gridline registered grids ([#476](https://github.com/GenericMappingTools/pygmt/pull/476))

### Maintenance

* Add a test for xarray shading ([#581](https://github.com/GenericMappingTools/pygmt/pull/581))
* Remove expected failures on grdview tests ([#589](https://github.com/GenericMappingTools/pygmt/pull/589))
* Redesign check_figures_equal testing function to be more explicit ([#590](https://github.com/GenericMappingTools/pygmt/pull/590))
* Cut Windows CI build time in half to 15 min ([#586](https://github.com/GenericMappingTools/pygmt/pull/586))
* Add a test for Session.write_data() writing netCDF grids ([#583](https://github.com/GenericMappingTools/pygmt/pull/583))
* Add a test to make sure shift_origin does not crash ([#580](https://github.com/GenericMappingTools/pygmt/pull/580))
* Add testing.check_figures_equal to avoid storing baseline images ([#555](https://github.com/GenericMappingTools/pygmt/pull/555))
* Eliminate unnecessary jobs from Travis CI ([#567](https://github.com/GenericMappingTools/pygmt/pull/567)) and Azure Pipelines ([#513](https://github.com/GenericMappingTools/pygmt/pull/513))
* Improve the workflow to test both GMT master ([#485](https://github.com/GenericMappingTools/pygmt/pull/485)) and 6.1 branches ([#554](https://github.com/GenericMappingTools/pygmt/pull/554))
* Automatically cancel in-progress CI runs of old commits ([#544](https://github.com/GenericMappingTools/pygmt/pull/544))
* Remove the Stickler CI configuration file ([#538](https://github.com/GenericMappingTools/pygmt/pull/538)), run style checks using GitHub Actions ([#519](https://github.com/GenericMappingTools/pygmt/pull/519))
* Cache GMT remote data as artifacts on GitHub ([#530](https://github.com/GenericMappingTools/pygmt/pull/530))
* Let pytest generate both HTML and XML coverage reports ([#512](https://github.com/GenericMappingTools/pygmt/pull/512))
* Run Continuous Integration tests on GitHub Actions ([#475](https://github.com/GenericMappingTools/pygmt/pull/475))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Tyler Newton](https://github.com/tjnewton)
* [Liam Toney](https://github.com/liamtoney)

----

## Release v0.1.2 (2020/07/07)

[![Digital Object Identifier for PyGMT v0.1.2](https://zenodo.org/badge/DOI/10.5281/zenodo.3930577.svg)](https://doi.org/10.5281/zenodo.3930577)

### Highlights

* Patch release in preparation for the SciPy 2020 sprint session
* Last version to support GMT 6.0, future PyGMT versions will require GMT 6.1 or newer

### New Features

* Wrap grdcut ([#492](https://github.com/GenericMappingTools/pygmt/pull/492))
* Add show_versions() function for printing debugging information used in issue reports ([#466](https://github.com/GenericMappingTools/pygmt/pull/466))

### Enhancements

* Change load_earth_relief()'s default resolution to 01d ([#488](https://github.com/GenericMappingTools/pygmt/pull/488))
* Enhance text with extra functionality and aliases ([#481](https://github.com/GenericMappingTools/pygmt/pull/481))

### Documentation

* Add gallery example for grdview ([#502](https://github.com/GenericMappingTools/pygmt/pull/502))
* Turn all short aliases into long form ([#474](https://github.com/GenericMappingTools/pygmt/pull/474))
* Update the plotting example using the colormap generated by pygmt.makecpt ([#472](https://github.com/GenericMappingTools/pygmt/pull/472))
* Add instructions to view the test coverage reports locally ([#468](https://github.com/GenericMappingTools/pygmt/pull/468))
* Update the instructions for testing pygmt install ([#459](https://github.com/GenericMappingTools/pygmt/pull/459))

### Bug Fixes

* Fix a bug when passing data to GMT in Session.open_virtual_file() ([#490](https://github.com/GenericMappingTools/pygmt/pull/490))

### Maintenance

* Temporarily expect failures for some grdcontour and grdview tests ([#503](https://github.com/GenericMappingTools/pygmt/pull/503))
* Fix several failures due to updates of earth relief data ([#498](https://github.com/GenericMappingTools/pygmt/pull/498))
* Unpin pylint version and fix some lint warnings ([#484](https://github.com/GenericMappingTools/pygmt/pull/484))
* Separate tests of gmtinfo and grdinfo ([#461](https://github.com/GenericMappingTools/pygmt/pull/461))
* Fix the test for GMT_COMPATIBILITY=6 ([#454](https://github.com/GenericMappingTools/pygmt/pull/454))
* Update baseline images for updates of earth relief data ([#452](https://github.com/GenericMappingTools/pygmt/pull/452))
* Simplify PyGMT Release process ([#446](https://github.com/GenericMappingTools/pygmt/pull/446))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Liam Toney](https://github.com/liamtoney)

----

## Release v0.1.1 (2020/05/22)

[![Digital Object Identifier for PyGMT v0.1.1](https://zenodo.org/badge/DOI/10.5281/zenodo.3837197.svg)](https://doi.org/10.5281/zenodo.3837197)

### Highlights

* 🏁Windows users rejoice, this bugfix release is for you!🏁
* Let PyGMT work with the conda GMT package on Windows ([#434](https://github.com/GenericMappingTools/pygmt/pull/434))

### Enhancements

* Handle setting special parameters without default settings for config ([#411](https://github.com/GenericMappingTools/pygmt/pull/411))

### Documentation

* Update install instructions ([#430](https://github.com/GenericMappingTools/pygmt/pull/430))
* Add PyGMT AGU 2019 poster to website ([#425](https://github.com/GenericMappingTools/pygmt/pull/425))
* Redirect www.pygmt.org to latest, instead of dev ([#423](https://github.com/GenericMappingTools/pygmt/pull/423))

### Bug Fixes

* Set GMT_COMPATIBILITY to 6 when pygmt session starts ([#432](https://github.com/GenericMappingTools/pygmt/pull/432))
* Improve how PyGMT finds the GMT library ([#440](https://github.com/GenericMappingTools/pygmt/pull/440))

### Maintenance

* Finalize fixes on Windows test suite for v0.1.1 ([#441](https://github.com/GenericMappingTools/pygmt/pull/441))
* Cache test data on Azure Pipelines ([#438](https://github.com/GenericMappingTools/pygmt/pull/438))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Jason K. Moore](https://github.com/moorepants)

----

## Release v0.1.0 (2020/05/03)

[![Digital Object Identifier for PyGMT v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.3782862.svg)](https://doi.org/10.5281/zenodo.3782862)

### Highlights

* 🎉 **First official release of PyGMT** 🎉
* Python 3.8 is now supported ([#398](https://github.com/GenericMappingTools/pygmt/pull/398))
* PyGMT now uses the stable version of GMT 6.0.0 by default ([#363](https://github.com/GenericMappingTools/pygmt/pull/363))
* Use sphinx-gallery to manage examples and tutorials ([#268](https://github.com/GenericMappingTools/pygmt/pull/268))

### New Features

* Wrap blockmedian ([#349](https://github.com/GenericMappingTools/pygmt/pull/349))
* Add pygmt.config() to change gmt defaults locally and globally ([#293](https://github.com/GenericMappingTools/pygmt/pull/293))
* Wrap grdview ([#330](https://github.com/GenericMappingTools/pygmt/pull/330))
* Wrap grdtrack ([#308](https://github.com/GenericMappingTools/pygmt/pull/308))
* Wrap colorbar ([#332](https://github.com/GenericMappingTools/pygmt/pull/332))
* Wrap text ([#321](https://github.com/GenericMappingTools/pygmt/pull/321))
* Wrap legend ([#333](https://github.com/GenericMappingTools/pygmt/pull/333))
* Wrap makecpt ([#329](https://github.com/GenericMappingTools/pygmt/pull/329))
* Add a new method to shift plot origins ([#289](https://github.com/GenericMappingTools/pygmt/pull/289))

### Enhancements

* Allow text accepting "frame" as an argument ([#385](https://github.com/GenericMappingTools/pygmt/pull/385))
* Allow for grids with negative lat/lon increments ([#369](https://github.com/GenericMappingTools/pygmt/pull/369))
* Allow passing in list to 'region' argument in surface ([#378](https://github.com/GenericMappingTools/pygmt/pull/378))
* Allow passing in scalar number to x and y in plot ([#376](https://github.com/GenericMappingTools/pygmt/pull/376))
* Implement default position/box for legend ([#359](https://github.com/GenericMappingTools/pygmt/pull/359))
* Add sequence_space converter in kwargs_to_string ([#325](https://github.com/GenericMappingTools/pygmt/pull/325))

### Documentation

* Update PyPI install instructions and API disclaimer message ([#421](https://github.com/GenericMappingTools/pygmt/pull/421))
* Fix the link to GMT documentation ([#419](https://github.com/GenericMappingTools/pygmt/pull/419))
* Use napoleon instead of numpydoc with sphinx ([#383](https://github.com/GenericMappingTools/pygmt/pull/383))
* Document using a list for repeated arguments ([#361](https://github.com/GenericMappingTools/pygmt/pull/361))
* Add legend gallery entry ([#358](https://github.com/GenericMappingTools/pygmt/pull/358))
* Update instructions to set GMT_LIBRARY_PATH ([#324](https://github.com/GenericMappingTools/pygmt/pull/324))
* Fix the link to the GMT homepage ([#331](https://github.com/GenericMappingTools/pygmt/pull/331))
* Split projections gallery by projection types ([#318](https://github.com/GenericMappingTools/pygmt/pull/318))
* Fix the link to GMT/Matlab API in the README ([#297](https://github.com/GenericMappingTools/pygmt/pull/297))
* Use shinx extlinks for linking GMT docs ([#294](https://github.com/GenericMappingTools/pygmt/pull/294))
* Comment about country code in projection examples ([#290](https://github.com/GenericMappingTools/pygmt/pull/290))
* Add an overview page listing presentations ([#286](https://github.com/GenericMappingTools/pygmt/pull/286))

### Bug Fixes

* Let surface return xr.DataArray instead of xr.Dataset ([#408](https://github.com/GenericMappingTools/pygmt/pull/408))
* Update GMT constant GMT_STR16 to GMT_VF_LEN for GMT API change in 6.1.0 ([#397](https://github.com/GenericMappingTools/pygmt/pull/397))
* Properly trigger pytest matplotlib image comparison ([#352](https://github.com/GenericMappingTools/pygmt/pull/352))
* Use uuid.uuid4 to generate unique names ([#274](https://github.com/GenericMappingTools/pygmt/pull/274))

### Maintenance

* Quickfix Zeit Now miniconda installer link to anaconda.com ([#413](https://github.com/GenericMappingTools/pygmt/pull/413))
* Fix GitHub Pages deployment from Travis ([#410](https://github.com/GenericMappingTools/pygmt/pull/410))
* Update and clean TravisCI configuration ([#404](https://github.com/GenericMappingTools/pygmt/pull/404))
* Quickfix min elevation for new SRTM15+V2.1 earth relief grids ([#401](https://github.com/GenericMappingTools/pygmt/pull/401))
* Wrap docstrings to 79 chars and check with flake8 ([#384](https://github.com/GenericMappingTools/pygmt/pull/384))
* Update continuous integration scripts to 1.2.0 ([#355](https://github.com/GenericMappingTools/pygmt/pull/355))
* Use Zeit Now to deploy doc builds from PRs ([#344](https://github.com/GenericMappingTools/pygmt/pull/344))
* Move gmt from requirements.txt to CI scripts instead ([#343](https://github.com/GenericMappingTools/pygmt/pull/343))
* Change py.test to pytest ([#338](https://github.com/GenericMappingTools/pygmt/pull/338))
* Add Google Analytics to measure site visitors ([#314](https://github.com/GenericMappingTools/pygmt/pull/314))
* Register mpl_image_compare marker to remove PytestUnknownMarkWarning ([#323](https://github.com/GenericMappingTools/pygmt/pull/323))
* Disable Windows CI builds before PR [#313](https://github.com/GenericMappingTools/pygmt/pull/313) is merged ([#320](https://github.com/GenericMappingTools/pygmt/pull/320))
* Enable Mac and Windows CI on Azure Pipelines ([#312](https://github.com/GenericMappingTools/pygmt/pull/312))
* Fixes for using GMT 6.0.0rc1 ([#311](https://github.com/GenericMappingTools/pygmt/pull/311))
* Assign authorship to "The PyGMT Developers" ([#284](https://github.com/GenericMappingTools/pygmt/pull/284))

### Deprecations

* Remove mention of gitter.im ([#405](https://github.com/GenericMappingTools/pygmt/pull/405))
* Remove portrait (-P) from common options ([#339](https://github.com/GenericMappingTools/pygmt/pull/339))
* Remove require.js since WorldWind was dropped ([#278](https://github.com/GenericMappingTools/pygmt/pull/278))
* Remove Web WorldWind support ([#275](https://github.com/GenericMappingTools/pygmt/pull/275))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Leonardo Uieda](https://github.com/leouieda)
* [Liam Toney](https://github.com/liamtoney)
* [Brook Tozer](https://github.com/btozer)
* [Claudio Satriano](https://github.com/claudiodsf)
* [Cody Woodson](https://github.com/Dovacody)
* [Mark Wieczorek](https://github.com/MarkWieczorek)
* [Philipp Loose](https://github.com/phloose)
* [Kathryn Materna](https://github.com/kmaterna)
