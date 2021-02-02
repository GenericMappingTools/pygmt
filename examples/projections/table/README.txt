Projection Table
----------------

The below table shows the projection codes for the 31 GMT projections.

.. Substitution definitions:
.. |lon0| replace:: lon\ :sub:`0`
.. |lat0| replace:: lat\ :sub:`0`
.. |lon1| replace:: lon\ :sub:`1`
.. |lat1| replace:: lat\ :sub:`1`
.. |lat2| replace:: lat\ :sub:`2`
.. |lonp| replace:: lon\ :sub:`p`
.. |latp| replace:: lat\ :sub:`p`

.. list-table::
   :widths: 20 28
   :header-rows: 1

   * - PyGMT Projection Argument
     - Projection Name
   * - **A**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - Lambert azimuthal equal area
   * - **B**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - Albers conic equal area
   * - **C**\ |lon0|/|lat0|/\ *width*
     - Cassini cylindrical
   * - **Cyl_stere/**\ [|lon0|\ [/|lat0|/]]\ *width*
     - Cylindrical stereographic
   * - **D**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - Equidistant conic
   * - **E**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - Azimuthal equidistant
   * - **F**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - Azimuthal gnomonic
   * - **G**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - Azimuthal orthographic
   * - **G**\ |lon0|/|lat0|/\ *alt*/*azim*/*tilt*/*twist*/*W*/*H*/*width*
     - General perspective
   * - **H**\ [|lon0|/]\ *width*
     - Hammer equal area
   * - **I**\ [|lon0|/]\ *width*
     - Sinusoidal equal area
   * - **J**\ [|lon0|/]\ *width*
     - Miller cylindrical
   * - **Kf**\ [|lon0|/]\ *width*
     - Eckert IV equal area
   * - **Ks**\ [|lon0|/]\ *width*
     - Eckert VI equal area
   * - **L**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - Lambert conic conformal
   * - **M**\ [|lon0|\ [/|lat0|]/]\ *width*
     - Mercator cylindrical
   * - **N**\ [|lon0|/]\ *width*
     - Robinson
   * - **Oa**\ |lon0|/|lat0|/\ *azim*/*width*\ [**+v**]
     - Oblique Mercator, 1: origin and azim
   * - **Ob**\ |lon0|/|lat0|/|lon1|/|lat1|/\ *width*\ [**+v**]
     - Oblique Mercator, 2: two points
   * - **Oc**\ |lon0|/|lat0|/|lonp|/|latp|/\ *width*\ [**+v**]
     - Oblique Mercator, 3: origin and pole
   * - **P**\ *width*\ [**+a**]\ [**+f**\ [**e**\|\ **p**\|\ *radius*]][**+r**\ *offset*][**+t**\ *origin*][**+z**\ [**p**\|\ *radius*]]
     - Polar [azimuthal] (:math:`\theta, r`) (or cylindrical)
   * - **Poly**\ [|lon0|\ [/|lat0|]/]\ *width*
     - Polyconic
   * - **Q**\ [|lon0|\ [/|lat0|/]]\ *width*
     - Equidistant cylindrical
   * - **R**\ [|lon0|/]\ *width*
     - Winkel Tripel
   * - **S**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - General stereographic
   * - **T**\ [|lon0|\ [/|lat0|]/]\ *width*
     - Transverse Mercator
   * - **U**\ *zone*/*width*
     - Universal Transverse Mercator (UTM)
   * - **V**\ [|lon0|/]\ *width*
     - Van der Grinten
   * - **W**\ [|lon0|/]\ *width*
     - Mollweide
   * - **X**\ *width*\ [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**][/\ *height*\ [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**]][**d**]
     - Linear, log\ :math:`_{10}`, :math:`x^a-y^b`, and time
   * - **Y**\ |lon0|/|lat0|/\ *width*
     - Cylindrical equal area
