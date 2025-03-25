# Common Parameters

```{glossary}
``distcalc``
    Determine how spherical distances are calculated. Valid values are:

    - ``"g"``: Perform great circle distance calculations, with parameters such as
      distance increments or radii compared against calculated great circle distances
      [Default]
    - ``"e"``: Select ellipsoidal (or geodesic) mode for the highest precision and
      slowest calculation time.
    - ``"f"``: Select Flat Earth mode, which gives a more approximate but faster result

    **Note:** (1) All spherical distance calculations depend on the current ellipsoid
    ({gmt-term}`PROJ_ELLIPSOID`), the definition of the mean radius
    ({gmt-term}`PROJ_MEAN_RADIUS`), and the specification of latitude type
    ({gmt-term}`PROJ_AUX_LATITUDE`). Geodesic distance calculations are also controlled
    by the algorithm to use for geodesic calculations ({gmt-term}`PROJ_GEODESIC`).
    (2) Coordinate transformations that can use ellipsoidal or spherical forms will
    first consult this parameter if given.

``verbose``
    Select verbosity level, which modulates the messages written to stderr.

    Choose among 7 levels of verbosity [Default is ``"w"``]:

    - ``"q"``: Quiet, not even fatal error messages are produced
    - ``"e"``: Error messages only
    - ``"w"``: Warnings [Default]
    - ``"t"``: Timings (report runtimes for time-intensive algorithms)
    - ``"i"``: Informational messages (same as ``verbose=True``)
    - ``"c"``: Compatibility warnings
    - ``"d"``: Debugging messages
```
