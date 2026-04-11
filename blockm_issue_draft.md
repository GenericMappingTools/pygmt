# pygmt.blockmean/blockmedian/blockmode: Block average (x, y, z) data tables by mean, median, or mode estimation

*This issue serves as the central place for discussing and tracking the implementation of the `blockmean`, `blockmedian`, and `blockmode` methods in PyGMT. The issue will be closed when the initial implementation is complete. Progress is tracked at https://github.com/orgs/GenericMappingTools/projects/3.*

## Documentation

### blockmean

- GMT: https://docs.generic-mapping-tools.org/dev/blockmean.html
- GMT.jl: https://www.generic-mapping-tools.org/GMTjl_doc/documentation/modules/blockmean
- PyGMT: https://www.pygmt.org/dev/api/generated/pygmt.blockmean.html

### blockmedian

- GMT: https://docs.generic-mapping-tools.org/dev/blockmedian.html
- GMT.jl: https://www.generic-mapping-tools.org/GMTjl_doc/documentation/modules/blockmedian
- PyGMT: https://www.pygmt.org/dev/api/generated/pygmt.blockmedian.html

### blockmode

- GMT: https://docs.generic-mapping-tools.org/dev/blockmode.html
- GMT.jl: https://www.generic-mapping-tools.org/GMTjl_doc/documentation/modules/blockmode
- PyGMT: https://www.pygmt.org/dev/api/generated/pygmt.blockmode.html

## GMT Option Flags and Modifiers

☑️: *Implemented*; ⬜: *To be implemented/discussed*; ~~Strikethrough~~: *Won't implement*.

### blockmean

- [ ] `-C`: Report center of block as position instead of mean position
- [ ] `-E`: Estimate standard deviations (or median absolute deviations) per block
- [ ] `-G`: Write output to one or more grid files
- [x] `-I`: `spacing`
- [x] `-R`: `region`
- [x] `-S`: `summary`
- [ ] `-W`: Input/output weights
- [x] `-V`: `verbose`
- [x] `-a`: `aspatial`
- [x] `-b`: `binary`
- [x] `-d`: `nodata`
- [x] `-e`: `find`
- [x] `-f`: `coltypes`
- [ ] `-g`: `gap`
- [x] `-h`: `header`
- [x] `-i`: `incols`
- [x] `-o`: `outcols`
- [ ] `-q`: `select_rows`
- [x] `-r`: `registration`
- [ ] `-s`: `skiprows`
- [x] `-w`: `wrap`
- [ ] ~~`-U`~~: Use `Figure.timestamp` instead.
- [ ] ~~`-X`/`-Y`~~: Use `Figure.shift_origin` instead.
- [ ] ~~`--PAR=value`~~: Use `pygmt.config` instead.

### blockmedian

- [ ] `-C`: Report center of block as position instead of median position
- [ ] `-E`: Estimate median absolute deviations per block
- [ ] `-G`: Write output to one or more grid files
- [x] `-I`: `spacing`
- [ ] `-Q`: No median checking (use with `-E`)
- [x] `-R`: `region`
- [ ] `-T`: Select the L1 norm (MAD) instead of median
- [ ] `-W`: Input/output weights
- [x] `-V`: `verbose`
- [x] `-a`: `aspatial`
- [x] `-b`: `binary`
- [x] `-d`: `nodata`
- [x] `-e`: `find`
- [x] `-f`: `coltypes`
- [ ] `-g`: `gap`
- [x] `-h`: `header`
- [x] `-i`: `incols`
- [x] `-o`: `outcols`
- [ ] `-q`: `select_rows`
- [x] `-r`: `registration`
- [ ] `-s`: `skiprows`
- [x] `-w`: `wrap`
- [ ] ~~`-U`~~: Use `Figure.timestamp` instead.
- [ ] ~~`-X`/`-Y`~~: Use `Figure.shift_origin` instead.
- [ ] ~~`--PAR=value`~~: Use `pygmt.config` instead.

### blockmode

- [ ] `-C`: Report center of block as position instead of mode position
- [ ] `-D`: Set bin width for LMS mode estimation
- [ ] `-E`: Estimate LMS sigma per block
- [ ] `-G`: Write output to one or more grid files
- [x] `-I`: `spacing`
- [ ] `-Q`: Use quantile (not LMS) mode estimation
- [x] `-R`: `region`
- [ ] `-W`: Input/output weights
- [x] `-V`: `verbose`
- [x] `-a`: `aspatial`
- [x] `-b`: `binary`
- [x] `-d`: `nodata`
- [x] `-e`: `find`
- [x] `-f`: `coltypes`
- [ ] `-g`: `gap`
- [x] `-h`: `header`
- [x] `-i`: `incols`
- [x] `-o`: `outcols`
- [ ] `-q`: `select_rows`
- [x] `-r`: `registration`
- [ ] `-s`: `skiprows`
- [x] `-w`: `wrap`
- [ ] ~~`-U`~~: Use `Figure.timestamp` instead.
- [ ] ~~`-X`/`-Y`~~: Use `Figure.shift_origin` instead.
- [ ] ~~`--PAR=value`~~: Use `pygmt.config` instead.

## Related GMT configurations

*List any related GMT configurations that may affect the behavior.*

## Notes on Input Formats

The functions accept (x, y, z) data as:
- A path to an ASCII data table file
- A 2-D `numpy.ndarray`
- A `pandas.DataFrame`
- An `xarray.Dataset`
- Separate 1-D arrays for x, y, and z coordinates

Optionally, a fourth column of weights (w) may be provided when using `-W`.

## Linked Pull Requests

- [x] Initial feature implementation (#596, #627, #1027)
- [ ] Add missing option flags (`-C`, `-E`, `-G`, `-W`, `-g`, `-q`, `-s`, and module-specific flags)
- [x] Add a gallery example

## Related Issues and Discussions

- #596: Initial `blockmean` implementation
- #627: Initial `blockmedian` implementation
- #1027: Initial `blockmode` implementation
