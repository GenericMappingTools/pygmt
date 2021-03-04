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
     - :doc:`Lambert azimuthal equal area
       </projections/azim/azim_equidistant>`
   * - **B**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :ref:`Albers conic equal area
       <sphx_glr_projections_conic_conic_albers.py>`
   * - **C**\ |lon0|/|lat0|/\ *width*
     - :ref:`Cassini cylindrical <sphx_glr_projections_cyl_cyl_cassini.py>`
   * - **Cyl_stere/**\ [|lon0|\ [/|lat0|/]]\ *width*
     - :ref:`Cylindrical stereographic
       <sphx_glr_projections_cyl_cyl_stereographic.py>`
   * - **D**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :ref:`Equidistant conic
       <sphx_glr_projections_conic_conic_equidistant.py>`
   * - **E**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :ref:`Azimuthal equidistant
       <sphx_glr_projections_azim_azim_equidistant.py>`
   * - **F**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :ref:`Azimuthal gnomonic <sphx_glr_projections_azim_azim_gnomonic.py>`
   * - **G**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :ref:`Azimuthal orthographic
       <sphx_glr_projections_azim_azim_orthographic.py>`
   * - **G**\ |lon0|/|lat0|/\ *alt*/*azim*/*tilt*/*twist*/*W*/*H*/*width*
     - :ref:`General perspective
       <sphx_glr_projections_azim_azim_general_perspective.py>`
   * - **H**\ [|lon0|/]\ *width*
     - :ref:`Hammer equal area <sphx_glr_projections_misc_misc_hammer.py>`
   * - **I**\ [|lon0|/]\ *width*
     - :ref:`Sinusoidal equal area
       <sphx_glr_projections_misc_misc_sinusoidal.py>`
   * - **J**\ [|lon0|/]\ *width*
     - :ref:`Miller cylindrical <sphx_glr_projections_cyl_cyl_miller.py>`
   * - **Kf**\ [|lon0|/]\ *width*
     - :ref:`Eckert IV equal area <sphx_glr_projections_misc_misc_eckertIV.py>`
   * - **Ks**\ [|lon0|/]\ *width*
     - :ref:`Eckert VI equal area <sphx_glr_projections_misc_misc_eckertVI.py>`
   * - **L**\ |lon0|/|lat0|/|lat1|/|lat2|/\ *width*
     - :ref:`Lambert conic conformal
       <sphx_glr_projections_conic_conic_lambert.py>`
   * - **M**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :ref:`Mercator cylindrical <sphx_glr_projections_cyl_cyl_mercator.py>`
   * - **N**\ [|lon0|/]\ *width*
     - :ref:`Robinson <sphx_glr_projections_misc_misc_robinson.py>`
   * - **Oa**\ |lon0|/|lat0|/\ *azim*/*width*\ [**+v**]
     - Oblique Mercator, 1: origin and azim
   * - **Ob**\ |lon0|/|lat0|/|lon1|/|lat1|/\ *width*\ [**+v**]
     - Oblique Mercator, 2: two points
   * - **Oc**\ |lon0|/|lat0|/|lonp|/|latp|/\ *width*\ [**+v**]
     - Oblique Mercator, 3: origin and pole
   * - **P**\ *width*\ [**+a**]\ [**+f**\ [**e**\|\ **p**\|\ *radius*]]\
       [**+r**\ *offset*][**+t**\ *origin*][**+z**\ [**p**\|\ *radius*]]
     - :ref:`Polar <sphx_glr_projections_nongeo_polar.py>` [azimuthal]
       (:math:`\theta, r`) (or cylindrical)
   * - **Poly**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :ref:`Polyconic <sphx_glr_projections_conic_polyconic.py>`
   * - **Q**\ [|lon0|\ [/|lat0|/]]\ *width*
     - :ref:`Equidistant cylindrical
       <sphx_glr_projections_cyl_cyl_equidistant.py>`
   * - **R**\ [|lon0|/]\ *width*
     - :ref:`Winkel Tripel <sphx_glr_projections_misc_misc_winkel_tripel.py>`
   * - **S**\ |lon0|/|lat0|\ [/\ *horizon*]/\ *width*
     - :ref:`General stereographic
       <sphx_glr_projections_azim_azim_general_stereographic.py>`
   * - **T**\ [|lon0|\ [/|lat0|]/]\ *width*
     - :ref:`Transverse Mercator
       <sphx_glr_projections_cyl_cyl_transverse_mercator.py>`
   * - **U**\ *zone*/*width*
     - :ref:`Universal Transverse Mercator (UTM)
       <sphx_glr_projections_cyl_cyl_universal_transverse_mercator.py>`
   * - **V**\ [|lon0|/]\ *width*
     - :ref:`Van der Grinten
       <sphx_glr_projections_misc_misc_van_der_grinten.py>`
   * - **W**\ [|lon0|/]\ *width*
     - :ref:`Mollweide <sphx_glr_projections_misc_misc_mollweide.py>`
   * - **X**\ *width*\ [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**][/\ *height*\
       [**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**]][**d**]
     - :ref:`Linear <sphx_glr_projections_nongeo_cartesian_linear.py>`,
       :ref:`log <sphx_glr_projections_nongeo_cartesian_logarithmic.py>`\
       :math:`_{10}`, :ref:`power
       <sphx_glr_projections_nongeo_cartesian_power.py>`, and time
   * - **Y**\ |lon0|/|lat0|/\ *width*
     - :ref:`Cylindrical equal area
       <sphx_glr_projections_cyl_cyl_equal_area.py>`
