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
| **A**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | [](/projections/azim/azim_lambert.rst) |
| **B**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | [](/projections/conic/conic_albers.rst) |
| **C**{{ lon0 }}/{{ lat0 }}/*width*                          | [](/projections/cyl/cyl_cassini.rst) |
| **Cyl_stere**/[{{ lon0 }}/[{{ lat0 }}/]]*width*             | [](/projections/cyl/cyl_stereographic.rst) |
| **D**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | [](/projections/conic/conic_equidistant.rst) |
| **E**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | [](/projections/azim/azim_equidistant.rst) |
| **F**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | [](/projections/azim/azim_gnomonic.rst) |
| **G**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | [](/projections/azim/azim_orthographic.rst) |
| **G**{{ lon0 }}/{{ lat0 }}/*width*[**+a***azimuth*][**+t***tilt*][**+v***vwidth*/*vheight*][**+w***twist*][**+z***altitude*] | [](/projections/azim/azim_general_perspective.rst) |
| **H**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_hammer.rst) |
| **I**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_sinusoidal.rst) |
| **J**[{{ lon0 }}/]*width*                                   | [](/projections/cyl/cyl_miller.rst) |
| **Kf**[{{ lon0 }}/]*width*                                  | [](/projections/misc/misc_eckertIV.rst) |
| **Ks**[{{ lon0 }}/]*width*                                  | [](/projections/misc/misc_eckertVI.rst) |
| **L**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | [](/projections/conic/conic_lambert.rst) |
| **M**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | [](/projections/cyl/cyl_mercator.rst) |
| **N**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_robinson.rst) |
| **Oa**{{ lon0 }}/{{ lat0 }}/*azimuth*/*width*[**+v**]             | Oblique Mercator projection: [1. origin and azimuth](/projections/cyl/cyl_oblique_mercator.rst) |
| **Ob**{{ lon0 }}/{{ lat0 }}/{{ lon1 }}/{{ lat1 }}/*width*[**+v**] | Oblique Mercator projection: [2. two points](/projections/cyl/cyl_oblique_mercator.rst) |
| **Oc**{{ lon0 }}/{{ lat0 }}/{{ lonp }}/{{ latp }}/*width*[**+v**] | Oblique Mercator projection: [3. origin and projection pole](/projections/cyl/cyl_oblique_mercator.rst) |
| **P***width*[**+a**][**+f**[**e**\|**p**\|*radius*]][**+r***offset*][**+t***origin*][**+z**[**p**\|*radius*]] | Polar [azimuthal](/projections/nongeo/polar.rst) ({math}`\theta, r`) or cylindrical |
| **Poly**/[{{ lon0 }}/[{{ lat0 }}/]]*width*                  | [](/projections/conic/polyconic.rst) |
| **Q**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | [](/projections/cyl/cyl_equidistant.rst) |
| **R**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_winkel_tripel.rst) |
| **S**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | [](/projections/azim/azim_general_stereographic.rst) |
| **T**{{ lon0 }}[/{{ lat0 }}]/*width*                        | [](/projections/cyl/cyl_transverse_mercator.rst) |
| **U***zone*/*width*                                         | [](/projections/cyl/cyl_universal_transverse_mercator.rst) |
| **V**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_van_der_grinten.rst) |
| **W**[{{ lon0 }}/]*width*                                   | [](/projections/misc/misc_mollweide.rst) |
| **X***width*[**l**\|**p***exp*\|**T**\|**t**][/*height*[**l**\|**p***exp*\|**T**\|**t**]][**d**] | Cartesian [linear](/projections/nongeo/cartesian_linear.rst), [logarithmic](/projections/nongeo/cartesian_logarithmic.rst), [power](/projections/nongeo/cartesian_power.rst), and time |
| **Y**{{ lon0 }}/{{ lat0 }}/*width*                          | [](/projections/cyl/cyl_equal_area.rst) |
