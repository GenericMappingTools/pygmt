GMT Python
==================================

**A Python interface for the Generic Mapping Tools**


Disclaimer
----------

**This package in early stages of design and implementation.**

We welcome any feedback and ideas!
Code contributions are also very welcome.
Let us know by submitting
`issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__
or send us a message on `our Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.


Previous work
-------------

To my knowledge, there have been 3 attempts at a GMT Python interface:

* `gmtpy <https://github.com/emolch/gmtpy>`__ by
  `Sebastian Heimann <https://github.com/emolch>`__
* `pygmt <https://github.com/ian-r-rose/pygmt>`__ by
  `Ian Rose <https://github.com/ian-r-rose>`__
* `PyGMT <https://github.com/glimmer-cism/PyGMT>`__  by
  `Magnus Hagdorn <https://github.com/mhagdorn>`__

Only ``gmtpy`` has received commits since 2014 and is the more mature
alternative.
However, the project `doesn't seem to be very activate
<https://github.com/emolch/gmtpy/graphs/contributors>`__.
Both ``gmtpy`` and ``PyGMT`` use system class (through ``subprocess.Popen``)
and pass input and output through ``subprocess.PIPE``.
``pygmt`` seems to call the GMT C API directly through a hand-coded Python C
extension.
This might compromise the portability of the package across operating systems
and makes distribution very painful.

We aim to learn from these attempts and create a library that interfaces with
the C API and provides a Pythonic API for GMT.


Goals
-----

* Provide access to GMT modules from Python using the GMT C API (no system
  calls).
* API design familiar for veteran GMT users (arguments ``R``,
  ``J``, etc) with more newbie-friendly alternatives/aliases
  (``region=[10, 20, -30, -10]``,  ``projection='M'``, etc).
* Input and output using Python native containers: numpy ``ndarray`` or pandas
  ``DataFrame`` for data tables and `xarray <http://xarray.pydata.org>`__
  ``Dataset`` for netCDF grids.
* Integration with the `Jupyter notebook <http://jupyter.org/>`__ to display
  plots and maps inline.
* Built around the new `GMT modern mode
  <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.


About modern mode
-----------------

GMT is introducing a "modern" execution mode that reduces the amount of
arguments needed for many programs and handles the PostScript building in the
background. ``gmt-python`` will be based strongly on modern mode but will also
allow the classic syntax.

For example, the following classic mode script that creates a PDF map::


    # Shading grid and color pallete
    gmt grdgradient -Nt0.2 -A45 data.nc -Gintens.nc
    gmt makecpt -Cgeo -T-8000/2000 > t.cpt
    # Build the map, one layer at a time
    gmt grdimage -Ct.cpt -Iintens.nc data.nc -JM6i -P -K > map.ps
    gmt pscoast -Rdata.nc -J -O -Dh -Baf -W0.75p -K >> map.ps
    echo "Japan Trench" | gmt pstext -F+f32p+cTC -Dj0/0.2i -Gwhite -R -J -O -K >> map.ps
    gmt psxy -W2p lines.txt -R -J -O -K >> map.ps
    gmt psscale -R -J -O -DjBL+w3i/0.1i+h+o0.3i/0.4i -Ct.cpt -W0.001 -F+gwhite+p0.5p -Bxaf -By+l"km" >> map.ps
    # Convert the PostScript map to PDF
    gmt psconvert maps.ps -Tf

is equivalent to the following in modern mode::

    # Start a new session named "map" that will produce PDF output
    gmt begin map pdf
        # Same thing but no redirecting and -R -J -O -K
        gmt grdgradient -Nt0.2 -A45 data.nc -Gintens.nc
        gmt makecpt -Cgeo -T-8000/2000 > t.cpt
        gmt grdimage -Ct.cpt -Iintens.nc data.nc -JM6i -P
        gmt pscoast -Rdata.nc -Dh -Baf -W0.75p
        echo "Japan Trench" | gmt pstext -F+f32p+cTC -Dj0/0.2i -Gwhite
        gmt psxy -W2p lines.txt
        gmt psscale -DjBL+w3i/0.1i+h+o0.3i/0.4i -Ct.cpt -W0.001 -F+gwhite+p0.5p -Bxaf -By+l"km"
    # When a session ends, GMT will fetch the map it produced and convert it to
    # PDF automatically. The file will be named after the session "map.pdf"
    gmt end

This is a great improvement: the code is smaller and more readable. It fits
naturally with Python `context managers
<https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`__ and can
be used to embed PNG converted output into Jupyter notebooks when ``gmt end``
is called.

Read more about modern mode at the
`Modernization wiki page <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.


.. toctree::
    :maxdepth: 2
    :hidden:

    install.rst
    design.rst
    api.rst
    contribute.rst
    license.rst
