Projection Table
================

PyGMT offers 31 map projections. These are specified using the ``projection`` argument.
The projection codes for the projection styles are shown below.

.. Substitution definitions:
.. |lon0| replace:: lon\ :sub:`0`
.. |lat0| replace:: lat\ :sub:`0`
.. |lon1| replace:: lon\ :sub:`1`
.. |lat1| replace:: lat\ :sub:`1`
.. |lat2| replace:: lat\ :sub:`2`
.. |lonp| replace:: lon\ :sub:`p`
.. |latp| replace:: lat\ :sub:`p`

.. list-table::
   :widths: 33 33
   :header-rows: 2

   * - PyGMT Projection Argument
     - Projection Name
   * - ``projection=`` (upper case for *width*, lower case for *scale*)
     -
   * - **A**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - Lambert azimuthal equal area