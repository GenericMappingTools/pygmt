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
     - :doc:`Lambert azimuthal equal area </projections/azim/azim_lambert>`
   * - **B**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Albers conic equal area </projections/conic/conic_albers>`
   * - **C**\ |lon0|/|lat0|/\ *width*
     - :doc:`Cassini cylindrical </projections/cyl/cyl_cassini>`
   * - **Cyl_stere**/\ [|lon0|/\ [|lat0|/]]\ *width*
     - :doc:`Cylindrical stereographic </projections/cyl/cyl_stereographic>`
   * - **D**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Equidistant conic </projections/conic/conic_equidistant>`
   * - **E**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal equidistant </projections/azim/azim_equidistant>`
   * - **F**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal gnomonic </projections/azim/azim_gnomonic>`
   * - **G**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`Azimuthal orthographic </projections/azim/azim_orthographic>`
   * - **G**\ |lon0|/|lat0|/\ *width*\ [**+a**\ *azimuth*]\ [**+t**\ *tilt*]\
       [**+v**\ *vwidth*/*vheight*]\ [**+w**\ *twist*]\ [**+z**\ *altitude*]
     - :doc:`General perspective </projections/azim/azim_general_perspective>`
   * - **H**\ [|lon0|/]\ *width*
     - :doc:`Hammer equal area </projections/misc/misc_hammer>`
   * - **I**\ [|lon0|/]\ *width*
     - :doc:`Sinusoidal equal area </projections/misc/misc_sinusoidal>`
   * - **J**\ [|lon0|/]\ *width*
     - :doc:`Miller cylindrical </projections/cyl/cyl_miller>`
   * - **Kf**\ [|lon0|/]\ *width*
     - :doc:`Eckert IV equal area </projections/misc/misc_eckertIV>`
   * - **Ks**\ [|lon0|/]\ *width*
     - :doc:`Eckert VI equal area </projections/misc/misc_eckertVI>`
   * - **L**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :doc:`Lambert conic conformal </projections/conic/conic_lambert>`
   * - **M**\ [|lon0|/\ [|lat0|/]]\ *width*
     - :doc:`Mercator cylindrical </projections/cyl/cyl_mercator>`
   * - **N**\ [|lon0|/]\ *width*
     - :doc:`Robinson </projections/misc/misc_robinson>`
   * - **Oa**\ |lon0|/|lat0|/\ *azimuth*/*width*\ [**+v**]
     - :doc:`Oblique Mercator, 1: origin and azimuth </projections/cyl/cyl_oblique_mercator_1>`
   * - **Ob**\ |lon0|/|lat0|/|lon1|/|lat1|/\ *width*\ [**+v**]
     - :doc:`Oblique Mercator, 2: two points </projections/cyl/cyl_oblique_mercator_2>`
   * - **Oc**\ |lon0|/|lat0|/|lonp|/|latp|/\ *width*\ [**+v**]
     - :doc:`Oblique Mercator, 3: origin and pole </projections/cyl/cyl_oblique_mercator_3>`
   * - **P**\ *width*\ [**+a**]\ [**+f**\ [**e**\|\ **p**\|\ *radius*]]\
       [**+r**\ *offset*][**+t**\ *origin*][**+z**\ [**p**\|\ *radius*]]
     - :doc:`Polar </projections/nongeo/polar>` [azimuthal]
       (:math:`\theta, r`) (or cylindrical)
   * - **Poly**/\ [|lon0|/\ [|lat0|/]]\ *width*
     - :doc:`Polyconic </projections/conic/polyconic>`
   * - **Q**\ [|lon0|/\ [|lat0|/]]\ *width*
     - :doc:`Equidistant cylindrical </projections/cyl/cyl_equidistant>`
   * - **R**\ [|lon0|/]\ *width*
     - :doc:`Winkel Tripel </projections/misc/misc_winkel_tripel>`
   * - **S**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :doc:`General stereographic
       </projections/azim/azim_general_stereographic>`
   * - **T**\ |lon0|\ [/\ |lat0|]/\ *width*
     - :doc:`Transverse Mercator </projections/cyl/cyl_transverse_mercator>`
   * - **U**\ *zone*/*width*
     - :doc:`Universal Transverse Mercator (UTM)
       </projections/cyl/cyl_universal_transverse_mercator>`
   * - **V**\ [|lon0|/]\ *width*
     - :doc:`Van der Grinten </projections/misc/misc_van_der_grinten>`
   * - **W**\ [|lon0|/]\ *width*
     - :doc:`Mollweide </projections/misc/misc_mollweide>`
   * - **X**\ *width*\ [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**][/\ *height*\
       [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**]][**d**]
     - :doc:`Linear </projections/nongeo/cartesian_linear>`,
       :doc:`logarithmic </projections/nongeo/cartesian_logarithmic>`,
       :doc:`power </projections/nongeo/cartesian_power>`, and time
   * - **Y**\ |lon0|/|lat0|/\ *width*
     - :doc:`Cylindrical equal area </projections/cyl/cyl_equal_area>`
