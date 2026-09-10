# Dimension and Distance Units

As a geospatial analysis and mapping package, GMT needs to distinguish between two types
of units: those used for plotting and those used for geographic distances. The former
are called **dimension units** (or plot units) and the latter are called
**distance units**.

(dimension-units)=
## Dimension Units

Dimension units are used for map dimensions, symbol sizes, pen widths, etc.

| Code | Unit | Notes |
|------|------|-------|
| `c` | Centimeter | Default for most dimensions |
| `i` | Inch | 1 inch = 2.54 cm |
| `p` | Point | 1 point = 1/72 inch |

**Defaults:** If no unit is given, GMT uses {gmt-term}`PROJ_LENGTH_UNIT` (default is `c`).
Fonts and pen thicknesses default to `p`.

(distance-units)=
## Distance Units

GMT supports various distance units for geographic calculations.

| Code | Unit | Notes |
|------|------|-------|
| `d` | Degree | Arc degree |
| `m` | Minute of arc | 1/60 degree |
| `s` | Second of arc | 1/3600 degree |
| `e` | Meter | Default distance unit |
| `k` | Kilometer | 1000 meters |
| `f` | Foot | 0.3048 meters |
| `u` | US Survey Foot | 1200/3937 meters |
| `M` | Statute Mile | 1.60934 km |
| `n` | Nautical Mile | 1.852 km |
