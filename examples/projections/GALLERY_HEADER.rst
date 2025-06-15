Projections
===========

PyGMT supports many map projections; see :doc:`/techref/projections` for an overview.
Use the ``projection`` parameter to specify which one you want to use in all plotting
methods. The projection is specified by a one-letter code along with (sometimes optional)
reference longitude and latitude and the width of the map (for example,
**A**\ *lon0/lat0*\ [*/horizon*\ ]\ */width*). The map height is determined based on the
region and projection. Furthermore, the usage of :doc:`EPSG codes </gallery/maps/epsg_codes>`
is suppported.

These are all the available projections:
