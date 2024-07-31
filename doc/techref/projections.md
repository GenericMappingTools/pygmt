# GMT Map Projections

The table below shows the projection codes for the 31 GMT projections:

| PyGMT Projection Argument | Projection Name |
| --- | --- |
| **A**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Lambert azimuthal equal area](https://www.pygmt.org/latest/projections/azim/azim_equidistant.html) |
| **B**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Albers conic equal area](https://www.pygmt.org/latest/projections/conic/conic_albers.html) |
| **C**{{ lon0 }}/{{ lat0 }}/*width* | [Cassini cylindrical](https://www.pygmt.org/latest/projections/cyl/cyl_cassini.html) |
| **Cyl_stere**/[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Cylindrical stereographic](https://www.pygmt.org/latest/projections/cyl/cyl_stereographic.html) |
| **D**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Equidistant conic](https://www.pygmt.org/latest/projections/conic/conic_equidistant) |
| **E**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal equidistant](https://www.pygmt.org/latest/projections/azim/azim_equidistant) |
| **F**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal gnomonic](https://www.pygmt.org/latest/projections/azim/azim_gnomonic) |
| **G**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal orthographic](https://www.pygmt.org/latest/projections/azim/azim_orthographic) |
| **G**{{ lon0 }}/{{ lat0 }}/*width*[**+a***azimuth*][**+t***tilt*][**+v***vwidth*/*vheight*][**+w***twist*][**+z***altitude*] | [General perspective](https://www.pygmt.org/latest/projections/azim/azim_general_perspective) |
| **H**[{{ lon0 }}/]*width* | [Hammer equal area](https://www.pygmt.org/latest/projections/misc/misc_hammer) |
| **I**[{{ lon0 }}/]*width* | [Sinusoidal equal area](https://www.pygmt.org/latest/projections/misc/misc_sinusoidal) |
| **J**[{{ lon0 }}/]*width* | [Miller cylindrical](https://www.pygmt.org/latest/projections/cyl/cyl_miller) |
| **Kf**[{{ lon0 }}/]*width* | [Eckert IV equal area](https://www.pygmt.org/latest/projections/misc/misc_eckertIV) |
| **Ks**[{{ lon0 }}/]*width* | [Eckert VI equal area](https://www.pygmt.org/latest/projections/misc/misc_eckertVI) |
| **L**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Lambert conic conformal](https://www.pygmt.org/latest/projections/conic/conic_lambert) |
| **M**[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Mercator cylindrical](https://www.pygmt.org/latest/projections/cyl/cyl_mercator) |
| **N**[{{ lon0 }}/]*width* | [Robinson](https://www.pygmt.org/latest/projections/misc/misc_robinson) |
| **Oa**{{ lon0 }}/{{ lat0 }}/*azimuth*/*width*[**+v**] | [Oblique Mercator, 1: origin and azimuth](https://www.pygmt.org/latest/projections/cyl/cyl_oblique_mercator_1) |
| **Ob**{{ lon0 }}/{{ lat0 }}/lon1/{{ lat1 }}/*width*[**+v**] | [Oblique Mercator, 2: two points](https://www.pygmt.org/latest/projections/cyl/cyl_oblique_mercator_2) |
| **Oc**{{ lon0 }}/{{ lat0 }}/lonp/{{ latp }}/*width*[**+v**] | [Oblique Mercator, 3: origin and pole](https://www.pygmt.org/latest/projections/cyl/cyl_oblique_mercator_3) |
| **P**\ *width*[**+a**][**+f**[**e**\|**p**\|*radius*]][**+r***offset*][**+t***origin*][**+z**[**p***radius*]] | [Polar](https://www.pygmt.org/latest/projections/nongeo/polar) [azimuthal] (`\theta`, `r`) (or cylindrical) |
| **Poly**/[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Polyconic](https://www.pygmt.org/latest/projections/conic/polyconic) |
| **Q**[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Equidistant cylindrica](https://www.pygmt.org/latest/projections/cyl/cyl_equidistant) |
| **R**[{{ lon0 }}/]*width* | [Winkel Tripel](https://www.pygmt.org/latest/projections/misc/misc_winkel_tripel) |
| **S**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [General stereographic](https://www.pygmt.org/latest/projections/azim/azim_general_stereographic) |
| **T**{{ lon0 }}[/{{ lat0 }}]/*width* | [Transverse Mercator](https://www.pygmt.org/latest/projections/cyl/cyl_transverse_mercator) |
| **U***zone*/*width* | [Universal Transverse Mercator (UTM)](https://www.pygmt.org/latest/projections/cyl/cyl_universal_transverse_mercator) |
| **V**[{{ lon0 }}/]*width* | [Van der Grinten](https://www.pygmt.org/latest/projections/misc/misc_van_der_grinten) |
| **W**[{{ lon0 }}/]*width* | [Mollweide](https://www.pygmt.org/latest/projections/misc/misc_mollweide) |
| **X**\ *width*[**l**\|\ **p**\ *exp*\|\ **T**\|\ **t**][/*height*[**l**\|\ **p**\|\ *exp*\|\ **T**\|\ **t**]][**d**] | [Linear](https://www.pygmt.org/latest/projections/nongeo/cartesian_linear), [logarithmic](https://www.pygmt.org/latest/projections/nongeo/cartesian_logarithmic), [power](https://www.pygmt.org/latest/projections/nongeo/cartesian_power), and time |
| **Y**{{ lon0 }}/{{ lat0 }}/*width* | [Cylindrical equal area](https://www.pygmt.org/latest/projections/cyl/cyl_equal_area) |
