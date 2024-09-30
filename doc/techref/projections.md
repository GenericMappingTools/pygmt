---
myst:
  substitutions:
    lon0: "lon{sub}`0`"
    lat0: "lat{sub}`0`"
    lon1: "lon{sub}`1`"
    lat1: "lat{sub}`1`"
    lat2: "lat{sub}`2`"
    lonp: "lon{sub}`p`"
    latp: "lat{sub}`p`"
---

# GMT Map Projections

The table below shows the projection codes for the 31 GMT map projections:

| PyGMT Projection Argument | Projection Name |
| --- | --- |
| **A**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {doc}`/projections/azim/azim_lambert` |
| **B**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {doc}`/projections/conic/conic_albers` |
| **C**{{ lon0 }}/{{ lat0 }}/*width*                          | {doc}`/projections/cyl/cyl_cassini` |
| **Cyl_stere**/[{{ lon0 }}/[{{ lat0 }}/]]*width*             | {doc}`/projections/cyl/cyl_stereographic` |
| **D**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {doc}`/projections/conic/conic_equidistant` |
| **E**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {doc}`/projections/azim/azim_equidistant` |
| **F**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {doc}`/projections/azim/azim_gnomonic` |
| **G**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {doc}`/projections/azim/azim_orthographic` |
| **G**{{ lon0 }}/{{ lat0 }}/*width*[**+a***azimuth*][**+t***tilt*][**+v***vwidth*/*vheight*][**+w***twist*][**+z***altitude*] | {doc}`/projections/azim/azim_general_perspective` |
| **H**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_hammer` |
| **I**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_sinusoidal` |
| **J**[{{ lon0 }}/]*width*                                   | {doc}`/projections/cyl/cyl_miller` |
| **Kf**[{{ lon0 }}/]*width*                                  | {doc}`/projections/misc/misc_eckertIV` |
| **Ks**[{{ lon0 }}/]*width*                                  | {doc}`/projections/misc/misc_eckertVI` |
| **L**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {doc}`/projections/conic/conic_lambert` |
| **M**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | {doc}`/projections/cyl/cyl_mercator` |
| **N**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_robinson` |
| **Oa**{{ lon0 }}/{{ lat0 }}/*azimuth*/*width*[**+v**]             | Oblique Mercator projection: {doc}`1. origin and azimuth </projections/cyl/cyl_oblique_mercator>` |
| **Ob**{{ lon0 }}/{{ lat0 }}/{{ lon1 }}/{{ lat1 }}/*width*[**+v**] | Oblique Mercator projection: {doc}`2. two points </projections/cyl/cyl_oblique_mercator>` |
| **Oc**{{ lon0 }}/{{ lat0 }}/{{ lonp }}/{{ latp }}/*width*[**+v**] | Oblique Mercator projection: {doc}`3. origin and projection pole </projections/cyl/cyl_oblique_mercator>` |
| **P***width*[**+a**][**+f**[**e**\|**p**\|*radius*]][**+r***offset*][**+t***origin*][**+z**[**p**\|*radius*]] | Polar {doc}`azimuthal </projections/nongeo/polar>` ({math}`\theta, r`) or cylindrical |
| **Poly**/[{{ lon0 }}/[{{ lat0 }}/]]*width*                  | {doc}`/projections/conic/polyconic` |
| **Q**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | {doc}`/projections/cyl/cyl_equidistant` |
| **R**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_winkel_tripel` |
| **S**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {doc}`/projections/azim/azim_general_stereographic` |
| **T**{{ lon0 }}[/{{ lat0 }}]/*width*                        | {doc}`/projections/cyl/cyl_transverse_mercator` |
| **U***zone*/*width*                                         | {doc}`/projections/cyl/cyl_universal_transverse_mercator` |
| **V**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_van_der_grinten` |
| **W**[{{ lon0 }}/]*width*                                   | {doc}`/projections/misc/misc_mollweide` |
| **X***width*[**l**\|**p***exp*\|**T**\|**t**][/*height*[**l**\|**p***exp*\|**T**\|**t**]][**d**] | Cartesian {doc}`linear </projections/nongeo/cartesian_linear>`, {doc}`logarithmic </projections/nongeo/cartesian_logarithmic>`, {doc}`power </projections/nongeo/cartesian_power>`, and time |
| **Y**{{ lon0 }}/{{ lat0 }}/*width*                          | {doc}`/projections/cyl/cyl_equal_area` |
