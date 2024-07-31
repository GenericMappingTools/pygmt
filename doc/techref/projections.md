---
myst:
  substitutions:
    lon0: "lon{sub}`0`",
    lat0: "lat{sub}`0`",
    lon1: "lon{sub}`1`",
    lat1: "lat{sub}`1`",
    lat2: "lat{sub}`2`",
    lonp: "lon{sub}`p`",
    latp: "lat{sub}`p`",
    url_doc_proj: "https://www.pygmt.org/latest/projections/",
---

# GMT Map Projections

The table below shows the projection codes for the 31 GMT projections:

| PyGMT Projection Argument | Projection Name |
| --- | --- |
| **A**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {{ '[Lambert azimuthal equal area]({}azim/azim_equidistant.html)'.format(url_doc_proj) }} |
| **B**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {{ '[Albers conic equal area]({}conic/conic_albers.html)'.format(url_doc_proj) }} |
| **C**{{ lon0 }}/{{ lat0 }}/*width*                          | {{ '[Cassini cylindrical]({}cyl/cyl_cassini.html)'.format(url_doc_proj) }} |
| **Cyl_stere**/[{{ lon0 }}/[{{ lat0 }}/]]*width*             | {{ '[Cylindrical stereographic]({}cyl/cyl_stereographic.html)'.format(url_doc_proj) }} |
| **D**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {{ '[Equidistant conic]({}conic/conic_equidistant)'.format(url_doc_proj) }} |
| **E**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {{ '[Azimuthal equidistant]({}azim/azim_equidistant)'.format(url_doc_proj) }} |
| **F**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {{ '[Azimuthal gnomonic]({}azim/azim_gnomonic)'.format(url_doc_proj) }} |
| **G**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {{ '[Azimuthal orthographic]({}azim/azim_orthographic)'.format(url_doc_proj) }} |
| **G**{{ lon0 }}/{{ lat0 }}/*width*[**+a***azimuth*][**+t***tilt*][**+v***vwidth*/*vheight*][**+w***twist*][**+z***altitude*] | {{ '[General perspective]({}azim/azim_general_perspective)'.format(url_doc_proj) }} |
| **H**[{{ lon0 }}/]*width*                                   | {{ '[Hammer equal area]({}misc/misc_hammer)'.format(url_doc_proj) }} |
| **I**[{{ lon0 }}/]*width*                                   | {{ '[Sinusoidal equal area]({}misc/misc_sinusoidal)'.format(url_doc_proj) }} |
| **J**[{{ lon0 }}/]*width*                                   | {{ '[Miller cylindrical]({}cyl/cyl_miller)'.format(url_doc_proj) }} |
| **Kf**[{{ lon0 }}/]*width*                                  | {{ '[Eckert IV equal area]({}misc/misc_eckertIV)'.format(url_doc_proj) }} |
| **Ks**[{{ lon0 }}/]*width*                                  | {{ '[Eckert VI equal area]({}misc/misc_eckertVI)'.format(url_doc_proj) }} |
| **L**{{ lon0 }}/{{ lat0 }}/{{ lat1 }}/{{ lat2 }}/*width*    | {{ '[Lambert conic conformal]({}conic/conic_lambert)'.format(url_doc_proj) }} |
| **M**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | {{ '[Mercator cylindrical]({}cyl/cyl_mercator)'.format(url_doc_proj) }} |
| **N**[{{ lon0 }}/]*width*                                   | {{ '[Robinson]({}misc/misc_robinson)'.format(url_doc_proj) }} |
| **Oa**{{ lon0 }}/{{ lat0 }}/*azimuth*/*width*[**+v**]       | {{ '[Oblique Mercator, 1: origin and azimuth]({}cyl/cyl_oblique_mercator_1)'.format(url_doc_proj) }} |
| **Ob**{{ lon0 }}/{{ lat0 }}/lon1/{{ lat1 }}/*width*[**+v**] | {{ '[Oblique Mercator, 2: two points]({}cyl/cyl_oblique_mercator_2)'.format(url_doc_proj) }} |
| **Oc**{{ lon0 }}/{{ lat0 }}/lonp/{{ latp }}/*width*[**+v**] | {{ '[Oblique Mercator, 3: origin and pole]({}cyl/cyl_oblique_mercator_3)'.format(url_doc_proj) }} |
| **P***width*[**+a**][**+f**[**e**\|**p**\|*radius*]][**+r***offset*][**+t***origin*][**+z**[**p***radius*]] | {{ '[Polar]({}nongeo/polar)'.format(url_doc_proj) }} [azimuthal] ({math}`\theta, r`) (or cylindrical)|
| **Poly**/[{{ lon0 }}/[{{ lat0 }}/]]*width*                  | {{ '[Polyconic]({}conic/polyconic)'.format(url_doc_proj) }} |
| **Q**[{{ lon0 }}/[{{ lat0 }}/]]*width*                      | {{ '[Equidistant cylindrica]({}cyl/cyl_equidistant)'.format(url_doc_proj) }} |
| **R**[{{ lon0 }}/]*width*                                   | {{ '[Winkel Tripel]({}misc/misc_winkel_tripel)'.format(url_doc_proj) }} |
| **S**{{ lon0 }}/{{ lat0 }}[/*horizon*]/*width*              | {{ '[General stereographic]({}azim/azim_general_stereographic)'.format(url_doc_proj) }} |
| **T**{{ lon0 }}[/{{ lat0 }}]/*width*                        | {{ '[Transverse Mercator]({}cyl/cyl_transverse_mercator)'.format(url_doc_proj) }} |
| **U***zone*/*width*                                         | {{ '[Universal Transverse Mercator (UTM)]({}cyl/cyl_universal_transverse_mercator)'.format(url_doc_proj) }} |
| **V**[{{ lon0 }}/]*width*                                   | {{ '[Van der Grinten]({}misc/misc_van_der_grinten)'.format(url_doc_proj) }} |
| **W**[{{ lon0 }}/]*width*                                   | {{ '[Mollweide]({}misc/misc_mollweide)'.format(url_doc_proj) }} |
| **X***width*[**l**\|**p***exp*\|**T**\|**t**][/*height*[**l**\|**p**\|*exp*\|**T**\|**t**]][**d**] | {{ '[Linear]({}nongeo/cartesian_linear)'.format(url_doc_proj) }} , {{ '[logarithmic]({}nongeo/cartesian_logarithmic)'.format(url_doc_proj) }} , {{ '[power]({}nongeo/cartesian_power)'.format(url_doc_proj) }} , and time |
| **Y**{{ lon0 }}/{{ lat0 }}/*width*                          | {{ '[Cylindrical equal area]({}cyl/cyl_equal_area)'.format(url_doc_proj) }} |
