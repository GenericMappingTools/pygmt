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
     - :doc:`Lambert azimuthal equal area </projections/azim/azim-lambert>`
   * - **B**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Albers conic equal area </projections/conic/conic-albers>`
   * - **C**\ |lon0|/|lat0|/\ *width*
     - :doc:`Cassini cylindrical </projections/cyl/cyl-cassini>`
   * - **Cyl_stere/**\ [|lon0|\ [/|lat0|/]]\ *width*
     - :doc:`Cylindrical stereographic </projections/cyl/cyl-stereographic>`
   * - **D**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Equidistant conic </projections/conic/conic-equidistant>`
   * - **E**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal equidistant </projections/azim/azim-equidistant>`
   * - **F**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal gnomonic </projections/azim/azim-gnomonic>`
   * - **G**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal orthographic </projections/azim/azim-orthographic>`
   * - **G**\ |lon0|/|lat0|/\ *alt*/*azim*/*tilt*/*twist*/*W*/*H*/*width*
     - :doc:`General perspective </projections/azim/azim-general-perspective>`
   * - **H**\ [|lon0|/]\ *width*
     - :doc:`Hammer equal area </projections/misc/misc-hammer>`
   * - **I**\ [|lon0|/]\ *width*
     - :doc:`Sinusoidal equal area </projections/misc/misc-sinusoidal>`
   * - **J**\ [|lon0|/]\ *width*
     - :doc:`Miller cylindrical </projections/cyl/cyl-miller>`
   * - **Kf**\ [|lon0|/]\ *width*
     - :doc:`Eckert IV equal area </projections/misc/misc-eckertIV>`
   * - **Ks**\ [|lon0|/]\ *width*
     - :doc:`Eckert VI equal area </projections/misc/misc-eckertVI>`
   * - **L**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Lambert conic conformal </projections/conic/conic-lambert>`
   * - **M**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :doc:`Mercator cylindrical </projections/cyl/cyl-mercator>`
   * - **N**\ [|lon0|/]\ *width*
     - :doc:`Robinson </projections/misc/misc-robinson>`
   * - **Oa**\ |lon0|/|lat0|/\ *azim*/*width*\ [**+v**]
     - Oblique Mercator, 1: origin and azim
   * - **Ob**\ |lon0|/|lat0|/|lon1|/|lat1|/\ *width*\ [**+v**]
     - Oblique Mercator, 2: two points
   * - **Oc**\ |lon0|/|lat0|/|lonp|/|latp|/\ *width*\ [**+v**]
     - Oblique Mercator, 3: origin and pole
   * - **P**\ *width*\ [**+a**]\ [**+f**\ [**e**\|\ **p**\|\ *radius*]]\
       [**+r**\ *offset*][**+t**\ *origin*][**+z**\ [**p**\|\ *radius*]]
     - :doc:`Polar </projections/nongeo/polar>` [azimuthal]
       (:math:`\theta, r`) (or cylindrical)
   * - **Poly**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :doc:`Polyconic </projections/conic/polyconic>`
   * - **Q**\ [|lon0|\ [/|lat0|/]]\ *width*
     - :doc:`Equidistant cylindrical </projections/cyl/cyl-equidistant>`
   * - **R**\ [|lon0|/]\ *width*
     - :doc:`Winkel Tripel </projections/misc/misc-winkel-tripel>`
   * - **S**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`General stereographic
       </projections/azim/azim-general-stereographic>`
   * - **T**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :doc:`Transverse Mercator </projections/cyl/cyl-transverse-mercator>`
   * - **U**\ *zone*/*width*
     - :doc:`Universal Transverse Mercator (UTM)
       </projections/cyl/cyl-universal-transverse-mercator>`
   * - **V**\ [|lon0|/]\ *width*
     - :doc:`Van der Grinten </projections/misc/misc-van-der-grinten>`
   * - **W**\ [|lon0|/]\ *width*
     - :doc:`Mollweide </projections/misc/misc-mollweide>`
   * - **X**\ *width*\ [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**][/\ *height*\
       [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**]][**d**]
     - :doc:`Linear </projections/nongeo/cartesian-linear>`,
       :doc:`logarithmic </projections/nongeo/cartesian-logarithmic>`,
       :doc:`power </projections/nongeo/cartesian-power>`, and time
   * - **Y**\ |lon0|/|lat0|/\ *width*
     - :doc:`Cylindrical equal area </projections/cyl/cyl-equal-area>`
