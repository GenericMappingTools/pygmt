# Changelog

## Release v0.16.0 (2025/06/18)

[![Digital Object Identifier for PyGMT v0.16.0](https://zenodo.org/badge/DOI/10.5281/zenodo.15628725.svg)](https://doi.org/10.5281/zenodo.15628725)

### Highlights

* 🎉 **Sixteenth minor release of PyGMT** 🎉
* Implement gmt xarray BackendEntrypoint to load raster files via GMT ([#3919](https://github.com/GenericMappingTools/pygmt/pull/3919), [#3932](https://github.com/GenericMappingTools/pygmt/pull/3932))
* Remove the dependency of netCDF4 ([#3643](https://github.com/GenericMappingTools/pygmt/pull/3643))

### Enhancements

* pygmt.grdclip: Parameters 'between' and 'replace'  accept a 2-D sequence ([#3883](https://github.com/GenericMappingTools/pygmt/pull/3883))
* pygmt.grdlandmask: Improve the checking of parameters 'maskvalues'/'bordervalues' ([#3963](https://github.com/GenericMappingTools/pygmt/pull/3963))
* Figure.coast/pygmt.select/pygmt.grdlandmask: Use long names ("crude"/"low"/"intermediate"/"high"/"full") for the 'resolution' parameter ([#3013](https://github.com/GenericMappingTools/pygmt/pull/3013))
* Add a helper function sequence_join to join a sequence by a separator ([#3961](https://github.com/GenericMappingTools/pygmt/pull/3961))
* Improve decorators @use_alias/@fmt_docstrings to list non-aliased aliases ([#3965](https://github.com/GenericMappingTools/pygmt/pull/3965))
* Store first tile as source encoding for tiled grids ([#3950](https://github.com/GenericMappingTools/pygmt/pull/3950))

### Deprecations

* Figure: Deprecate the private _preprocess method (will be removed in v0.18.0) ([#3948](https://github.com/GenericMappingTools/pygmt/pull/3948))
* Deprecate pygmt.io.load_dataarray, use xarray.load_dataarray instead ([#3922](https://github.com/GenericMappingTools/pygmt/pull/3922))
* Session.virtualfile_in: Deprecate the parameter 'extra_arrays'. Prepare and pass a dictionary of arrays instead (will be removed in v0.20.0) ([#3823](https://github.com/GenericMappingTools/pygmt/pull/3823))
* Session.virtualfile_in: Deprecate parameter 'required_z'. Use 'mincols' instead (will be removed in v0.20.0) ([#3369](https://github.com/GenericMappingTools/pygmt/pull/3369))
* Session.virtualfile_in: Deprecate parameter 'required_data' to 'required' (will be removed in v0.20.0) ([#3931](https://github.com/GenericMappingTools/pygmt/pull/3931))
* Session.virtualfile_from_vectors: Remove the deprecated '*args' parameter [deprecated since v0.14.0] ([#3893](https://github.com/GenericMappingTools/pygmt/pull/3893))
* SPEC 0: Bump minimum supported versions to NumPy 1.26, xarray>=2023.07 and pandas>=2.1 ([#3916](https://github.com/GenericMappingTools/pygmt/pull/3916), [#3918](https://github.com/GenericMappingTools/pygmt/pull/3918), [#3895](https://github.com/GenericMappingTools/pygmt/pull/3895))
* Bump minimum supported version to pyarrow>=16, packaging>=24.2, geopandas>=1.0, and contextily>=1.5 ([#3917](https://github.com/GenericMappingTools/pygmt/pull/3917), [#3933](https://github.com/GenericMappingTools/pygmt/pull/3933), [#3908](https://github.com/GenericMappingTools/pygmt/pull/3908), [#3912](https://github.com/GenericMappingTools/pygmt/pull/3912))

### Bug Fixes

* pygmt.select: Parameter 'mask' accepts a sequence of strings ([#3956](https://github.com/GenericMappingTools/pygmt/pull/3956))

### Documentation

* GMTDataArrayAccessor: Improve the documentation to clarify how the accessor works ([#3955](https://github.com/GenericMappingTools/pygmt/pull/3955))

### Maintenance

* Update the AUTHORSHIP and Maintainers' Guides to reflect co-author contributions ([#3904](https://github.com/GenericMappingTools/pygmt/pull/3904))
* Set registration and gtype properly as enums on gmt accessor init ([#3942](https://github.com/GenericMappingTools/pygmt/pull/3942))
* Set license and license-files key in project metadata to follow PEP639 ([#3699](https://github.com/GenericMappingTools/pygmt/pull/3699))
* CI: Test NumPy 2.3 in the GMT Tests workflow ([#3968](https://github.com/GenericMappingTools/pygmt/pull/3968))
* Bump to ruff>=0.12.0 and fix violations ([#3980](https://github.com/GenericMappingTools/pygmt/pull/3980))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.15.0...v0.16.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Michael Grund](https://github.com/michaelgrund)
* [Federico Esteban](https://github.com/Esteban82)

---

## Release v0.15.0 (2025/03/31)

[![Digital Object Identifier for PyGMT v0.15.0](https://zenodo.org/badge/DOI/10.5281/zenodo.15071586.svg)](https://doi.org/10.5281/zenodo.15071586)

### Highlights

* 🎉 **Fifteenth minor release of PyGMT** 🎉
* One new gallery example and two new tutorials
* Figure.shift_origin: Support shifting origins temporarily when used as a context manager ([#2509](https://github.com/GenericMappingTools/pygmt/pull/2509))
* Documentation as HTML ZIP archive and in PDF format for offline reference

### Enhancements

* **BREAKING** Support typesetting apostrophe (') and backtick (`) ([#3105](https://github.com/GenericMappingTools/pygmt/pull/3105))
* **BREAKING** pygmt.grdcut: Refactor to store output in virtualfiles for grids ([#3115](https://github.com/GenericMappingTools/pygmt/pull/3115))
* GMTDataArrayAccessor: Support passing values using enums GridRegistration and GridType for grid registration and type ([#3696](https://github.com/GenericMappingTools/pygmt/pull/3696))
* pygmt.grdfill: Add new parameters 'constantfill'/'gridfill'/'neighborfill'/'splinefill' for filling holes ([#3855](https://github.com/GenericMappingTools/pygmt/pull/3855))
* pygmt.grdfill: Add new parameter 'inquire' to inquire the bounds of holes ([#3880](https://github.com/GenericMappingTools/pygmt/pull/3880))
* pygmt.grdfill: Add alias 'coltypes' (-f) ([#3869](https://github.com/GenericMappingTools/pygmt/pull/3869))

### Deprecations

* pygmt.grdfill: Deprecate parameter 'no_data' to 'hole' (remove in v0.19.0) ([#3852](https://github.com/GenericMappingTools/pygmt/pull/3852))
* pygmt.grdfill: Deprecate parameter 'mode', use parameters 'constantfill'/'gridfill'/'neighborfill'/'splinefill' instead (remove in v0.19.0) ([#3855](https://github.com/GenericMappingTools/pygmt/pull/3855))
* pygmt.grdclip: Deprecate parameter 'new' to 'replace' (remove in v0.19.0) ([#3884](https://github.com/GenericMappingTools/pygmt/pull/3884))
* clib.Session: Remove deprecated open_virtual_file method, use open_virtualfile instead (Deprecated since v0.11.0) ([#3738](https://github.com/GenericMappingTools/pygmt/pull/3738))
* clib.Session: Remove deprecated virtualfile_from_data method, use virtualfile_in instead (Deprecated since v0.13.0) ([#3739](https://github.com/GenericMappingTools/pygmt/pull/3739))

### Documentation

* Add an advanced tutorial for plotting focal mechanisms (beachballs) ([#2550](https://github.com/GenericMappingTools/pygmt/pull/2550))
* Add an advanced tutorial for creating legends ([#3594](https://github.com/GenericMappingTools/pygmt/pull/3594))
* Add a gallery example for Figure.hlines and Figure.vlines ([#3755](https://github.com/GenericMappingTools/pygmt/pull/3755))

### Maintenance

* Use the 'release-branch-semver' version scheme for setuptools_scm ([#3828](https://github.com/GenericMappingTools/pygmt/pull/3828))
* Rename _GMT_DATASET.to_dataframe to .to_pandas and _GMT_GRID.to_dataarray/_GMT_IMAGE.to_dataarray to .to_xarray ([#3798](https://github.com/GenericMappingTools/pygmt/pull/3798))
* Bump to ruff 0.9.0, apply ruff 2025 style, and ignore A005 (stdlib-module-shadowing) violations ([#3763](https://github.com/GenericMappingTools/pygmt/pull/3763))
* Use well-known labels in project URLs following PEP753 ([#3743](https://github.com/GenericMappingTools/pygmt/pull/3743))
* clib.conversion: Remove the unused array_to_datetime function ([#3507](https://github.com/GenericMappingTools/pygmt/pull/3507))
* CI: Test on Linux arm64 runners ([#3778](https://github.com/GenericMappingTools/pygmt/pull/3778))
* CI: Build PDF documentation using tectonic ([#3765](https://github.com/GenericMappingTools/pygmt/pull/3765))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.14.0...v0.15.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)

---

## Release v0.14.2 (2025/02/15)

[![Digital Object Identifier for PyGMT v0.14.2](https://zenodo.org/badge/DOI/10.5281/zenodo.14868324.svg)](https://doi.org/10.5281/zenodo.14868324)


### Bug Fixes

* **Patch release fixing a critical bug introduced in PyGMT v0.14.1**
* Fix the bug for passing text strings with numeric values ([#3804](https://github.com/GenericMappingTools/pygmt/pull/3804))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.14.1...v0.14.2>

### Contributors

* [Dongdong Tian](https://github.com/seisman)

---

## Release v0.14.1 (2025/02/01)

[![Digital Object Identifier for PyGMT v0.14.1](https://zenodo.org/badge/DOI/10.5281/zenodo.14742338.svg)](https://doi.org/10.5281/zenodo.14742338)

### Highlights

* **Patch release fixing critical bugs in PyGMT v0.14.0**
* Fix the bug of converting Python sequence of datetime-like objects ([#3760](https://github.com/GenericMappingTools/pygmt/pull/3760))

### Maintenance

* CI: Separate jobs for publishing to TestPyPI and PyPI ([#3742](https://github.com/GenericMappingTools/pygmt/pull/3742))
* clib.conversion._to_numpy: Add tests for Python sequence of datetime-like objects ([#3758](https://github.com/GenericMappingTools/pygmt/pull/3758))
* Fix an image in README.md (broken on PyPI) and rewrap to 88 characters ([#3740](https://github.com/GenericMappingTools/pygmt/pull/3740))
* Fix the dataset link in the RGB image gallery example ([#3781](https://github.com/GenericMappingTools/pygmt/pull/3781))
* Update License year to 2025 ([#3737](https://github.com/GenericMappingTools/pygmt/pull/3737))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.14.0...v0.14.1>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)

---

## Release v0.14.0 (2024/12/31)

[![Digital Object Identifier for PyGMT v0.14.0](https://zenodo.org/badge/DOI/10.5281/zenodo.14535921.svg)](https://doi.org/10.5281/zenodo.14535921)

### Highlights

* 🎉 **Fourteenth minor release of PyGMT** 🎉
* Bump minimum supported version to GMT>=6.4.0 ([#3450](https://github.com/GenericMappingTools/pygmt/pull/3450))
* Two new plotting methods and six new functions to access more GMT remote datasets
* PyArrow as an optional dependency and improved support of PyArrow data types ([#3592](https://github.com/GenericMappingTools/pygmt/pull/3592))

### New Features

* Add Figure.hlines for plotting horizontal lines ([#923](https://github.com/GenericMappingTools/pygmt/pull/923))
* Add Figure.vlines for plotting vertical lines ([#3726](https://github.com/GenericMappingTools/pygmt/pull/3726))
* Add load_black_marble to load "Black Marble" dataset ([#3469](https://github.com/GenericMappingTools/pygmt/pull/3469))
* Add load_blue_marble to load "Blue Marble" dataset ([#2235](https://github.com/GenericMappingTools/pygmt/pull/2235))
* Add load_earth_deflection to load "IGPP Earth east-west and north-south deflection" datasets ([#3728](https://github.com/GenericMappingTools/pygmt/pull/3728))
* Add load_earth_dist to load "GSHHG Earth distance to shoreline" dataset ([#3706](https://github.com/GenericMappingTools/pygmt/pull/3706))
* Add load_earth_mean_dynamic_topography to load "CNES Earth Mean Dynamic Topography" dataset ([#3718](https://github.com/GenericMappingTools/pygmt/pull/3718))
* Add load_earth_mean_sea_surface to load "CNES Earth Mean Sea Surface" dataset ([#3717](https://github.com/GenericMappingTools/pygmt/pull/3717))
* load_earth_free_air_anomaly: Add "uncertainty" parameter to load the "IGPP Earth free-air anomaly uncertainty" dataset  ([#3727](https://github.com/GenericMappingTools/pygmt/pull/3727))


### Enhancements

* Figure.plot: Add the "symbol" parameter to support plotting data points with varying symbols ([#1117](https://github.com/GenericMappingTools/pygmt/pull/1117))
* Figure.plot3d: Add the "symbol" parameter to support plotting data points with varying symbols ([#3559](https://github.com/GenericMappingTools/pygmt/pull/3559))
* Figure.legend: Support passing a StringIO object as the legend specification ([#3438](https://github.com/GenericMappingTools/pygmt/pull/3438))
* load_tile_map: Add parameter "crs" to set the CRS of the returned dataarray ([#3554](https://github.com/GenericMappingTools/pygmt/pull/3554))
* PyArrow: Support pyarrow arrays with string/large_string/string_view types ([#3619](https://github.com/GenericMappingTools/pygmt/pull/3619))
* Support 1-D/2-D numpy arrays with longlong and ulonglong dtype ([#3566](https://github.com/GenericMappingTools/pygmt/pull/3566))
* GMT_IMAGE: Implement the to_dataarray method for 3-band images ([#3128](https://github.com/GenericMappingTools/pygmt/pull/3128))
* Ensure non-ASCII characters are typeset correctly even if PS_CHAR_ENCODING is not "ISOLatin1+" ([#3611](https://github.com/GenericMappingTools/pygmt/pull/3611))
* Add enums GridRegistration and GridType for grid registration and type ([#3693](https://github.com/GenericMappingTools/pygmt/pull/3693))

### Deprecations

* SPEC 0: Bump minimum supported versions to Python 3.11, NumPy 1.25, pandas>=2.0 and xarray>=2023.04 ([#3460](https://github.com/GenericMappingTools/pygmt/pull/3460), [#3606](https://github.com/GenericMappingTools/pygmt/pull/3606), [#3697](https://github.com/GenericMappingTools/pygmt/pull/3697))
* clib.Session.virtualfile_from_vectors: Now takes a sequence of vectors as its single argument (Passing multiple arguments will be unsupported in v0.16.0) ([#3522](https://github.com/GenericMappingTools/pygmt/pull/3522))
* Remove the deprecated build_arg_string function (deprecated since v0.12.0) ([#3427](https://github.com/GenericMappingTools/pygmt/pull/3427))
* Figure.grdcontour: Remove the deprecated syntax for the 'annotation' parameter (deprecated since v0.12.0) ([#3428](https://github.com/GenericMappingTools/pygmt/pull/3428))

### Bug Fixes

* launch_external_viewer: Use full path when opening the file in a web browser ([#3647](https://github.com/GenericMappingTools/pygmt/pull/3647))
* PyArrow: Map date32[day]/date64[ms] dtypes in pandas objects to np.datetime64 with correct date/time units ([#3617](https://github.com/GenericMappingTools/pygmt/pull/3617))
* clib.session: Add the GMT_SESSION_NOGDALCLOSE flag to keep GDAL open ([#3672](https://github.com/GenericMappingTools/pygmt/pull/3672))
* Set the "Conventions" attribute to "CF-1.7" for netCDF grids only ([#3463](https://github.com/GenericMappingTools/pygmt/pull/3463))
* Fix the conversion error for pandas.Series with missing values in pandas<=2.1 ([#3505](https://github.com/GenericMappingTools/pygmt/pull/3505), [#3596](https://github.com/GenericMappingTools/pygmt/pull/3596))
* GeoPandas: Explicitly convert columns with overflow integers to avoid OverflowError with fiona 1.10 ([#3455](https://github.com/GenericMappingTools/pygmt/pull/3455))
* Figure.plot/Figure.plot3d: Improve the check of the "style" parameter for "v" or "V" ([#3603](https://github.com/GenericMappingTools/pygmt/pull/3603))
* Correctly reserve the grid data dtype by converting ctypes array to numpy array with np.ctypeslib.as_array ([#3446](https://github.com/GenericMappingTools/pygmt/pull/3446))
* **Breaking**: Figure.text: Fix typesetting of integers when mixed with floating-point values ([#3493](https://github.com/GenericMappingTools/pygmt/pull/3493))

### Documentation

* Add basic tutorial "Plotting polygons" ([#3593](https://github.com/GenericMappingTools/pygmt/pull/3593))
* Update the gallery example for plotting lines with LineString/MultiLineString geometry ([#3711](https://github.com/GenericMappingTools/pygmt/pull/3711))
* Add the PyGMT ecosystem page ([#3475](https://github.com/GenericMappingTools/pygmt/pull/3475))
* Document the support policy for optional packages ([#3616](https://github.com/GenericMappingTools/pygmt/pull/3616))
* Document the environment variables that can affect the behavior of PyGMT ([#3432](https://github.com/GenericMappingTools/pygmt/pull/3432))
* Document the built-in patterns in the Technical Reference section ([#3466](https://github.com/GenericMappingTools/pygmt/pull/3466))
* Document Continuous Benchmarking in Maintainers Guides ([#3631](https://github.com/GenericMappingTools/pygmt/pull/3631))
* Add instructions for installing optional dependencies ([#3506](https://github.com/GenericMappingTools/pygmt/pull/3506))
* Update "PyData Ecosystem" to "Scientific Python Ecosystem" ([#3447](https://github.com/GenericMappingTools/pygmt/pull/3447))
* Figure.savefig: Clarify that the "transparent" parameter also works for the PNG file associated with the KML format ([#3579](https://github.com/GenericMappingTools/pygmt/pull/3579))
* Add the PyGMT talk at AGU24 to the "Overview" section ([#3685](https://github.com/GenericMappingTools/pygmt/pull/3685))
* Add the GMT/PyGMT pre-conference workshop at AGU24 to the "External resources" section ([#3689](https://github.com/GenericMappingTools/pygmt/pull/3689))
* Add TODO comments in the maintainers guides and update the release checklist ([#3724](https://github.com/GenericMappingTools/pygmt/pull/3724))

### Maintenance

* **Breaking**: data_kind: data is None and required now returns the "empty" kind ([#3482](https://github.com/GenericMappingTools/pygmt/pull/3482))
* **Breaking**: data_kind: Now "matrix" represents a 2-D numpy array and unrecognized data types fall back to "vectors" ([#3351](https://github.com/GenericMappingTools/pygmt/pull/3351))
* Add Support for Python 3.13 ([#3490](https://github.com/GenericMappingTools/pygmt/pull/3490))
* Add the Session.virtualfile_from_stringio method to allow StringIO input for certain functions/methods ([#3326](https://github.com/GenericMappingTools/pygmt/pull/3326))
* Add "geodatasets" as a dependency for docs and update the choropleth example ([#3719](https://github.com/GenericMappingTools/pygmt/pull/3719))
* PyArrow: Check compatibility of pyarrow.array with string type ([#2933](https://github.com/GenericMappingTools/pygmt/pull/2933))
* Rename sphinx-gallery's README.txt to GALLERY_HEADER.rst and require Sphinx-Gallery>=0.17.0 ([#3348](https://github.com/GenericMappingTools/pygmt/pull/3348))
* clib.conversion: Remove the as_c_contiguous function and use np.ascontiguousarray instead ([#3492](https://github.com/GenericMappingTools/pygmt/pull/3492))
* Use TODO comments to track deprecations and workarounds ([#3722](https://github.com/GenericMappingTools/pygmt/pull/3722))
* Move Figure.psconvert into a separate file ([#3553](https://github.com/GenericMappingTools/pygmt/pull/3553))
* Improve the data type checking for 2-D arrays passed to the GMT C API ([#3563](https://github.com/GenericMappingTools/pygmt/pull/3563))
* Enable ruff's TD (flake8-todos), COM (flake8-commas), TRY (tryceratops), and EM (flake8-errmsg) rules ([#3723](https://github.com/GenericMappingTools/pygmt/pull/3723), [#3531](https://github.com/GenericMappingTools/pygmt/pull/3531), [#3665](https://github.com/GenericMappingTools/pygmt/pull/3665), [#3661](https://github.com/GenericMappingTools/pygmt/pull/3661))
* CI: Install pyarrow-core instead of pyarrow from conda-forge ([#3698](https://github.com/GenericMappingTools/pygmt/pull/3698))
* CI: Ensure no hyphens in Python file and directory names in the "Style Checks" workflow ([#3703](https://github.com/GenericMappingTools/pygmt/pull/3703))
* Bump to ruff>=0.8.0 and rename rule TCH to TC ([#3662](https://github.com/GenericMappingTools/pygmt/pull/3662))
* Bump to Ghostscript 10.04.0 ([#3443](https://github.com/GenericMappingTools/pygmt/pull/3443))
* Add enums GridFormat for GMT grid format ID ([#3449](https://github.com/GenericMappingTools/pygmt/pull/3449))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.13.0...v0.14.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Jiayuan Yao](https://github.com/core-man)

---

## Release v0.13.0 (2024/09/05)

[![Digital Object Identifier for PyGMT v0.13.0](https://zenodo.org/badge/DOI/10.5281/zenodo.13679420.svg)](https://doi.org/10.5281/zenodo.13679420)

### Highlights

* 🎉 **Thirteenth minor release of PyGMT** 🎉
* Add new documentation section "Technical Reference" and document the supported encodings and fonts
* Tutorial for "Draping a dataset on top of a topographic surface" ([#3316](https://github.com/GenericMappingTools/pygmt/pull/3316))
* Tutorial for "Typesetting non-ASCII characters" ([#3389](https://github.com/GenericMappingTools/pygmt/pull/3389))

### New Features

* Wrap the GMT API function GMT_Read_Data to read data into GMT data containers ([#3324](https://github.com/GenericMappingTools/pygmt/pull/3324))
* Wrap GMT's standard data type GMT_IMAGE for images ([#3338](https://github.com/GenericMappingTools/pygmt/pull/3338))

### Enhancements

* **Breaking**: pygmt.x2sys_cross: Refactor to use virtualfiles for output tables ([#3182](https://github.com/GenericMappingTools/pygmt/pull/3182))
* pygmt.show_versions: Warn about incompatible Ghostscript versions ([#3244](https://github.com/GenericMappingTools/pygmt/pull/3244))
* pygmt.show_versions: Show GDAL version ([#3364](https://github.com/GenericMappingTools/pygmt/pull/3364), [#3376](https://github.com/GenericMappingTools/pygmt/pull/3376))
* pygmt.datasets.load_*: Add autocompletion support for the 'resolution' parameter ([#3260](https://github.com/GenericMappingTools/pygmt/pull/3260))
* clib.Session: Refactor the `__getitem__` special method to avoid calling API function GMT_Get_Enum repeatedly ([#3261](https://github.com/GenericMappingTools/pygmt/pull/3261))
* clib: Refactor to avoid checking GMT version repeatedly and only check once when loading the GMT library ([#3254](https://github.com/GenericMappingTools/pygmt/pull/3254))
* Support non-ASCII characters in ISO-8859-x charsets ([#3310](https://github.com/GenericMappingTools/pygmt/pull/3310))
* Refactor to improve the user experience with non-ASCII characters ([#3206](https://github.com/GenericMappingTools/pygmt/pull/3206))

### Deprecations

* SPEC 0: Bump minimum supported version to xarray 2022.09 ([#3372](https://github.com/GenericMappingTools/pygmt/pull/3372))
* SPEC 0: Bump minimum supported version to NumPy 1.24 ([#3286](https://github.com/GenericMappingTools/pygmt/pull/3286))
* clib: Deprecate API function 'Session.virtualfile_from_data', use 'Session.virtualfile_in' instead (will be removed in v0.15.0) ([#3225](https://github.com/GenericMappingTools/pygmt/pull/3225))
* Remove the unused pygmt.print_clib_info function ([#3257](https://github.com/GenericMappingTools/pygmt/pull/3257))
* Figure.timestamp: Remove deprecated parameter 'justification', use 'justify' instead (deprecated since v0.11.0) ([#3222](https://github.com/GenericMappingTools/pygmt/pull/3222))

### Bug Fixes

* pygmt.set_display: Fix the bug that `method=None` doesn't reset to the default display method ([#3396](https://github.com/GenericMappingTools/pygmt/pull/3396))
* load_tile_map: Register the rio accessor by importing rioxarray, so the returned raster has CRS ([#3323](https://github.com/GenericMappingTools/pygmt/pull/3323))
* load_tile_map: Fix the raster band indexing, should start from 1 ([#3322](https://github.com/GenericMappingTools/pygmt/pull/3322))
* load_tile_map: Replace deprecated rio.set_crs with rio.write_crs ([#3321](https://github.com/GenericMappingTools/pygmt/pull/3321))
* PYGMT_USE_EXTERNAL_DISPLAY should NOT disable image display in Jupyter notebook environment ([#3418](https://github.com/GenericMappingTools/pygmt/pull/3418))

### Documentation

* External Resources: Add tutorial in Portuguese and using PyGMT in Google Colab ([#3360](https://github.com/GenericMappingTools/pygmt/pull/3360))
* Remove the non-official GMT wrappers from README ([#3413](https://github.com/GenericMappingTools/pygmt/pull/3413))
* Give recommendations about GMT-Ghostscript incompatibility and the testing example ([#3249](https://github.com/GenericMappingTools/pygmt/pull/3249))
* Document the supported 35 standard Postscript fonts in the Technical Reference section ([#3378](https://github.com/GenericMappingTools/pygmt/pull/3378))
* Add an offboarding access checklist for maintainers ([#3411](https://github.com/GenericMappingTools/pygmt/pull/3411))
* Update the onboarding access checklist in Maintainers Guides ([#3404](https://github.com/GenericMappingTools/pygmt/pull/3404))
* Add sphinx extension myst-nb to enable writing executable Markdown notebooks ([#3379](https://github.com/GenericMappingTools/pygmt/pull/3379))

### Maintenance

* pygmt.grd2cpt & pygmt.makecpt: Simplify the logic for dealing with CPT output ([#3334](https://github.com/GenericMappingTools/pygmt/pull/3334))
* geopandas: Use io.StringIO to read geojson data and handle compatibility with geopandas v0.x and v1.x ([#3247](https://github.com/GenericMappingTools/pygmt/pull/3247))
* Simplify the "Minimum Supported Versions" page using MyST customized URL schemes ([#3383](https://github.com/GenericMappingTools/pygmt/pull/3383))
* build_arg_list: Raise an exception if an invalid output file name is given ([#3336](https://github.com/GenericMappingTools/pygmt/pull/3336))
* sphinx-gallery: Temporarily pin to < 0.17.0 ([#3350](https://github.com/GenericMappingTools/pygmt/pull/3350))
* Run pytest with `--color=yes` to force GitHub Actions logs to have color ([#3330](https://github.com/GenericMappingTools/pygmt/pull/3330))
* Patch the callback print function to suppress the UnicodeDecodeError ([#3367](https://github.com/GenericMappingTools/pygmt/pull/3367))
* Move Will from Active Maintainers to Distinguished Contributors ([#3388](https://github.com/GenericMappingTools/pygmt/pull/3388))
* Enable ruff's unspecified-encoding (PLW1514) rule and fix violations ([#3319](https://github.com/GenericMappingTools/pygmt/pull/3319))
* Enable ruff's literal-membership (PLR6201) rule and fix violations ([#3317](https://github.com/GenericMappingTools/pygmt/pull/3317))
* Determine the minimum required versions of dependencies from package metadata for docs ([#3380](https://github.com/GenericMappingTools/pygmt/pull/3380))
* CI: Use OIDC token for codecov uploading ([#3163](https://github.com/GenericMappingTools/pygmt/pull/3163))
* CI: Test NumPy 2.1 in the GMT Tests workflow ([#3401](https://github.com/GenericMappingTools/pygmt/pull/3401))
* CI: Set GMT_ENABLE_OPENMP to TRUE to enable OpenMP support on macOS ([#3266](https://github.com/GenericMappingTools/pygmt/pull/3266))
* CI: Fix the name of the 'build' package to 'python-build' on conda-forge ([#3408](https://github.com/GenericMappingTools/pygmt/pull/3408))
* CI: Bump to ubuntu-24.04 and mambaforge-23.11 in ReadTheDocs ([#3296](https://github.com/GenericMappingTools/pygmt/pull/3296))
* CI: Build GMT dev source code with OpenMP enabled on Linux and GThreads enabled on Linux/macOS ([#3011](https://github.com/GenericMappingTools/pygmt/pull/3011))
* CI: Add pytest plugins pytest-xdist and pytest-rerunfailures ([#3193](https://github.com/GenericMappingTools/pygmt/pull/3193), [#3267](https://github.com/GenericMappingTools/pygmt/pull/3267))
* Add pre-commit config with pre-commit-hooks and enable pre-commit.ci to update hooks quarterly ([#3283](https://github.com/GenericMappingTools/pygmt/pull/3283), [#3414](https://github.com/GenericMappingTools/pygmt/pull/3414))
* Add a test to make sure PyGMT works with paths that contain non-ASCII characters ([#3280](https://github.com/GenericMappingTools/pygmt/pull/3280))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.12.0...v0.13.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Andre L. Belem](https://github.com/andrebelem)

---

## Release v0.12.0 (2024/05/01)

[![Digital Object Identifier for PyGMT v0.12.0](https://zenodo.org/badge/DOI/10.5281/zenodo.11062720.svg)](https://doi.org/10.5281/zenodo.11062720)

### Highlights

* 🎉 **Twelfth minor release of PyGMT** 🎉
* 🚀 Almost all module wrappers (with a few exceptions) now use in-memory GMT *virtual files* instead of intermediate temporary files to improve performance ([#2730](https://github.com/GenericMappingTools/pygmt/issues/2730))
* Almost all module wrappers (with a few exceptions) now have consistent behavior for table-like output ([#1318](https://github.com/GenericMappingTools/pygmt/issues/1318))
* Adopt [SPEC 0](https://scientific-python.org/specs/spec-0000/) policy for minimum supported versions of GMT, Python, and other core dependencies

### Enhancements

* **Breaking**: (Unneeded) extra double quotes around text strings (containing whitespaces) are now considered as part of the text string ([#3132](https://github.com/GenericMappingTools/pygmt/pull/3132), [#3457](https://github.com/GenericMappingTools/pygmt/issues/3457))
* pygmt.project: Add 'output_type' parameter for output in pandas/numpy/file formats ([#3110](https://github.com/GenericMappingTools/pygmt/pull/3110))
* pygmt.grdtrack: Add 'output_type' parameter for output in pandas/numpy/file formats ([#3106](https://github.com/GenericMappingTools/pygmt/pull/3106))
* pygmt.blockm*: Add 'output_type' parameter for output in pandas/numpy/file formats ([#3103](https://github.com/GenericMappingTools/pygmt/pull/3103))
* Figure.grdcontour: Adjust processing arguments passed to "annotation" and "interval" parameters ([#3116](https://github.com/GenericMappingTools/pygmt/pull/3116))
* Figure.contour: Adjust processing arguments passed to "annotation" and "levels" parameters ([#2706](https://github.com/GenericMappingTools/pygmt/pull/2706))
* clib: Wrap the GMT API function GMT_Read_VirtualFile ([#2993](https://github.com/GenericMappingTools/pygmt/pull/2993))
* clib: Add virtualfile_to_dataset method for converting virtualfile to a dataset ([#3083](https://github.com/GenericMappingTools/pygmt/pull/3083), [#3140](https://github.com/GenericMappingTools/pygmt/pull/3140), [#3157](https://github.com/GenericMappingTools/pygmt/pull/3157),
[#3117](https://github.com/GenericMappingTools/pygmt/pull/3117))
* clib: Add the virtualfile_out method for creating output virtualfile ([#3057](https://github.com/GenericMappingTools/pygmt/pull/3057))
* Wrap GMT_Inquire_VirtualFile to get the family of virtualfiles ([#3152](https://github.com/GenericMappingTools/pygmt/pull/3152))
* Wrap GMT's standard data type GMT_GRID for grids ([#2398](https://github.com/GenericMappingTools/pygmt/pull/2398))
* Wrap GMT's standard data type GMT_DATASET for table inputs ([#2729](https://github.com/GenericMappingTools/pygmt/pull/2729), [#3131](https://github.com/GenericMappingTools/pygmt/pull/3131), [#3174](https://github.com/GenericMappingTools/pygmt/pull/3174))
* Wrap GMT's data structure GMT_GRID_HEADER for grid/image/cube headers ([#3127](https://github.com/GenericMappingTools/pygmt/pull/3127), [#3134](https://github.com/GenericMappingTools/pygmt/pull/3134))
* Session.call_module: Support passing a list of argument strings ([#3139](https://github.com/GenericMappingTools/pygmt/pull/3139))
* Refactor the _load_remote_dataset function to load tiled and non-tiled grids in a consistent way ([#3120](https://github.com/GenericMappingTools/pygmt/pull/3120))
* Refactor all wrappers to pass an argument list to Session.call_module ([#3132](https://github.com/GenericMappingTools/pygmt/pull/3132))
* Add function build_arg_list for building arguments list from keyword dictionaries ([#3149](https://github.com/GenericMappingTools/pygmt/pull/3149))
* Support left/right single quotation marks in text and arguments ([#3192](https://github.com/GenericMappingTools/pygmt/pull/3192))
* non_ascii_to_octal: Return the input string if it only contains printable ASCII characters ([#3199](https://github.com/GenericMappingTools/pygmt/pull/3199))

### Deprecations

* SPEC 0: Set minimum supported versions to Python>=3.10, pandas>=1.5 and xarray>=2022.06 ([#3043](https://github.com/GenericMappingTools/pygmt/pull/3043), [#3039](https://github.com/GenericMappingTools/pygmt/pull/3039), [#3151](https://github.com/GenericMappingTools/pygmt/pull/3151))
* Figure.plot/plot3d/rose: Remove deprecated parameter "color", use "fill" instead (deprecated since v0.8.0) ([#3032](https://github.com/GenericMappingTools/pygmt/pull/3032))
* Figure.velo: Remove deprecated parameters "color"/"uncertaintycolor", use "fill"/"uncertaintyfill" instead (deprecated since v0.8.0) ([#3034](https://github.com/GenericMappingTools/pygmt/pull/3034))
* Figure.wiggle: Remove deprecated parameter "color", use "fillpositive"/"fillnegative" instead (deprecated since v0.8.0) ([#3035](https://github.com/GenericMappingTools/pygmt/pull/3035))
* Figure.grdimage: Remove deprecated parameter "bit_color", use "bitcolor" instead (deprecated since v0.8.0) ([#3036](https://github.com/GenericMappingTools/pygmt/pull/3036))
* Figure: Remove deprecated "xshift" ("X") and "yshift" ("Y") parameters, use "Figure.shift_origin" instead (deprecated since v0.8.0) ([#3044](https://github.com/GenericMappingTools/pygmt/pull/3044))
* Figure: Remove deprecated "timestamp" ("U") parameter, use "Figure.timestamp" instead (deprecated since v0.9.0) ([#3045](https://github.com/GenericMappingTools/pygmt/pull/3045))
* clib: Rename the "virtualfile_from_data" method to "virtualfile_in" ([#3068](https://github.com/GenericMappingTools/pygmt/pull/3068))
* Deprecate the "build_arg_string" function, use build_arg_list instead (deprecated since v0.12.0, will be removed in v0.14.0) ([#3184](https://github.com/GenericMappingTools/pygmt/pull/3184))
* Deprecate the "sequence_plus" converter, only used for the "annotation" parameter of Figure.grdcontour (deprecated since v0.12.0, will be removed in v0.14.0) ([#3207](https://github.com/GenericMappingTools/pygmt/pull/3207))
* Figure.grdcontour: Deprecate parameter "interval" to "levels" (FutureWarning since v0.12.0, will be removed in v0.16.0) ([#3209](https://github.com/GenericMappingTools/pygmt/pull/3209))

### Documentation

* External Resources: Add repository "gmt-pygmt-plotting" ([#3213](https://github.com/GenericMappingTools/pygmt/pull/3213))
* Gallery example "Custom symbols": Mention own custom symbols ([#3186](https://github.com/GenericMappingTools/pygmt/pull/3186))
* Intro "04 Table inputs": Document that a list of file names, pathlib.Path objects, URLs, or remote files is supported ([3214](https://github.com/GenericMappingTools/pygmt/pull/3214))
* Tutorial "Plotting text": Rewrite to improve structure, explain more parameters, show list input ([#2760](https://github.com/GenericMappingTools/pygmt/pull/2760))

### Maintenance

* pygmt.filter1d: Improve performance by storing output in virtual files ([#3085](https://github.com/GenericMappingTools/pygmt/pull/3085))
* pygmt.grdvolume: Refactor to store output in virtual files instead of temporary files ([#3102](https://github.com/GenericMappingTools/pygmt/pull/3102))
* pygmt.grdhisteq.compute_bins: Refactor to store output in virtual files instead of temporary files ([#3109](https://github.com/GenericMappingTools/pygmt/pull/3109))
* pygmt.grd2xyz: Improve performance by storing output in virtual files ([#3097](https://github.com/GenericMappingTools/pygmt/pull/3097))
* pygmt.select: Improve performance by storing output in virtual files ([#3108](https://github.com/GenericMappingTools/pygmt/pull/3108))
* pygmt.triangulate.delaunay_triples: Improve performance by storing output in virtual files ([#3107](https://github.com/GenericMappingTools/pygmt/pull/3107))
* pygmt.which: Refactor to get rid of temporary files ([#3148](https://github.com/GenericMappingTools/pygmt/pull/3148))
* Use consistent names (vintbl and vingrd) for input virtual files ([#3082](https://github.com/GenericMappingTools/pygmt/pull/3082))
* Add sequence_to_ctypes_array to convert a sequence to a ctypes array ([#3136](https://github.com/GenericMappingTools/pygmt/pull/3136))
* Add strings_to_ctypes_array to convert a sequence of strings into a ctypes array ([#3137](https://github.com/GenericMappingTools/pygmt/pull/3137))
* Figure.psconvert: Ignore the unrecognized "metadata" parameter added by pytest-mpl v0.17.0 ([#3054](https://github.com/GenericMappingTools/pygmt/pull/3054))
* Remote Datasets: Adjust attributes - remove "title", use default of "name" and "long_name", introduce "description" ([#3048](https://github.com/GenericMappingTools/pygmt/pull/3048))
* Adopt SPEC 0 policy and drop NEP 29 policy ([#3037](https://github.com/GenericMappingTools/pygmt/pull/3037))
* Document the support policy for minimum required GMT versions ([#3070](https://github.com/GenericMappingTools/pygmt/pull/3070))
* Bump to ghostscript 10.03.0 ([#3112](https://github.com/GenericMappingTools/pygmt/pull/3112))
* Bump to ruff 0.3.0 ([#3081](https://github.com/GenericMappingTools/pygmt/pull/3081))
* Enable ruff's PTH (flake8-use-pathlib) rules and fix violations ([#3129](https://github.com/GenericMappingTools/pygmt/pull/3129))
* Change the dev dependency "matplotlib" to "matplotlib-base" to reduce environment size ([#3158](https://github.com/GenericMappingTools/pygmt/pull/3158))
* Migrate from os.path to pathlib ([#3119](https://github.com/GenericMappingTools/pygmt/pull/3119))
* CI: Use "gh release" to upload assets to release ([#3187](https://github.com/GenericMappingTools/pygmt/pull/3187))
* CI: Consistently use github.token instead of secrets.GITHUB_TOKEN ([#3189](https://github.com/GenericMappingTools/pygmt/pull/3189))
* CI: Configure workflows to run on "workflow_dispatch" event ([#3133](https://github.com/GenericMappingTools/pygmt/pull/3133))
* Switch to official GitHub action for managing app tokens ([#3165](https://github.com/GenericMappingTools/pygmt/pull/3165))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.11.0...v0.12.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Michael Grund](https://github.com/michaelgrund)
* [Wei Ji Leong](https://github.com/weiji14)

---

## Release v0.11.0 (2024/02/01)

[![Digital Object Identifier for PyGMT v0.11.0](https://zenodo.org/badge/DOI/10.5281/zenodo.10578540.svg)](https://doi.org/10.5281/zenodo.10578540)

### Highlights

* 🎉 **Eleventh minor release of PyGMT** 🎉
* Tutorial for table inputs ([#2722](https://github.com/GenericMappingTools/pygmt/pull/2722)) and gallery example for choropleth map ([#2796](https://github.com/GenericMappingTools/pygmt/pull/2796))
* Easy access to planetary relief datasets (Mercury, Venus, Moon, Mars, Pluto) ([#3028](https://github.com/GenericMappingTools/pygmt/pull/3028),  [#2906](https://github.com/GenericMappingTools/pygmt/pull/2906), [#2674](https://github.com/GenericMappingTools/pygmt/pull/2674), [#2847](https://github.com/GenericMappingTools/pygmt/pull/2847), [#3027](https://github.com/GenericMappingTools/pygmt/pull/3027))
* Faster PyGMT by ~0.1 seconds for each module call ([#2930](https://github.com/GenericMappingTools/pygmt/pull/2930))

### New Features

* Support timedelta64 dtype as input ([#2884](https://github.com/GenericMappingTools/pygmt/pull/2884))
* Figure.text: Support passing in a list of angle/font/justify values ([#2720](https://github.com/GenericMappingTools/pygmt/pull/2720))
* Figure.savefig: Support saving figures in PPM (.ppm) format ([#2771](https://github.com/GenericMappingTools/pygmt/pull/2771))
* Figure.savefig: Support generating GeoTIFF file (with extension '.tiff') ([#2698](https://github.com/GenericMappingTools/pygmt/pull/2698))
* Figure.savefig: Add the 'worldfile' parameter to write a companion world file for raster images ([#2766](https://github.com/GenericMappingTools/pygmt/pull/2766))

### Enhancements

* geopandas: Correctly handle columns with integer values bigger than the largest 32-bit integer ([#2841](https://github.com/GenericMappingTools/pygmt/pull/2841))
* pyarrow: Support date32[day] and date64[ms] dtypes in pandas objects ([#2845](https://github.com/GenericMappingTools/pygmt/pull/2845))
* datasets.load_tile_map and Figure.tilemap: Add "zoom_adjust" parameter ([#2934](https://github.com/GenericMappingTools/pygmt/pull/2934))
* grdlandmask: Add common alias "cores" for "x" ([#2944](https://github.com/GenericMappingTools/pygmt/pull/2944))
* Figure.coast: Add alias "box" for "-F" ([#2823](https://github.com/GenericMappingTools/pygmt/pull/2823))
* Improve the error messages for unsupported numpy dtypes ([#2856](https://github.com/GenericMappingTools/pygmt/pull/2856))
* Set GMT_SESSION_NAME to a unique name on Windows for multiprocessing support ([#2938](https://github.com/GenericMappingTools/pygmt/pull/2938))
* Figure.savefig: Support .jpeg as JPEG image extension ([#2691](https://github.com/GenericMappingTools/pygmt/pull/2691))
* Figure.savefig: Support uppercase file extensions (e.g., PNG, PDF) ([#2697](https://github.com/GenericMappingTools/pygmt/pull/2697))

### Deprecations

* Rename API function Session.open_virtual_file to Session.open_virtualfile (remove in v0.15.0) ([#2996](https://github.com/GenericMappingTools/pygmt/pull/2996))
* NEP29: Set minimum required version to NumPy 1.23+ ([#2991](https://github.com/GenericMappingTools/pygmt/pull/2991))
* Figure.timestamp: Deprecate parameter 'justification' to 'justify' (remove in v0.13.0) ([#3002](https://github.com/GenericMappingTools/pygmt/pull/3002))
* Figure.grdimage: Remove the unsupported 'img_out'/'A' parameter ([#2907](https://github.com/GenericMappingTools/pygmt/pull/2907))

### Bug Fixes

* pygmt.which: Fix the bug when passing multiple files ([#2726](https://github.com/GenericMappingTools/pygmt/pull/2726))
* pygmt.filter1d: Fix the bug that the first line is read as headers ([#2780](https://github.com/GenericMappingTools/pygmt/pull/2780))
* clib: Fix the bug when passing multiple columns of strings with variable lengths to the GMT C API ([#2719](https://github.com/GenericMappingTools/pygmt/pull/2719))
* Let kwargs_to_strings work with default values and positional arguments ([#2826](https://github.com/GenericMappingTools/pygmt/pull/2826))
* Figure.meca: Fix typo pricipal_axis -> principal_axis ([#2940](https://github.com/GenericMappingTools/pygmt/pull/2940))

### Documentation

* Add gallery example "Scale bar" ([#2822](https://github.com/GenericMappingTools/pygmt/pull/2822))
* Add gallery example for plotting connection lines ("connection" parameter of Figure.plot) ([#2999](https://github.com/GenericMappingTools/pygmt/pull/2999))
* Add gallery example showing how to adjust line segment ends (caps and joints) ([#3015](https://github.com/GenericMappingTools/pygmt/pull/3015))
* Gallery example "Legend": Update regarding input data and multi-column legends ([#2762](https://github.com/GenericMappingTools/pygmt/pull/2762))
* Add the Japanese "PyGMT-HOWTO" tutorial to "External Resources" ([#2743](https://github.com/GenericMappingTools/pygmt/pull/2743))
* Figure.plot: Update docstring for "connection" parameter to GMT 6.5 ([#2994](https://github.com/GenericMappingTools/pygmt/pull/2994))
* Use consistent description for the "outgrid" parameter ([#2874](https://github.com/GenericMappingTools/pygmt/pull/2874))
* Improve the onboarding access checklist for contributors, maintainers and administrators ([#2656](https://github.com/GenericMappingTools/pygmt/pull/2656))
* Recommend Miniforge instead of Mambaforge ([#2833](https://github.com/GenericMappingTools/pygmt/pull/2833))

### Maintenance

* pyarrow: Check compatibility of pyarrow-backed pandas objects with numeric dtypes ([#2774](https://github.com/GenericMappingTools/pygmt/pull/2774))
* Switch away from Stamen basemaps ([#2717](https://github.com/GenericMappingTools/pygmt/pull/2717))
* Add the "validate_output_table_type" function to check the "output_type" parameter ([#2772](https://github.com/GenericMappingTools/pygmt/pull/2772))
* Create "skip_if_no" helper function to skip tests when missing a package ([#2883](https://github.com/GenericMappingTools/pygmt/pull/2883))
* Fix "fixture_xr_image" to open "earth_day_01d" directly with rioxarray ([#2963](https://github.com/GenericMappingTools/pygmt/pull/2963))
* Improve the way to import optional modules ([#2809](https://github.com/GenericMappingTools/pygmt/pull/2809))
* Move variable `__gmt_version__` to pygmt.clib to avoid cyclic-import errors ([#2713](https://github.com/GenericMappingTools/pygmt/pull/2713))
* Refactor the internal "_load_remote_dataset function" to simplify datasets' definitions ([#2917](https://github.com/GenericMappingTools/pygmt/pull/2917))
* Benchmark grdsample, grdfilter and sph2grd with fixed cores ([#2945](https://github.com/GenericMappingTools/pygmt/pull/2945))
* Setup Continuous Benchmarking workflow with pytest-codspeed ([#2908](https://github.com/GenericMappingTools/pygmt/pull/2908))
* Update output shape and mean values from some x2sys_cross tests ([#2986](https://github.com/GenericMappingTools/pygmt/pull/2986))
* Bump the GMT version in CI to 6.5.0 ([#2962](https://github.com/GenericMappingTools/pygmt/pull/2962))
* Bump ghostscript to 10.02.1 ([#2694](https://github.com/GenericMappingTools/pygmt/pull/2694))
* Add support for Python 3.12 ([#2711](https://github.com/GenericMappingTools/pygmt/pull/2711))
* NEP29: Test PyGMT on NumPy 1.26 ([#2692](https://github.com/GenericMappingTools/pygmt/pull/2692))
* CI: Trigger the cache_data workflow in PRs if cache files are added/deleted/updated ([#2939](https://github.com/GenericMappingTools/pygmt/pull/2939))
* CI: Test GMT dev version on Windows by building from source ([#2773](https://github.com/GenericMappingTools/pygmt/pull/2773))
* CI: Set cache-downloads to false to speedup the "Setup Micromamba" step ([#2946](https://github.com/GenericMappingTools/pygmt/pull/2946))
* CI: Run certain GitHub Actions workflows on official repo only ([#2951](https://github.com/GenericMappingTools/pygmt/pull/2951))
* CI: Run benchmarks if PR is labeled with "run/benchmark" ([#2958](https://github.com/GenericMappingTools/pygmt/pull/2958))
* CI: Run "GMT Dev Tests" if PR is labeled with "run/test-gmt-dev" ([#2960](https://github.com/GenericMappingTools/pygmt/pull/2960))
* CI: Require at least one code block separator for example files in the Style Checks workflow ([#2810](https://github.com/GenericMappingTools/pygmt/pull/2810))
* Add Mypy for static type checking ([#2808](https://github.com/GenericMappingTools/pygmt/pull/2808))
* TYP: Improve the doc style for type hints ([#2813](https://github.com/GenericMappingTools/pygmt/pull/2813))
* TYP: Add type hints support for pygmt.datasets.load_sample_data ([#2859](https://github.com/GenericMappingTools/pygmt/pull/2859))
* TYP: Add type hints for the "registration" parameter in pygmt.datasets.load_* functions ([#2867](https://github.com/GenericMappingTools/pygmt/pull/2867))
* TYP: Add type hints for "data_source" in load_earth_relief and load_earth_magnetic_anomaly functions ([#2849](https://github.com/GenericMappingTools/pygmt/pull/2849))
* TYP: Add type hints for parameters of Figure.timestamp([#2890](https://github.com/GenericMappingTools/pygmt/pull/2890))
* TYP: Add type hints for "terminator" in Figure.solar and simplify codes ([#2881](https://github.com/GenericMappingTools/pygmt/pull/2881))
* TYP: Add type hints for parameters of Figure.shift_origin, improve docstrings, and add inline examples ([#2879](https://github.com/GenericMappingTools/pygmt/pull/2879))
* doc: Convert the installation guides source code from ReST to Markdown ([#2992](https://github.com/GenericMappingTools/pygmt/pull/2992))
* doc: Convert overview source code from ReST to Markdown ([#2953](https://github.com/GenericMappingTools/pygmt/pull/2953))
* doc: Move compatibility table from README to separate file ([#2862](https://github.com/GenericMappingTools/pygmt/pull/2862))
* Enable the PDF format documentation in the ReadTheDocs site ([#2876](https://github.com/GenericMappingTools/pygmt/pull/2876))
* Add the full changelog link to the release drafter template ([#2838](https://github.com/GenericMappingTools/pygmt/pull/2838))
* Release Drafter: Automatically replace GitHub handles with names and links ([#2777](https://github.com/GenericMappingTools/pygmt/pull/2777))
* Exclude CODE_OF_CONDUCT.md, AUTHORSHIP.md and pygmt/tests directory from distributions ([#2957](https://github.com/GenericMappingTools/pygmt/pull/2957))
* Add Zenodo's GMT community to the maintainer's onboarding list ([#2761](https://github.com/GenericMappingTools/pygmt/pull/2761))
* Use ruff to lint and format codes, and remove flakeheaven/isort/black/blackdoc ([#2741](https://github.com/GenericMappingTools/pygmt/issues/2741))
* Use codespell to check common misspellings ([#2673](https://github.com/GenericMappingTools/pygmt/pull/2673))
* Use "# %%" as code block separators in examples ([#2662](https://github.com/GenericMappingTools/pygmt/pull/2662))

**Full Changelog**: <https://github.com/GenericMappingTools/pygmt/compare/v0.10.0...v0.11.0>

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Max Jones](https://github.com/maxrjones)

---

## Release v0.10.0 (2023/09/02)

[![Digital Object Identifier for PyGMT v0.10.0](https://zenodo.org/badge/DOI/10.5281/zenodo.8303186.svg)](https://doi.org/10.5281/zenodo.8303186)

### Highlights

* 🎉 **Tenth minor release of PyGMT** 🎉
* Support non-ASCII characters in Figure.text ([#2638](https://github.com/GenericMappingTools/pygmt/pull/2638)) and other method arguments ([#2584](https://github.com/GenericMappingTools/pygmt/pull/2584))
* Three new tutorials and seven new gallery examples

### Enhancements

* Figure.colorbar: Add alias for "Q" ([#2608](https://github.com/GenericMappingTools/pygmt/pull/2608))
* Figure.grdimage: Allow passing RGB xarray.DataArray images ([#2590](https://github.com/GenericMappingTools/pygmt/pull/2590))
* Figure.image: Add alias for "G" ([#2615](https://github.com/GenericMappingTools/pygmt/pull/2615))
* Figure.meca: Add aliases for "L", "T", and "Fr" ([#2546](https://github.com/GenericMappingTools/pygmt/pull/2546))
* clib.Session: Wrap the GMT_Get_Common API function ([#2500](https://github.com/GenericMappingTools/pygmt/pull/2500))
* pygmt.grdfill: Add alias for "N" ([#2618](https://github.com/GenericMappingTools/pygmt/pull/2618))
* pygmt.select: Add aliases for "C", "F", and "L" ([#2466](https://github.com/GenericMappingTools/pygmt/pull/2466))
* pygmt.show_versions: Show versions of IPython and rioxarray ([#2492](https://github.com/GenericMappingTools/pygmt/pull/2492))
* Better handling of optional virtual files (e.g., shading in Figure.grdimage) ([#2493](https://github.com/GenericMappingTools/pygmt/pull/2493))

### Deprecations

* Remove the unused pygmt.test() function ([#2652](https://github.com/GenericMappingTools/pygmt/pull/2652))
* Figure.grdimage: Deprecate parameter "bit_color" to "bitcolor" (remove in v0.12.0) ([#2635](https://github.com/GenericMappingTools/pygmt/pull/2635))
* Figure.text: Remove the deprecated "incols" parameter (deprecated since v0.8.0) ([#2473](https://github.com/GenericMappingTools/pygmt/pull/2473))
* NEP29: Set minimum required version to Python 3.9+ ([#2487](https://github.com/GenericMappingTools/pygmt/pull/2487))
* NEP29: Set minimum required version to NumPy 1.22+ ([#2586](https://github.com/GenericMappingTools/pygmt/pull/2586))

### Bug Fixes

* load_earth_mask: Keep data's encoding to correctly infer data's registration and gtype information ([#2632](https://github.com/GenericMappingTools/pygmt/pull/2632))
* Geopandas integration: Mapping int/int64 to int32 for OGR_GMT format ([#2592](https://github.com/GenericMappingTools/pygmt/pull/2592))
* Figure.meca: Let the "scale" parameter accept int/float/str values ([#2566](https://github.com/GenericMappingTools/pygmt/pull/2566))
* Figure.meca: Fix beachball offsetting for ndarray input (requires GMT>6.4.0) ([#2576](https://github.com/GenericMappingTools/pygmt/pull/2576))

### Documentation

* Document the default CPT for GMT remote datasets ([#2573](https://github.com/GenericMappingTools/pygmt/pull/2573))
* Add tutorial to explain naming of PyGMT figure elements ([#2383](https://github.com/GenericMappingTools/pygmt/pull/2383))
* Add tutorial to show interactive data visualization via `panel` ([#2498](https://github.com/GenericMappingTools/pygmt/pull/2498))
* Add tutorial for cartesian histograms ([#2445](https://github.com/GenericMappingTools/pygmt/pull/2445))
* Add gallery example to show usage of dcw parameter in Figure.coast ([#2428](https://github.com/GenericMappingTools/pygmt/pull/2428))
* Add gallery example to show usage of tile maps ([#2585](https://github.com/GenericMappingTools/pygmt/pull/2585))
* Add gallery example showing how to build an envelope around a curve ([#2587](https://github.com/GenericMappingTools/pygmt/pull/2587))
* Add gallery example for plotting an RGB image from an xarray.DataArray ([#2641](https://github.com/GenericMappingTools/pygmt/pull/2641))
* Add gallery example "Quoted lines" (`style="q"`) ([#2563](https://github.com/GenericMappingTools/pygmt/pull/2563))
* Add gallery example "Decorated lines" (`style="~"`) ([#2564](https://github.com/GenericMappingTools/pygmt/pull/2564))
* Add gallery example "Cross-section along a transect" ([#2515](https://github.com/GenericMappingTools/pygmt/pull/2515))

### Maintenance

* Use substitutions to show the minimum required Python and GMT versions dynamically in installation guides ([#2488](https://github.com/GenericMappingTools/pygmt/pull/2488))
* Use np.asarray to convert a 1-D array to datetime type in array_to_datetime ([#2481](https://github.com/GenericMappingTools/pygmt/pull/2481))
* Use consistent docstrings for test files ([#2578](https://github.com/GenericMappingTools/pygmt/pull/2578))
* Use concurrency to cancel previous runs ([#2589](https://github.com/GenericMappingTools/pygmt/pull/2589))
* Set date_format to ISO8601 to silence pandas 2.0 UserWarning on read_csv ([#2569](https://github.com/GenericMappingTools/pygmt/pull/2569))
* Remove dummy_context and use contextlib.nullcontext instead ([#2491](https://github.com/GenericMappingTools/pygmt/pull/2491))
* NEP29: Test PyGMT on NumPy 1.25 ([#2581](https://github.com/GenericMappingTools/pygmt/pull/2581))
* Fix tests for Aug 2023 updated remote datasets ([#2636](https://github.com/GenericMappingTools/pygmt/pull/2636))
* Figure.meca: Refactor the two tests for offsetting beachballs ([#2572](https://github.com/GenericMappingTools/pygmt/pull/2572))
* Figure.meca: Refactor tests for plotting multiple focal mechanisms ([#2565](https://github.com/GenericMappingTools/pygmt/pull/2565))
* Figure.meca: Refactor tests for plotting a single focal mechanism ([#2533](https://github.com/GenericMappingTools/pygmt/pull/2533))
* Figure.meca: Add a test for passing event names via pandas.DataFrame ([#2582](https://github.com/GenericMappingTools/pygmt/pull/2582))
* Exclude bots from contributors in release drafter ([#2484](https://github.com/GenericMappingTools/pygmt/pull/2484))
* Exclude DVC files from source/binary distributions ([#2634](https://github.com/GenericMappingTools/pygmt/pull/2634))
* CI: Use mamba-org/provision-with-micromamba to setup micromamba ([#2435](https://github.com/GenericMappingTools/pygmt/pull/2435))
* CI: Migrate provision-with-micromamba to setup-micromamba ([#2536](https://github.com/GenericMappingTools/pygmt/pull/2536))
* CI: Run dev tests on scientific Python nightly wheels ([#2612](https://github.com/GenericMappingTools/pygmt/pull/2612))
* CI: Remove the deprecated cml-publish command from the dvc-diff workflow ([#2559](https://github.com/GenericMappingTools/pygmt/pull/2559))
* CI: Fix and simplify the dvc-diff workflow ([#2549](https://github.com/GenericMappingTools/pygmt/pull/2549))
* CI: Add the "Doctests" workflow to run doctests weekly ([#2456](https://github.com/GenericMappingTools/pygmt/pull/2456))
* CI: Add detailed descriptions in the workflow files and update maintainer guides ([#2496](https://github.com/GenericMappingTools/pygmt/pull/2496))
* Add private function _validate_data_input to validate input data ([#2595](https://github.com/GenericMappingTools/pygmt/pull/2595))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Jing-Hui Tong](https://github.com/jhtong33)
* [Max Jones](https://github.com/maxrjones)

---

## Release v0.9.0 (2023/03/31)

[![Digital Object Identifier for PyGMT v0.9.0](https://zenodo.org/badge/DOI/10.5281/zenodo.7772533.svg)](https://doi.org/10.5281/zenodo.7772533)

### Highlights

* 🎉 **Ninth minor release of PyGMT** 🎉
* Add Figure.tilemap to plot XYZ tile maps ([#2394](https://github.com/GenericMappingTools/pygmt/pull/2394))
* Add function to load raster tile maps using contextily ([#2125](https://github.com/GenericMappingTools/pygmt/pull/2125))
* Eleven new/updated gallery and inline examples

### New Features

* Add load_earth_mask function for GSHHG Global Earth Mask dataset ([#2310](https://github.com/GenericMappingTools/pygmt/pull/2310))
* Add Figure.timestamp to plot the GMT timestamp logo ([#2208](https://github.com/GenericMappingTools/pygmt/pull/2208), [#2425](https://github.com/GenericMappingTools/pygmt/pull/2425))

### Enhancements

* pygmt.surface: Add aliases for "C", "L", "M", and "T" ([#2321](https://github.com/GenericMappingTools/pygmt/pull/2321))
* Figure.meca: Add aliases for "C", "E", "G", and "W" ([#2345](https://github.com/GenericMappingTools/pygmt/pull/2345))
* Figure.colorbar: Add aliases for "L" and "Z" ([#2357](https://github.com/GenericMappingTools/pygmt/pull/2357))

### Deprecations

* NEP29: Set minimum required version to NumPy 1.21+ ([#2389](https://github.com/GenericMappingTools/pygmt/pull/2389))
* Recommend Figure.timestamp and remove timestamp (U) alias from all plotting methods ([#2135](https://github.com/GenericMappingTools/pygmt/pull/2135))
* Remove the deprecated load_fractures_compilation function (deprecated since v0.6.0) ([#2303](https://github.com/GenericMappingTools/pygmt/pull/2303))
* Remove the deprecated load_hotspots function (deprecated since v0.6.0) ([#2309](https://github.com/GenericMappingTools/pygmt/pull/2309))
* Remove the deprecated load_japan_quakes function (deprecated since v0.6.0) ([#2301](https://github.com/GenericMappingTools/pygmt/pull/2301))
* Remove the deprecated load_mars_shape function (deprecated since v0.6.0) ([#2304](https://github.com/GenericMappingTools/pygmt/pull/2304))
* Remove the deprecated load_ocean_ridge_points function (deprecated since v0.6.0)  ([#2308](https://github.com/GenericMappingTools/pygmt/pull/2308))
* Remove the deprecated load_sample_bathymetry function (deprecated since v0.6.0) ([#2305](https://github.com/GenericMappingTools/pygmt/pull/2305))
* Remove the deprecated load_usgs_quakes function (deprecated since v0.6.0) ([#2306](https://github.com/GenericMappingTools/pygmt/pull/2306))
* pygmt.grdtrack: Remove the warning about the incorrect parameter order of 'points, grid' (warned since v0.7.0) ([#2312](https://github.com/GenericMappingTools/pygmt/pull/2312))

### Bug Fixes

* GMTDataArrayAccessor: Fallback to default grid registration and gtype if the grid source file doesn't exist ([#2009](https://github.com/GenericMappingTools/pygmt/pull/2009))
* Figure.subplot: Fix setting "sharex", "sharey", and "frame" in combination with Figure.basemap ([#2417](https://github.com/GenericMappingTools/pygmt/pull/2417))
* Figure.subplot: Fix strange positioning issues after exiting subplot ([#2427](https://github.com/GenericMappingTools/pygmt/pull/2427))
* pygmt.config: Correctly reset to default values that contain whitespaces ([#2331](https://github.com/GenericMappingTools/pygmt/pull/2331))
* pygmt.set_display: Do nothing when the display method is set to 'none' ([#2450](https://github.com/GenericMappingTools/pygmt/pull/2450))

### Documentation

* GMTDataArrayAccessor: Add inline examples for setting GMT specific properties ([#2370](https://github.com/GenericMappingTools/pygmt/pull/2370))
* Document limitations of GMT xarray accessors ([#2375](https://github.com/GenericMappingTools/pygmt/pull/2375))
* Revise the notes about registration and gtype of remote datasets ([#2384](https://github.com/GenericMappingTools/pygmt/pull/2384))
* Add project keywords to the pyproject.toml file ([#2315](https://github.com/GenericMappingTools/pygmt/pull/2315))
* Add inline example for colorbar ([#2373](https://github.com/GenericMappingTools/pygmt/pull/2373))
* Add inline example for grdview ([#2381](https://github.com/GenericMappingTools/pygmt/pull/2381))
* Add inline example for load_earth_mask ([#2355](https://github.com/GenericMappingTools/pygmt/pull/2355))
* Add inline example for load_earth_vertical_gravity_gradient ([#2356](https://github.com/GenericMappingTools/pygmt/pull/2356))
* Add inline examples and improve documentation for pygmt.set_display ([#2458](https://github.com/GenericMappingTools/pygmt/pull/2458))
* Add gallery example showing how to use patterns via the "fill" parameter (or similar parameters) ([#2329](https://github.com/GenericMappingTools/pygmt/pull/2329))
* Add gallery example for scatter plot with histograms on sides ([#2410](https://github.com/GenericMappingTools/pygmt/pull/2410))
* Add gallery example showing how to use advanced grdgradient via the "azimuth" & "normalize" parameters ([#2354](https://github.com/GenericMappingTools/pygmt/pull/2354))
* Add gallery example for the Figure.timestamp method ([#2391](https://github.com/GenericMappingTools/pygmt/pull/2391))
* Expand gallery example "Colorbar" for categorical data ([#2395](https://github.com/GenericMappingTools/pygmt/pull/2395))
* Expand gallery example "Focal mechanisms" to use "*fill" and "pen" ([#2433](https://github.com/GenericMappingTools/pygmt/pull/2433))
* Add working example to quickstart section of README ([#2369](https://github.com/GenericMappingTools/pygmt/pull/2369))
* Recommend Mambaforge and mamba in the installation and contributing guides ([#2385](https://github.com/GenericMappingTools/pygmt/pull/2385))

### Maintenance

* Add the GMTSampleData class to simplify the load_sample_data and list_sample_data functions ([#2342](https://github.com/GenericMappingTools/pygmt/pull/2342))
* Add a new target 'doctest' to run doctests only and simplify Makefile ([#2443](https://github.com/GenericMappingTools/pygmt/pull/2443))
* Add a package-level variable `__gmt_version__` for development use ([#2366](https://github.com/GenericMappingTools/pygmt/pull/2366))
* Allow printing show_versions() to in-memory buffer to enable testing ([#2399](https://github.com/GenericMappingTools/pygmt/pull/2399))
* Accept a dict containing configurable GMT parameters in build_arg_string ([#2324](https://github.com/GenericMappingTools/pygmt/pull/2324))
* Publish to TestPyPI and PyPI via OpenID Connect token ([#2453](https://github.com/GenericMappingTools/pygmt/pull/2453))
* Remove --sdist --wheel flags from the build command ([#2420](https://github.com/GenericMappingTools/pygmt/pull/2420))
* Replace ModuleNotFoundError with the more general ImportError ([#2441](https://github.com/GenericMappingTools/pygmt/pull/2441))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Jing-Hui Tong](https://github.com/jhtong33)
* [Max Jones](https://github.com/maxrjones)

---

## Release v0.8.0 (2022/12/30)

[![Digital Object Identifier for PyGMT v0.8.0](https://zenodo.org/badge/DOI/10.5281/zenodo.7481934.svg)](https://doi.org/10.5281/zenodo.7481934)

### Highlights

* 🎉 **Eighth minor release of PyGMT** 🎉
* Added support for tab auto-completion for all GMT default parameters ([#2213](https://github.com/GenericMappingTools/pygmt/pull/2213))
* Created functions to download GMT remote datasets ([#1786](https://github.com/GenericMappingTools/pygmt/issues/1786))
* Wrapped the ternary module ([#1431](https://github.com/GenericMappingTools/pygmt/pull/1431))
* Added an intro tutorial for creating contour maps ([#2126](https://github.com/GenericMappingTools/pygmt/pull/2126))

### New Features

* Add load_earth_free_air_anomaly function for Earth free-air anomaly dataset ([#2238](https://github.com/GenericMappingTools/pygmt/pull/2238))
* Add load_earth_geoid function for Earth Geoid dataset ([#2236](https://github.com/GenericMappingTools/pygmt/pull/2236))
* Add load_earth_magnetic_anomaly function for Earth magnetic anomaly dataset ([#2196](https://github.com/GenericMappingTools/pygmt/pull/2196), [#2239](https://github.com/GenericMappingTools/pygmt/pull/2239), [#2241](https://github.com/GenericMappingTools/pygmt/pull/2241))
* Add load_earth_vertical_gravity_gradient function for Earth vertical gravity gradient dataset ([#2240](https://github.com/GenericMappingTools/pygmt/pull/2240))
* load_earth_relief: Add the support of data sources "gebco" , "gebcosi", and "synbath" ([#1818](https://github.com/GenericMappingTools/pygmt/pull/1818), [#2162](https://github.com/GenericMappingTools/pygmt/pull/2162), [#2192](https://github.com/GenericMappingTools/pygmt/pull/2192), [#2281](https://github.com/GenericMappingTools/pygmt/pull/2281))
* Wrap ternary ([#1431](https://github.com/GenericMappingTools/pygmt/pull/1431))

### Enhancements

* Set gridline (if available) as the default grid registration for remote datasets ([#2266](https://github.com/GenericMappingTools/pygmt/pull/2266))
* Add ternary sample dataset ([#2211](https://github.com/GenericMappingTools/pygmt/pull/2211))
* Figure.ternary: Add parameters "alabel", "blabel", and "clabel" ([#2139](https://github.com/GenericMappingTools/pygmt/pull/2139))
* Figure.psconvert: Add a new alias "gs_path" (-G) ([#2076](https://github.com/GenericMappingTools/pygmt/pull/2076))
* Figure.psconvert: Check if the given prefix is valid ([#2170](https://github.com/GenericMappingTools/pygmt/pull/2170))
* Figure.savefig: Raise a FileNotFoundError if the parent directory doesn't exist ([#2160](https://github.com/GenericMappingTools/pygmt/pull/2160))
* Figure.show: Allow keyword arguments passed to Figure.psconvert ([#2078](https://github.com/GenericMappingTools/pygmt/pull/2078))
* pygmt.config: Support tab auto-completion for all GMT defaults ([#2213](https://github.com/GenericMappingTools/pygmt/pull/2213))
* Rewrite the meca function to support offsetting and labeling beachballs ([#1784](https://github.com/GenericMappingTools/pygmt/pull/1784))

### Deprecations

* Deprecate xshift (X) and yshift (Y) aliases from all plotting modules (remove in v0.12.0) ([#2071](https://github.com/GenericMappingTools/pygmt/pull/2071))
* Figure.plot: Deprecate parameter "color" to "fill" (remove in v0.12.0) ([#2177](https://github.com/GenericMappingTools/pygmt/pull/2177))
* Figure.plot3d: Deprecate parameter "color" to "fill" (remove in v0.12.0) ([#2178](https://github.com/GenericMappingTools/pygmt/pull/2178))
* Figure.rose: Deprecate parameter color to fill (remove in v0.12.0) ([#2181](https://github.com/GenericMappingTools/pygmt/pull/2181))
* Figure.velo: Deprecate parameters "color" to "fill" and "uncertaintycolor" to "uncertaintyfill" (remove in v0.12.0) ([#2206](https://github.com/GenericMappingTools/pygmt/pull/2206))
* Figure.wiggle: Deprecate parameter "color" (remove in v0.12.0) and add "fillpositive"/"fillnegative" ([#2205](https://github.com/GenericMappingTools/pygmt/pull/2205))
* Figure.psconvert: Remove the deprecated parameter "icc_gray" (deprecated since v0.6.0) ([#2267](https://github.com/GenericMappingTools/pygmt/pull/2267))
* Figure.text: Deprecate parameter "incols" to "use_word" (remove in v0.10.0)  ([#1964](https://github.com/GenericMappingTools/pygmt/pull/1964))

### Bug Fixes

* Figure.meca: Fix line and circle of offset parameter for dict/pandas input  ([#2226](https://github.com/GenericMappingTools/pygmt/pull/2226))
* Figure.meca: Fix beachball offsetting with dict/pandas inputs ([#2202](https://github.com/GenericMappingTools/pygmt/pull/2202))
* Figure.meca: Fix the bug when passing a dict of scalar values to the spec parameter ([#2174](https://github.com/GenericMappingTools/pygmt/pull/2174))
* Figure.ternary: Fix the crash for pd.DataFrame input with GMT 6.3.0-6.4.0 ([#2274](https://github.com/GenericMappingTools/pygmt/pull/2274))

### Documentation

* Add intro tutorial section for creating contour map ([#2126](https://github.com/GenericMappingTools/pygmt/pull/2126))
* Add gallery example for Figure.ternary method ([#2138](https://github.com/GenericMappingTools/pygmt/pull/2138))
* Add gallery example showing the usage of vertical and horizontal bars ([#1521](https://github.com/GenericMappingTools/pygmt/pull/1521))
* Add inline example for coast ([#2142](https://github.com/GenericMappingTools/pygmt/pull/2142))
* Add inline example for grdcontour ([#2148](https://github.com/GenericMappingTools/pygmt/pull/2148))
* Add inline example for grdimage ([#2146](https://github.com/GenericMappingTools/pygmt/pull/2146))
* Add inline example for grd2cpt ([#2145](https://github.com/GenericMappingTools/pygmt/pull/2145))
* Add inline example for solar ([#2147](https://github.com/GenericMappingTools/pygmt/pull/2147))
* Add SciPy 2022 talk to presentations ([#2053](https://github.com/GenericMappingTools/pygmt/pull/2053))
* Add instructions to install pygmt kernel for Jupyter users ([#2153](https://github.com/GenericMappingTools/pygmt/pull/2153))
* Improve instructions about setting GMT_LIBRARY_PATH env variable ([#2136](https://github.com/GenericMappingTools/pygmt/pull/2136))
* Add badges for conda package version, license, and twitter ([#2081](https://github.com/GenericMappingTools/pygmt/pull/2081))
* Add PyOpenSci peer reviewed badge to main README ([#2112](https://github.com/GenericMappingTools/pygmt/pull/2112))

### Maintenance

* Add an internal function to load GMT remote datasets ([#2200](https://github.com/GenericMappingTools/pygmt/pull/2200))
* Add support for Python 3.11 ([#2172](https://github.com/GenericMappingTools/pygmt/pull/2172))
* NEP29: Test PyGMT on NumPy 1.24 ([#2256](https://github.com/GenericMappingTools/pygmt/pull/2256))
* NEP29: Test PyGMT on NumPy 1.23 and 1.21 ([#2057](https://github.com/GenericMappingTools/pygmt/pull/2057))
* Bump the GMT version in CI to 6.4.0 ([#1990](https://github.com/GenericMappingTools/pygmt/pull/1990))
* Update baseline images for GMT 6.4.0 ([#1883](https://github.com/GenericMappingTools/pygmt/pull/1883))
* Migrate Continuous Documentation from Vercel to Readthedocs ([#1859](https://github.com/GenericMappingTools/pygmt/pull/1859))
* Set nested_sections to False for Sphinx-Gallery 0.11.0 regarding a correct navgation bar ([#2046](https://github.com/GenericMappingTools/pygmt/pull/2046))
* Convert bug report, feature, and module request issue templates into yaml configured forms ([#2091](https://github.com/GenericMappingTools/pygmt/pull/2091), [#2214](https://github.com/GenericMappingTools/pygmt/pull/2214), [#2216](https://github.com/GenericMappingTools/pygmt/pull/2216))
* doc: Set different html_baseurl for stable and dev versions ([#2158](https://github.com/GenericMappingTools/pygmt/pull/2158))
* Update the instructions for checking README syntax ([#2265](https://github.com/GenericMappingTools/pygmt/pull/2265))
* Use longname placeholders in the docstrings for common options ([#1932](https://github.com/GenericMappingTools/pygmt/pull/1932))
* Add optional dependencies to pyproject.toml ([#2069](https://github.com/GenericMappingTools/pygmt/pull/2069))
* Migrate project metadata from setup.py to pyproject.toml following PEP621 ([#1848](https://github.com/GenericMappingTools/pygmt/pull/1848))
* Move blackdoc options to pyproject.toml ([#2093](https://github.com/GenericMappingTools/pygmt/pull/2093))
* Move docformatter options from Makefile to pyproject.toml ([#2072](https://github.com/GenericMappingTools/pygmt/pull/2072))
* Replace flake8 with flakeheaven ([#1847](https://github.com/GenericMappingTools/pygmt/pull/1847))
* Add a workflow and Makefile target to test old GMT versions every Tuesday ([#2079](https://github.com/GenericMappingTools/pygmt/pull/2079))
* Check if a module outputs to a temporary file using "Path().stat().st_size > 0" ([#2224](https://github.com/GenericMappingTools/pygmt/pull/2224))
* pygmt.show_versions: Show GMT binary version and hide the Python interpreter path ([#1838](https://github.com/GenericMappingTools/pygmt/pull/1838))
* Refactor grdview and grdimage to use virtualfile_from_data ([#1988](https://github.com/GenericMappingTools/pygmt/pull/1988))
* Use the org-wide code of conduct ([#2020](https://github.com/GenericMappingTools/pygmt/pull/2020))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Michael Grund](https://github.com/michaelgrund)
* [Wei Ji Leong](https://github.com/weiji14)
* [Max Jones](https://github.com/maxrjones)

---

## Release v0.7.0 (2022/07/01)

[![Digital Object Identifier for PyGMT v0.7.0](https://zenodo.org/badge/DOI/10.5281/zenodo.6702566.svg)](https://doi.org/10.5281/zenodo.6702566)

### Highlights

* 🎉 **Seventh minor release of PyGMT** 🎉
* Wrapped 3 GMT modules
* Added two new PyGMT tutorials and EGU 2022 short course to external resources page ([#1971](https://github.com/GenericMappingTools/pygmt/pull/1971) and [#1935](https://github.com/GenericMappingTools/pygmt/pull/1935))

### New Features

* Wrap binstats ([#1652](https://github.com/GenericMappingTools/pygmt/pull/1652))
* Wrap filter1d ([#1512](https://github.com/GenericMappingTools/pygmt/pull/1512))
* Wrap dimfilter ([#1492](https://github.com/GenericMappingTools/pygmt/pull/1492))

### Enhancements

* Support passing data in NumPy int8, int16, uint8 and uint16 dtypes to GMT ([#1963](https://github.com/GenericMappingTools/pygmt/pull/1963))
* inset: Add region and projection aliases and fix two examples ([#1931](https://github.com/GenericMappingTools/pygmt/pull/1931))
* basemap: Plotting frames if required parameters are not given ([#1909](https://github.com/GenericMappingTools/pygmt/pull/1909))
* basemap: Added box alias for F ([#1894](https://github.com/GenericMappingTools/pygmt/pull/1894))
* Add a sample dataset maunaLoa_co2 ([#1961](https://github.com/GenericMappingTools/pygmt/pull/1961))
* Add a sample dataset notre_dame_topography ([#1920](https://github.com/GenericMappingTools/pygmt/pull/1920))
* Add a sample dataset earth_relief_holes ([#1921](https://github.com/GenericMappingTools/pygmt/pull/1921))

### Deprecations

* NEP29: Set minimum required version to NumPy 1.20+ ([#1985](https://github.com/GenericMappingTools/pygmt/pull/1985))
* Figure.wiggle: Remove parameter 'columns', use 'incols' instead. ([#1977](https://github.com/GenericMappingTools/pygmt/pull/1977))
* Figure.histogram and pygmt.info: Remove parameter 'table', use 'data' instead ([#1975](https://github.com/GenericMappingTools/pygmt/pull/1975))
* pygmt.surface: Remove parameter 'outfile', use 'outgrid' instead ([#1976](https://github.com/GenericMappingTools/pygmt/pull/1976))
* blockm/contour/plot/plot3d/rose/surface/wiggle: Change the parameter order of data array and input arrays ([#1978](https://github.com/GenericMappingTools/pygmt/pull/1978))

### Bug Fixes

* grdtrack: Fix the bug when profile is given ([#1867](https://github.com/GenericMappingTools/pygmt/pull/1867))
* Fix the grid accessor (grid registration and type) for 3D grids ([#1913](https://github.com/GenericMappingTools/pygmt/pull/1913))

### Documentation

* Add instructions to install PyGMT using mamba ([#1967](https://github.com/GenericMappingTools/pygmt/pull/1967))
* Improve two gallery examples regarding categorical colormaps ([#1934](https://github.com/GenericMappingTools/pygmt/pull/1934))
* Add inline example to dimfilter ([#1956](https://github.com/GenericMappingTools/pygmt/pull/1956))
* Add inline example to surface ([#1953](https://github.com/GenericMappingTools/pygmt/pull/1953))
* Add inline example to grdfill ([#1954](https://github.com/GenericMappingTools/pygmt/pull/1954))
* Add inline code examples to contributing guidelines ([#1924](https://github.com/GenericMappingTools/pygmt/pull/1924))
* Add thumbnail images to the external resources page ([#1941](https://github.com/GenericMappingTools/pygmt/pull/1941))
* Redesign the team gallery using sphinx-design's card directive ([#1937](https://github.com/GenericMappingTools/pygmt/pull/1937))

### Maintenance

* Fix broken 'Improve this page' links using sphinx variable page_source_suffix ([#1969](https://github.com/GenericMappingTools/pygmt/pull/1969))
* Split up functions for loading datasets ([#1955](https://github.com/GenericMappingTools/pygmt/pull/1955))
* Set setuptools_scm fallback_version to follow  PEP440 ([#1945](https://github.com/GenericMappingTools/pygmt/pull/1945))
* Refactor text to use virtualfile_from_data ([#1121](https://github.com/GenericMappingTools/pygmt/pull/1121))
* Run full tests only on Wednesday scheduled jobs ([#1833](https://github.com/GenericMappingTools/pygmt/pull/1833))
* Run GMT Dev Tests on Monday, Wednesday and Friday only ([#1922](https://github.com/GenericMappingTools/pygmt/pull/1922))
* Update GMT Dev Tests workflow to test on macOS-12 and ubuntu-22.04 ([#1918](https://github.com/GenericMappingTools/pygmt/pull/1918))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Wei Ji Leong](https://github.com/weiji14)
* [Andre L. Belem](https://github.com/andrebelem)
* [Yvonne Fröhlich](https://github.com/yvonnefroehlich)
* [Max Jones](https://github.com/maxrjones)
* [Jack Beagley](https://github.com/jackbeagley)
* [Michael Grund](https://github.com/michaelgrund)

---

## Release v0.6.1 (2022/04/11)

[![Digital Object Identifier for PyGMT v0.6.1](https://zenodo.org/badge/DOI/10.5281/zenodo.6426493.svg)](https://doi.org/10.5281/zenodo.6426493)

### Highlights

* Patch release which allows passing None explicitly to pygmt functions ([#1872](https://github.com/GenericMappingTools/pygmt/pull/1872), [#1862](https://github.com/GenericMappingTools/pygmt/pull/1862), [#1857](https://github.com/GenericMappingTools/pygmt/pull/1857), [#1815](https://github.com/GenericMappingTools/pygmt/pull/1815))
* A new tutorial for grdhisteq ([#1821](https://github.com/GenericMappingTools/pygmt/pull/1821))

### Bug Fixes

* Fix pathlib support for plot and plot3d ([#1831](https://github.com/GenericMappingTools/pygmt/pull/1831))

### Documentation

* Add inline example for grdvolume ([#1726](https://github.com/GenericMappingTools/pygmt/pull/1726))
* Format author affiliations in CITATION.cff and AUTHORS.md ([#1844](https://github.com/GenericMappingTools/pygmt/pull/1844))

### Maintenance

* NEP29: Run PyGMT tests and docs build on Python 3.10 ([#1868](https://github.com/GenericMappingTools/pygmt/pull/1868))
* Let pygmt.show_versions() report geopandas version ([#1846](https://github.com/GenericMappingTools/pygmt/pull/1846))
* Refactor build_arg_string to also deal with infile and outfile ([#1837](https://github.com/GenericMappingTools/pygmt/pull/1837))
* Migrate build system settings to pyproject.toml following pep517 and pep518 ([#1845](https://github.com/GenericMappingTools/pygmt/pull/1845))
* Use the build package to build sdist and wheel distributions ([#1823](https://github.com/GenericMappingTools/pygmt/pull/1823))
* Let slash command /test-gmt-dev report job URL ([#1866](https://github.com/GenericMappingTools/pygmt/pull/1866))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Max Jones](https://github.com/maxrjones)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Will Schlitzer](https://github.com/willschlitzer)

---

## Release v0.6.0 (2022/03/14)

[![Digital Object Identifier for PyGMT v0.6.0](https://zenodo.org/badge/DOI/10.5281/zenodo.6349217.svg)](https://doi.org/10.5281/zenodo.6349217)

### Highlights

* 🎉 **Sixth minor release of PyGMT** 🎉
* New inline examples for 14 functions!
* Single `pygmt.datasets.load_sample_data` function for loading any sample dataset ([#1685](https://github.com/GenericMappingTools/pygmt/pull/1685))
* Minimum required GMT version is now 6.3.0 ([#1649](https://github.com/GenericMappingTools/pygmt/pull/1649))

### New Features

* Wrap triangulate ([#731](https://github.com/GenericMappingTools/pygmt/pull/731))
* Wrap grdhisteq ([#1433](https://github.com/GenericMappingTools/pygmt/pull/1433))

### Enhancements

* Add alias for blockmean's -S parameter ([#1601](https://github.com/GenericMappingTools/pygmt/pull/1601))
* Allow users to set the waiting time when displaying a preview image using an external viewer ([#1618](https://github.com/GenericMappingTools/pygmt/pull/1618))
* Raise an exception if the given parameter is not recognized and is longer than 2 characters ([#1792](https://github.com/GenericMappingTools/pygmt/pull/1792))

### Deprecations

* Figure.plot/plot3d: Remove parameter "sizes", use "size" instead ([#1809](https://github.com/GenericMappingTools/pygmt/pull/1809))
* Figure.contour/plot/plot3d/rose: Remove parameter "columns", use "incols" instead ([#1806](https://github.com/GenericMappingTools/pygmt/pull/1806))
* Figure.psconvert: Add new aliases and deprecate parameter "icc_gray" (remove in v0.8.0) ([#1673](https://github.com/GenericMappingTools/pygmt/pull/1673))
* NEP29: Set minimum required version to Python 3.8+ ([#1676](https://github.com/GenericMappingTools/pygmt/pull/1676))
* NEP29: Set minimum required version to NumPy 1.19+ ([#1675](https://github.com/GenericMappingTools/pygmt/pull/1675))

### Bug Fixes

* Allow passing arguments containing spaces into pygmt functions ([#1487](https://github.com/GenericMappingTools/pygmt/pull/1487))
* Fix the spacing parameter processing for many modules ([#1805](https://github.com/GenericMappingTools/pygmt/pull/1805))
* Fix missing gcmt convention keys in pygmt.meca ([#1611](https://github.com/GenericMappingTools/pygmt/pull/1611))
* Fix the spacing parameter and check required parameters in xyz2grd ([#1804](https://github.com/GenericMappingTools/pygmt/pull/1804))
* Fix UnicodeDecodeError with shapefiles for plot and plot3d ([#1695](https://github.com/GenericMappingTools/pygmt/pull/1695))

### Documentation

* Add a shorter video introduction to the home page ([#1769](https://github.com/GenericMappingTools/pygmt/pull/1769))
* Add Liam's 2021 ROSES video to learning resources ([#1760](https://github.com/GenericMappingTools/pygmt/pull/1760))
* Add quick conda install instructions in main README ([#1717](https://github.com/GenericMappingTools/pygmt/pull/1717))
* Add instructions for reporting upstream bugs to contributing.md ([#1610](https://github.com/GenericMappingTools/pygmt/pull/1610))
* List key development dependencies to install for new contributors ([#1783](https://github.com/GenericMappingTools/pygmt/pull/1783))
* Update Code of Conduct to v2.1 ([#1754](https://github.com/GenericMappingTools/pygmt/pull/1754))
* Update the contributing guide about pushing changes to dvc and git ([#1776](https://github.com/GenericMappingTools/pygmt/pull/1776))
* Update dataset links to the new remote-datasets site ([#1785](https://github.com/GenericMappingTools/pygmt/pull/1785))
* Add more sections to the API docs ([#1643](https://github.com/GenericMappingTools/pygmt/pull/1643))
* Add an "add a title" to starter tutorial ([#1688](https://github.com/GenericMappingTools/pygmt/pull/1688))
* Reorganize tutorial section in the documentation sidebar ([#1603](https://github.com/GenericMappingTools/pygmt/pull/1603))
* Update the starter tutorial introduction ([#1607](https://github.com/GenericMappingTools/pygmt/pull/1607))
* Add gallery example to showcase blockmean ([#1598](https://github.com/GenericMappingTools/pygmt/pull/1598))
* Add gallery example to showcase project ([#1696](https://github.com/GenericMappingTools/pygmt/pull/1696))
* Update text symbol gallery example ([#1648](https://github.com/GenericMappingTools/pygmt/pull/1648))
* Add inline example for blockmean ([#1729](https://github.com/GenericMappingTools/pygmt/pull/1729))
* Add inline example for blockmedian ([#1730](https://github.com/GenericMappingTools/pygmt/pull/1730))
* Add inline example for blockmode ([#1731](https://github.com/GenericMappingTools/pygmt/pull/1731))
* Add inline example for grd2xyz ([#1713](https://github.com/GenericMappingTools/pygmt/pull/1713))
* Add inline example for grdclip ([#1711](https://github.com/GenericMappingTools/pygmt/pull/1711))
* Add inline example for grdcut ([#1689](https://github.com/GenericMappingTools/pygmt/pull/1689))
* Add inline example for grdgradient ([#1720](https://github.com/GenericMappingTools/pygmt/pull/1720))
* Add inline example for grdlandmask ([#1721](https://github.com/GenericMappingTools/pygmt/pull/1721))
* Add inline example for grdproject ([#1722](https://github.com/GenericMappingTools/pygmt/pull/1722))
* Add inline example for grdsample ([#1724](https://github.com/GenericMappingTools/pygmt/pull/1724))
* Add inline example for grdtrack ([#1725](https://github.com/GenericMappingTools/pygmt/pull/1725))
* Add inline example for select ([#1756](https://github.com/GenericMappingTools/pygmt/pull/1756))
* Add inline example for sph2grd ([#1718](https://github.com/GenericMappingTools/pygmt/pull/1718))
* Add inline example for xyz2grd ([#1719](https://github.com/GenericMappingTools/pygmt/pull/1719))

### Maintenance

* Add a test to make sure the incols parameter works for pandas.DataFrame ([#1771](https://github.com/GenericMappingTools/pygmt/pull/1771))
* Add load_static_earth_relief function for internal testing ([#1727](https://github.com/GenericMappingTools/pygmt/pull/1727))
* Migrate pylint settings from .pylintrc to pyproject.toml ([#1755](https://github.com/GenericMappingTools/pygmt/pull/1755))
* NEP29: Test PyGMT on NumPy 1.22 ([#1701](https://github.com/GenericMappingTools/pygmt/pull/1701))
* Replace pkg_resources with importlib.metadata ([#1674](https://github.com/GenericMappingTools/pygmt/pull/1674))
* Update deprecated -g common option syntax ([#1670](https://github.com/GenericMappingTools/pygmt/pull/1670))
* Update deprecated -JG syntax ([#1659](https://github.com/GenericMappingTools/pygmt/pull/1659))
* Use pytest-doctestplus to skip some inline doctests ([#1790](https://github.com/GenericMappingTools/pygmt/pull/1790))
* Use Python 3.10 in Continuous Integration tests ([#1577](https://github.com/GenericMappingTools/pygmt/pull/1577))

### Contributors

* [Will Schlitzer](https://github.com/willschlitzer)
* [Max Jones](https://github.com/maxrjones)
* [Dongdong Tian](https://github.com/seisman)
* [Michael Grund](https://github.com/michaelgrund)
* [Wei Ji Leong](https://github.com/weiji14)
* [Julius Busecke](https://github.com/jbusecke)

---

## Release v0.5.0 (2021/10/29)

[![Digital Object Identifier for PyGMT v0.5.0](https://zenodo.org/badge/DOI/10.5281/zenodo.5607255.svg)](https://doi.org/10.5281/zenodo.5607255)

### Highlights

* 🎉 **Fifth minor release of PyGMT** 🎉
* Wrapped 12 GMT modules
* Standardized and reorder table inputs to be 'data, x, y, z' across functions ([#1479](https://github.com/GenericMappingTools/pygmt/pull/1479))
* Added a gallery example showing usage of line objects from a geopandas.GeoDataFrame ([#1474](https://github.com/GenericMappingTools/pygmt/pull/1474))

### New Features

* Wrap blockmode ([#1456](https://github.com/GenericMappingTools/pygmt/pull/1456))
* Wrap gmtselect ([#1429](https://github.com/GenericMappingTools/pygmt/pull/1429))
* Wrap grd2xyz ([#1284](https://github.com/GenericMappingTools/pygmt/pull/1284))
* Wrap grdproject ([#1377](https://github.com/GenericMappingTools/pygmt/pull/1377))
* Wrap grdsample ([#1380](https://github.com/GenericMappingTools/pygmt/pull/1380))
* Wrap grdvolume ([#1299](https://github.com/GenericMappingTools/pygmt/pull/1299))
* Wrap nearneighbor ([#1379](https://github.com/GenericMappingTools/pygmt/pull/1379))
* Wrap project ([#1122](https://github.com/GenericMappingTools/pygmt/pull/1122))
* Wrap sph2grd ([#1434](https://github.com/GenericMappingTools/pygmt/pull/1434))
* Wrap sphdistance ([#1383](https://github.com/GenericMappingTools/pygmt/pull/1383))
* Wrap sphinterpolate ([#1418](https://github.com/GenericMappingTools/pygmt/pull/1418))
* Wrap xyz2grd ([#636](https://github.com/GenericMappingTools/pygmt/pull/636))
* Add function to import seafloor crustal age dataset ([#1471](https://github.com/GenericMappingTools/pygmt/pull/1471))
* Add pygmt.load_dataarray function ([#1439](https://github.com/GenericMappingTools/pygmt/pull/1439))

### Enhancements

* Expand table-like input options for Figure.contour ([#1531](https://github.com/GenericMappingTools/pygmt/pull/1531))
* Expand table-like input options for pygmt.surface ([#1455](https://github.com/GenericMappingTools/pygmt/pull/1455))
* Raise GMTInvalidInput exception when required z is missing ([#1478](https://github.com/GenericMappingTools/pygmt/pull/1478))
* Add support for passing pathlib.Path objects as filenames ([#1382](https://github.com/GenericMappingTools/pygmt/pull/1382))
* Allow passing a list to the 'incols' parameter for blockm, grdtrack and text ([#1475](https://github.com/GenericMappingTools/pygmt/pull/1475))
* Plot square or cube by default for OGR/GMT files with Point/MultiPoint types ([#1438](https://github.com/GenericMappingTools/pygmt/pull/1438))
* Plot square or cube by default for geopandas Point/MultiPoint types ([#1405](https://github.com/GenericMappingTools/pygmt/pull/1405))
* Add area_thresh to COMMON_OPTIONS ([#1426](https://github.com/GenericMappingTools/pygmt/pull/1426))
* Add function to import Mars dataset ([#1420](https://github.com/GenericMappingTools/pygmt/pull/1420))
* Add function to import hotspot dataset ([#1386](https://github.com/GenericMappingTools/pygmt/pull/1386))

### Deprecations

* pygmt.blockm*: Reorder input parameters to 'data, x, y, z' ([#1565](https://github.com/GenericMappingTools/pygmt/pull/1565))
* pygmt.surface: Reorder input parameters to 'data, x, y, z' ([#1562](https://github.com/GenericMappingTools/pygmt/pull/1562))
* Figure.contour: Reorder input parameters to 'data, x, y, z' ([#1561](https://github.com/GenericMappingTools/pygmt/pull/1561))
* Figure.plot3d: Reorder input parameters to 'data, x, y, z' ([#1560](https://github.com/GenericMappingTools/pygmt/pull/1560))
* Figure.plot: Reorder input parameters to "data, x, y" ([#1547](https://github.com/GenericMappingTools/pygmt/pull/1547))
* Figure.rose: Reorder input parameters to 'data, length, azimuth' ([#1546](https://github.com/GenericMappingTools/pygmt/pull/1546))
* Figure.wiggle: Reorder input parameter to 'data, x, y, z' ([#1548](https://github.com/GenericMappingTools/pygmt/pull/1548))
* Figure.histogram: Deprecate parameter "table" to "data" (remove in v0.7.0) ([#1540](https://github.com/GenericMappingTools/pygmt/pull/1540))
* pygmt.info: Deprecate parameter "table" to "data" (remove in v0.7.0) ([#1538](https://github.com/GenericMappingTools/pygmt/pull/1538))
* Figure.wiggle: Deprecate parameter "columns" to "incols" (remove in v0.7.0) ([#1504](https://github.com/GenericMappingTools/pygmt/pull/1504))
* pygmt.surface: Deprecate parameter "outfile" to "outgrid" (remove in v0.7.0) ([#1458](https://github.com/GenericMappingTools/pygmt/pull/1458))
* NEP29: Set minimum required version to NumPy 1.18+ ([#1430](https://github.com/GenericMappingTools/pygmt/pull/1430))

### Bug Fixes

* Allow GMTDataArrayAccessor to work on sliced datacubes ([#1581](https://github.com/GenericMappingTools/pygmt/pull/1581))
* Allow non-string color when input data is a matrix or a file for plot and plot3d ([#1526](https://github.com/GenericMappingTools/pygmt/pull/1526))
* Raise RuntimeWarning instead of an exception for irregular grid spacing ([#1530](https://github.com/GenericMappingTools/pygmt/pull/1530))
* Raise an error for zero increment grid ([#1484](https://github.com/GenericMappingTools/pygmt/pull/1484))

### Documentation

* Add CITATION.cff file for PyGMT ([#1592](https://github.com/GenericMappingTools/pygmt/pull/1592))
* Update region and projection standard docstrings ([#1510](https://github.com/GenericMappingTools/pygmt/pull/1510))
* Document gmtwhich -Ga option to download to appropriate cache folder ([#1554](https://github.com/GenericMappingTools/pygmt/pull/1554))
* Add gallery example showing the usage of text symbols ([#1522](https://github.com/GenericMappingTools/pygmt/pull/1522))
* Add gallery example for grdgradient ([#1428](https://github.com/GenericMappingTools/pygmt/pull/1428))
* Add gallery example for grdlandmask ([#1469](https://github.com/GenericMappingTools/pygmt/pull/1469))
* Add missing aliases to pygmt.grdgradient ([#1515](https://github.com/GenericMappingTools/pygmt/pull/1515))
* Add missing aliases to pygmt.sphdistance ([#1516](https://github.com/GenericMappingTools/pygmt/pull/1516))
* Add missing aliases to pygmt.blockmean and pygmt.blockmedian ([#1500](https://github.com/GenericMappingTools/pygmt/pull/1500))
* Add missing aliases to pygmt.Figure.wiggle ([#1498](https://github.com/GenericMappingTools/pygmt/pull/1498))
* Add missing aliases to pygmt.Figure.velo ([#1497](https://github.com/GenericMappingTools/pygmt/pull/1497))
* Add missing aliases to pygmt.surface ([#1501](https://github.com/GenericMappingTools/pygmt/pull/1501))
* Add missing aliases to pygmt.Figure.plot3d ([#1503](https://github.com/GenericMappingTools/pygmt/pull/1503))
* Add missing aliases to pygmt.grdlandmask ([#1423](https://github.com/GenericMappingTools/pygmt/pull/1423))
* Add missing aliases to pygmt.grdtrack ([#1499](https://github.com/GenericMappingTools/pygmt/pull/1499))
* Add missing aliases to pygmt.Figure.plot ([#1502](https://github.com/GenericMappingTools/pygmt/pull/1502))
* Add missing aliases to pygmt.Figure.text ([#1448](https://github.com/GenericMappingTools/pygmt/pull/1448))
* Add missing aliases to pygmt.Figure.histogram ([#1451](https://github.com/GenericMappingTools/pygmt/pull/1451))
* Add missing alias to pygmt.Figure.legend ([#1453](https://github.com/GenericMappingTools/pygmt/pull/1453))
* Add missing aliases to pygmt.Figure.rose ([#1452](https://github.com/GenericMappingTools/pygmt/pull/1452))
* Add missing alias to pygmt.Figure.grdview ([#1450](https://github.com/GenericMappingTools/pygmt/pull/1450))
* Add missing aliases to pygmt.Figure.image.py ([#1449](https://github.com/GenericMappingTools/pygmt/pull/1449))
* Add missing common options to contour ([#1446](https://github.com/GenericMappingTools/pygmt/pull/1446))
* Add missing 'incols' alias to info ([#1476](https://github.com/GenericMappingTools/pygmt/pull/1476))

### Maintenance

* Add support for Python 3.10 ([#1591](https://github.com/GenericMappingTools/pygmt/pull/1591))
* Make IPython partially optional on CI to increase test coverage of figure.py ([#1496](https://github.com/GenericMappingTools/pygmt/pull/1496))
* Use mamba to install Continuous Integration dependencies ([#841](https://github.com/GenericMappingTools/pygmt/pull/841))
* Remove deprecated codecov dependency from CI ([#1494](https://github.com/GenericMappingTools/pygmt/pull/1494))
* Add the use of Flake8 to check examples and fix warnings ([#1477](https://github.com/GenericMappingTools/pygmt/pull/1477))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Michael Grund](https://github.com/michaelgrund)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Wei Ji Leong](https://github.com/weiji14)
* [Max Jones](https://github.com/maxrjones)
* [Yohai Magen](https://github.com/yohaimagen)
* [Amanda Leaman](https://github.com/arleaman)
* [@daroari](https://github.com/daroari)
* [@obaney](https://github.com/obaney)
* [@srijac](https://github.com/srijac)
* [Andrés Ignacio Torres](https://github.com/aitorres)
* [Becky Salvage](https://github.com/BeckySalvage)
* [Claudio Satriano](https://github.com/claudiodsf)
* [Jamie J Quinn](https://github.com/JamieJQuinn)
* [@carocamargo](https://github.com/carocamargo)

----

## Release v0.4.1 (2021/08/07)

[![Digital Object Identifier for PyGMT v0.4.1](https://zenodo.org/badge/DOI/10.5281/zenodo.5162003.svg)](https://doi.org/10.5281/zenodo.5162003)

### Highlights

* 🎉 **Patch release with multiple gallery examples** 🎉
* Change default GitHub branch name from "master" to "main" to increase inclusivity ([#1360](https://github.com/GenericMappingTools/pygmt/pull/1360))
* Add a "[PyGMT Team](https://www.pygmt.org/latest/team.html)" page ([#1308](https://github.com/GenericMappingTools/pygmt/pull/1308))

### Enhancements

* Add common alias "verbose" (V) to grdlandmask and savefig ([#1343](https://github.com/GenericMappingTools/pygmt/pull/1343))

### Bug Fixes

* Change invalid input conditions in grdtrack ([#1376](https://github.com/GenericMappingTools/pygmt/pull/1376))
* Fix bug so that x2sys_cross accepts dataframes with NaN values ([#1369](https://github.com/GenericMappingTools/pygmt/pull/1369))

### Documentation

* Combine documentation and compatibility sections in README ([#1415](https://github.com/GenericMappingTools/pygmt/pull/1415))
* Add a gallery example for grdclip ([#1396](https://github.com/GenericMappingTools/pygmt/pull/1396))
* Add a gallery example for different colormaps in subplots ([#1394](https://github.com/GenericMappingTools/pygmt/pull/1394))
* Add a gallery example for the contour method ([#1387](https://github.com/GenericMappingTools/pygmt/pull/1387))
* Add a gallery example showing individual custom symbols ([#1348](https://github.com/GenericMappingTools/pygmt/pull/1348))
* Add common option aliases to COMMON_OPTIONS in decorators.py ([#1407](https://github.com/GenericMappingTools/pygmt/pull/1407))
* Add return statement to grdclip and grdgradient docstring ([#1390](https://github.com/GenericMappingTools/pygmt/pull/1390))
* Restructure contributing.md to separate docs/general info from contributing code section ([#1339](https://github.com/GenericMappingTools/pygmt/pull/1339))

### Maintenance

* Add tomli as a dependency in GMT Dev Tests ([#1401](https://github.com/GenericMappingTools/pygmt/pull/1401))
* NEP29: Test PyGMT on NumPy 1.21 ([#1355](https://github.com/GenericMappingTools/pygmt/pull/1355))

### Contributors

* [Max Jones](https://github.com/maxrjones)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Michael Grund](https://github.com/michaelgrund)
* [Wei Ji Leong](https://github.com/weiji14)
* [Yohai Magen](https://github.com/yohaimagen)
* [Jiayuan Yao](https://github.com/core-man)
* [Dongdong Tian](https://github.com/seisman)
* [Kadatatlu Kishore](https://github.com/kadatatlukishore)
* [@sean0921](https://github.com/sean0921)
* [Soham Banerjee](https://github.com/soham4abc)

----

## Release v0.4.0 (2021/06/20)

[![Digital Object Identifier for PyGMT v0.4.0](https://zenodo.org/badge/DOI/10.5281/zenodo.4978645.svg)](https://doi.org/10.5281/zenodo.4978645)

### Highlights

* 🎉 **Fourth minor release of PyGMT** 🎉
* Add tutorials for datetime data ([#1193](https://github.com/GenericMappingTools/pygmt/pull/1193)) and plotting vectors ([#1070](https://github.com/GenericMappingTools/pygmt/pull/1070))
* Support tab auto-completion in Jupyter ([#1282](https://github.com/GenericMappingTools/pygmt/pull/1282))
* Minimum required GMT version is now 6.2.0 or newer ([#1321](https://github.com/GenericMappingTools/pygmt/pull/1321))

### New Features

* Wrap blockmean ([#1092](https://github.com/GenericMappingTools/pygmt/pull/1092))
* Wrap grdclip ([#1261](https://github.com/GenericMappingTools/pygmt/pull/1261))
* Wrap grdfill ([#1276](https://github.com/GenericMappingTools/pygmt/pull/1276))
* Wrap grdgradient ([#1269](https://github.com/GenericMappingTools/pygmt/pull/1269))
* Wrap grdlandmask ([#1273](https://github.com/GenericMappingTools/pygmt/pull/1273))
* Wrap histogram ([#1072](https://github.com/GenericMappingTools/pygmt/pull/1072))
* Wrap rose ([#794](https://github.com/GenericMappingTools/pygmt/pull/794))
* Wrap solar ([#804](https://github.com/GenericMappingTools/pygmt/pull/804))
* Wrap velo ([#525](https://github.com/GenericMappingTools/pygmt/pull/525))
* Wrap wiggle ([#1145](https://github.com/GenericMappingTools/pygmt/pull/1145))
* Add new function to load fractures sample data ([#1101](https://github.com/GenericMappingTools/pygmt/pull/1101))
* Allow load_earth_relief() to load the original land-only 01s or 03s SRTM tiles ([#976](https://github.com/GenericMappingTools/pygmt/pull/976))
* Handle geopandas and shapely geometries via geo_interface link ([#1000](https://github.com/GenericMappingTools/pygmt/pull/1000))
* Support passing string type numbers, geographic coordinates and datetimes ([#975](https://github.com/GenericMappingTools/pygmt/pull/975))

### Enhancements

* Allow passing an array as intensity for plot3d ([#1109](https://github.com/GenericMappingTools/pygmt/pull/1109))
* Allow passing an array as intensity for plot ([#1065](https://github.com/GenericMappingTools/pygmt/pull/1065))
* Allow passing xr.DataArray as shading to grdimage ([#750](https://github.com/GenericMappingTools/pygmt/pull/750))
* Allow x/y/z input for blockmedian and blockmean ([#1319](https://github.com/GenericMappingTools/pygmt/pull/1319))
* Allow pygmt.which to accept a list of filenames as input ([#1312](https://github.com/GenericMappingTools/pygmt/pull/1312))
* Refactor blockm* to use virtualfile_from_data and improve i/o ([#1280](https://github.com/GenericMappingTools/pygmt/pull/1280))
* Refactor grdtrack to use virtualfile_from_data and improve i/o to pandas.DataFrame ([#1189](https://github.com/GenericMappingTools/pygmt/pull/1189))
* Add parameters to histogram ([#1249](https://github.com/GenericMappingTools/pygmt/pull/1249))
* Add alias 'aspatial' to methods blockmedian, info, plot, plot3d, surface ([#1090](https://github.com/GenericMappingTools/pygmt/pull/1090))
* Add alias 'registration' to methods blockmean, info, grdfilter, surface ([#1089](https://github.com/GenericMappingTools/pygmt/pull/1089))
* Add incols to COMMON_OPTIONS, blockmean, and blockmedian ([#1300](https://github.com/GenericMappingTools/pygmt/pull/1300))
* Improve Figure.show for displaying previews in Jupyter notebooks and external viewers ([#529](https://github.com/GenericMappingTools/pygmt/pull/529))
* Let Figure.savefig recommend .eps or .pdf when .ps extension is used ([#1307](https://github.com/GenericMappingTools/pygmt/pull/1307))

### Deprecations

* Figure.contour: Deprecate parameter "columns" to "incols" (remove in v0.6.0) ([#1303](https://github.com/GenericMappingTools/pygmt/pull/1303))
* Figure.plot: Deprecate parameter "sizes" to "size" (remove in v0.6.0) ([#1254](https://github.com/GenericMappingTools/pygmt/pull/1254))
* Figure.plot: Deprecate parameter "columns" to "incols" (remove in v0.6.0) ([#1298](https://github.com/GenericMappingTools/pygmt/pull/1298))
* Figure.plot3d: Deprecate parameter "sizes" to "size" (remove in v0.6.0) ([#1258](https://github.com/GenericMappingTools/pygmt/pull/1258))
* Figure.plot3d: Deprecate parameter "columns" to "incols" (remove in v0.6.0) ([#1040](https://github.com/GenericMappingTools/pygmt/pull/1040))
* Figure.rose: Deprecate parameter "columns" to "incols" (remove in v0.6.0) ([#1306](https://github.com/GenericMappingTools/pygmt/pull/1306))
* NEP29: Set minimum required versions to NumPy 1.17+ and Python 3.7+ ([#1074](https://github.com/GenericMappingTools/pygmt/pull/1074))
* Raise a warning for the use of short-form parameters when long-forms are available ([#1316](https://github.com/GenericMappingTools/pygmt/pull/1316))

### Bug Fixes

* Allow pandas.Series inputs to fig.histogram and pygmt.info ([#1329](https://github.com/GenericMappingTools/pygmt/pull/1329))
* Explicitly use netcdf4 engine in xarray.open_dataarray to read grd files ([#1264](https://github.com/GenericMappingTools/pygmt/pull/1264))
* Let Figure.savefig support filenames with spaces ([#1116](https://github.com/GenericMappingTools/pygmt/pull/1116))
* Let Figure.show(method='external') work well in Python scripts ([#1062](https://github.com/GenericMappingTools/pygmt/pull/1062))

### Documentation

* Add histogram gallery example ([#1272](https://github.com/GenericMappingTools/pygmt/pull/1272))
* Add a gallery example showing individual basic geometric symbols ([#1211](https://github.com/GenericMappingTools/pygmt/pull/1211))
* Specify rectangle's width and height via style parameter in multi-parameter symbols example ([#1325](https://github.com/GenericMappingTools/pygmt/pull/1325))
* Update the inset gallery example ([#1287](https://github.com/GenericMappingTools/pygmt/pull/1287))
* Add categorical colorbars for plot, plot3d and line colors gallery examples ([#1267](https://github.com/GenericMappingTools/pygmt/pull/1267))
* Apply NIST SI unit convention to some gallery examples ([#1194](https://github.com/GenericMappingTools/pygmt/pull/1194))
* Use colorblind-friendly colors in the scatter plots gallery example ([#1013](https://github.com/GenericMappingTools/pygmt/pull/1013))
* Added documentation for three oblique mercator projections ([#1251](https://github.com/GenericMappingTools/pygmt/pull/1251))
* Add a list of external PyGMT resources ([#1210](https://github.com/GenericMappingTools/pygmt/pull/1210))
* Complete documentation for grdtrack ([#1190](https://github.com/GenericMappingTools/pygmt/pull/1190))
* Add projection and region to grdview docstring ([#1295](https://github.com/GenericMappingTools/pygmt/pull/1295))
* Add common alias spacing (-I) for specifying grid increments ([#1288](https://github.com/GenericMappingTools/pygmt/pull/1288))
* Standardize docstrings for table-like inputs ([#1186](https://github.com/GenericMappingTools/pygmt/pull/1186))
* Clarify that the "transparency" parameter in plot/plot3d/text can be 1d array  ([#1265](https://github.com/GenericMappingTools/pygmt/pull/1265))
* Clarify that the "color" parameter in plot/plot3d can be 1d array ([#1260](https://github.com/GenericMappingTools/pygmt/pull/1260))
* Clarify interplay of spacing and per_column in info ([#1127](https://github.com/GenericMappingTools/pygmt/pull/1127))
* Remove the "full test" section from installation guide ([#1206](https://github.com/GenericMappingTools/pygmt/pull/1206))
* Clarify position of deprecate_parameter decorator to be above use_alias ([#1302](https://github.com/GenericMappingTools/pygmt/pull/1302))
* Add guidelines for managing issues to maintenance.md ([#1301](https://github.com/GenericMappingTools/pygmt/pull/1301))
* Add alias name convention to CONTRIBUTING.md ([#1256](https://github.com/GenericMappingTools/pygmt/pull/1256))
* Move contributing guide details to website and rename two sections ([#1335](https://github.com/GenericMappingTools/pygmt/pull/1335))
* Update the check_figures_equal testing section in CONTRIBUTING.md  ([#1108](https://github.com/GenericMappingTools/pygmt/pull/1108))
* Revise Pull Request review process in CONTRIBUTING.md ([#1119](https://github.com/GenericMappingTools/pygmt/pull/1119))

### Maintenance

* Add a workflow to upload baseline images as a release asset ([#1317](https://github.com/GenericMappingTools/pygmt/pull/1317))
* Add regression test for grdimage plotting an xarray.DataArray grid subset ([#1314](https://github.com/GenericMappingTools/pygmt/pull/1314))
* Add download_test_data to download data files used in tests ([#1310](https://github.com/GenericMappingTools/pygmt/pull/1310))
* Remove xfails and workarounds for datetime inputs into pygmt.info ([#1236](https://github.com/GenericMappingTools/pygmt/pull/1236))
* Improve the DVC image diff workflow to support side-by-side comparison of modified images ([#1219](https://github.com/GenericMappingTools/pygmt/pull/1219))
* Document the deprecation policy and add the deprecate_parameter decorator to deprecate parameters ([#1160](https://github.com/GenericMappingTools/pygmt/pull/1160))
* Convert booleans arguments in build_arg_string, not in kwargs_to_strings ([#1125](https://github.com/GenericMappingTools/pygmt/pull/1125))
* Create GitHub Action workflow for reporting DVC image diffs ([#1104](https://github.com/GenericMappingTools/pygmt/pull/1104))
* Update "GMT Dev Tests" workflow to test macOS-11.0 and pre-release Python packages ([#1105](https://github.com/GenericMappingTools/pygmt/pull/1105))
* Initialize data version control for managing test images ([#1036](https://github.com/GenericMappingTools/pygmt/pull/1036))
* Separate workflows for running tests and building documentation ([#1033](https://github.com/GenericMappingTools/pygmt/pull/1033))

### Contributors

* [Dongdong Tian](https://github.com/seisman)
* [Wei Ji Leong](https://github.com/weiji14)
* [Michael Grund](https://github.com/michaelgrund)
* [Max Jones](https://github.com/maxrjones)
* [Will Schlitzer](https://github.com/willschlitzer)
* [Jiayuan Yao](https://github.com/core-man)
* [Abhishek Anant](https://github.com/noturshek)
* [Claire Klima](https://github.com/cklima616)
* [Megan Munzek](https://github.com/munzekm)
* [Michael Neumann](https://github.com/MichaeINeumann)
* [Nathan Loria](https://github.com/Nathandloria)
* [Noor Buchi](https://github.com/noorbuchi)
* [Shivani chauhan](https://github.com/xdshivani)
* [@alperen-kilic](https://github.com/alperen-kilic)
* [Loïc Houpert](https://github.com/lhoupert)
* [Emily McMullan](https://github.com/eemcmullan)
* [Lawrence Qupty](https://github.com/Lawqup)
* [Matthew Tankersley](https://github.com/mdtanker)
* [@shahid-0](https://github.com/shahid-0)
* [Vitor Gratiere Torres](https://github.com/vitorgt)

----

## Release v0.3.1 (2021/03/14)

[![Digital Object Identifier for PyGMT v0.3.1](https://zenodo.org/badge/DOI/10.5281/zenodo.4592991.svg)](https://doi.org/10.5281/zenodo.4592991)

### Highlights

* 🎉 **Multiple bug fixes and an improved gallery** 🎉
* Reorganized gallery examples into new categories ([#995](https://github.com/GenericMappingTools/pygmt/pull/995))
* Added gallery examples for plotting vectors ([#950](https://github.com/GenericMappingTools/pygmt/pull/950), [#890](https://github.com/GenericMappingTools/pygmt/pull/890))
* Last version to support GMT 6.1.1, future PyGMT versions will require GMT 6.2.0 or newer

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
* [Max Jones](https://github.com/maxrjones)
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
* [Max Jones](https://github.com/maxrjones)

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
* Add PyGMT Zenodo BibTeX entry to main README ([#678](https://github.com/GenericMappingTools/pygmt/pull/678))
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
