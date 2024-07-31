# GMT Map Projections

The table below shows the projection codes for the 31 GMT projections:

| PyGMT Projection Argument | Projection Name |
| --- | --- |
| **A**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Lambert azimuthal equal area]({{ url_doc_proj }}azim/azim_equidistant.html) |
| **B**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Albers conic equal area]({{ url_doc_proj }}conic/conic_albers.html) |
| **C**{{ lon0 }}/{{ lat0 }}/*width* | [Cassini cylindrical]({{ url_doc_proj }}cyl/cyl_cassini.html) |
| **Cyl_stere**/[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Cylindrical stereographic]({{ url_doc_proj }}cyl/cyl_stereographic.html) |
| **D**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Equidistant conic]({{ url_doc_proj }}conic/conic_equidistant) |
| **E**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal equidistant]({{ url_doc_proj }}azim/azim_equidistant) |
| **F**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal gnomonic]({{ url_doc_proj }}azim/azim_gnomonic) |
| **G**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [Azimuthal orthographic]({{ url_doc_proj }}azim/azim_orthographic) |
| **G**{{ lon0 }}/{{ lat0 }}/*width*[**+a***azimuth*][**+t***tilt*][**+v***vwidth*/*vheight*][**+w***twist*][**+z***altitude*] | [General perspective]({{ url_doc_proj }}azim/azim_general_perspective) |
| **H**[{{ lon0 }}/]*width* | [Hammer equal area]({{ url_doc_proj }}misc/misc_hammer) |
| **I**[{{ lon0 }}/]*width* | [Sinusoidal equal area]({{ url_doc_proj }}misc/misc_sinusoidal) |
| **J**[{{ lon0 }}/]*width* | [Miller cylindrical]({{ url_doc_proj }}cyl/cyl_miller) |
| **Kf**[{{ lon0 }}/]*width* | [Eckert IV equal area]({{ url_doc_proj }}misc/misc_eckertIV) |
| **Ks**[{{ lon0 }}/]*width* | [Eckert VI equal area]({{ url_doc_proj }}misc/misc_eckertVI) |
| **L**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width* | [Lambert conic conformal]({{ url_doc_proj }}conic/conic_lambert) |
| **M**[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Mercator cylindrical]({{ url_doc_proj }}cyl/cyl_mercator) |
| **N**[{{ lon0 }}/]*width* | [Robinson]({{ url_doc_proj }}misc/misc_robinson) |
| **Oa**{{ lon0 }}/{{ lat0 }}/*azimuth*/*width*[**+v**] | [Oblique Mercator, 1: origin and azimuth]({{ url_doc_proj }}cyl/cyl_oblique_mercator_1) |
| **Ob**{{ lon0 }}/{{ lat0 }}/lon1/{{ lat1 }}/*width*[**+v**] | [Oblique Mercator, 2: two points]({{ url_doc_proj }}cyl/cyl_oblique_mercator_2) |
| **Oc**{{ lon0 }}/{{ lat0 }}/lonp/{{ latp }}/*width*[**+v**] | [Oblique Mercator, 3: origin and pole]({{ url_doc_proj }}cyl/cyl_oblique_mercator_3) |
| **P***width*[**+a**][**+f**[**e**\|**p**\|*radius*]][**+r***offset*][**+t***origin*][**+z**[**p***radius*]] | [Polar]({{ url_doc_proj }}nongeo/polar) [azimuthal] ({math}`\theta, r`) (or cylindrical) |
| **Poly**/[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Polyconic]({{ url_doc_proj }}conic/polyconic) |
| **Q**[{{ lon0 }}/[{{ lat0 }}/]]*width* | [Equidistant cylindrica]({{ url_doc_proj }}cyl/cyl_equidistant) |
| **R**[{{ lon0 }}/]*width* | [Winkel Tripel]({{ url_doc_proj }}misc/misc_winkel_tripel) |
| **S**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width* | [General stereographic]({{ url_doc_proj }}azim/azim_general_stereographic) |
| **T**{{ lon0 }}[/{{ lat0 }}]/*width* | [Transverse Mercator]({{ url_doc_proj }}cyl/cyl_transverse_mercator) |
| **U***zone*/*width* | [Universal Transverse Mercator (UTM)]({{ url_doc_proj }}cyl/cyl_universal_transverse_mercator) |
| **V**[{{ lon0 }}/]*width* | [Van der Grinten]({{ url_doc_proj }}misc/misc_van_der_grinten) |
| **W**[{{ lon0 }}/]*width* | [Mollweide]({{ url_doc_proj }}misc/misc_mollweide) |
| **X***width*[**l**\|**p***exp*\|**T**\|**t**][/*height*[**l**\|**p**\|*exp*\|**T**\|**t**]][**d**] | [Linear]({{ url_doc_proj }}nongeo/cartesian_linear), [logarithmic]({{ url_doc_proj }}nongeo/cartesian_logarithmic), [power]({{ url_doc_proj }}nongeo/cartesian_power), and time |
| **Y**{{ lon0 }}/{{ lat0 }}/*width* | [Cylindrical equal area]({{ url_doc_proj }}cyl/cyl_equal_area) |
