"""
Cylindrical Stereographic
=========================

``Cyl_stere/[lon0/][lat0/]width``: Give central meridian ``lon0`` (optional) and
standard parallel ``lat0`` (optional). The standard parallel is typically one of these
(but can be any value):

* 66.159467 - Miller's modified Gall
* 55 - Kamenetskiy's First
* 45 - Gall's Stereographic
* 30 - Bolshoi Sovietskii Atlas Mira or Kamenetskiy's Second
* 0 - Braun's Cylindrical

"""
import pygmt

fig = pygmt.Figure()
fig.coast(region="g", frame="afg", land="gray", projection="Cyl_stere/30/-20/8i")
fig.show()
