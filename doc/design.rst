.. _design:

Design
======


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
        gmt grdimage -Ct.cpt -Iintens.nc data.nc -JM6i
        gmt coast -Rdata.nc -Dh -Baf -W0.75p
        echo "Japan Trench" | gmt text -F+f32p+cTC -Dj0/0.2i -Gwhite
        gmt plot -W2p lines.txt
        gmt colorbar -DjBL+w3i/0.1i+h+o0.3i/0.4i -Ct.cpt -W0.001 -F+gwhite+p0.5p -Bxaf -By+l"km"
    # When a session ends, GMT will fetch the map it produced and convert it to
    # PDF automatically. The file will be named after the session "map.pdf"
    gmt end

This is a great improvement: the code is smaller and more readable. It fits
naturally with Python :ref:`context managers <context-managers>` and can
be used to embed PNG converted output into Jupyter notebooks when ``gmt end``
is called.

Read more about modern mode at the
`Modernization wiki page <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.



GMT Python
----------

``gmt-python`` is made for the future. We will support **only Python 3.5 or
later** and require the `new "modern" mode of GMT <http://gmt.soest.hawaii.edu/boards/2/topics/4930>`__
(currently only in the ``trunk`` of the SVN repository).
The ``modern`` mode removes the need for ``-O -K`` and explicitly redirecting
to a ``.ps`` file.
This all happens in the background.
A final call to ``gmt end`` brings the plot out of hiding and finalizes
the Postscript.
This mode is perfect for the Python interface, which would have to handle
generation of the Postscript file in the background anyway.

We will wrap the GMT C API using the :py:mod:`ctypes` module of the Python
standard library.
:py:mod:`ctypes` grants access to C data types and foreign functions in DDLs and
shared libraries, making it possible to wrap these libraries with pure Python
code.
Not having compiled modules makes packaging and distribution of Python software
a lot easier.

Wrappers for GMT data types and C functions will be implemented in a lower
level wrapper library.
These will be direct :py:mod:`ctypes` wrappers of the GMT module functions and any
other function that is needed on the Python side.
The low-level functions will not handle any data type conversion or setting up
of argument list.

We'll also provide higher level functions that mirror all GMT modules.
These functions will be built on top of the low-level library and will handle
all data conversions and parsing of arguments.
This is the part of the library with which the user will interact (the GMT
Python API).


The GMT Python API
------------------

Each GMT module has a function in the ``gmt`` package.
Command-line arguments are passes as function keyword arguments.
Data can be passed as file names or in-memory data.

The simplest usage would be with data in a file and generating a PDF output
figure, just as a normal GMT script::

    import gmt

    fig = gmt.Figure()
    cpt = gmt.makecpt(C='cubhelix', T=[-4500, 4500])
    fig.grdimage(input='grid.nc', J='M6i', B='af', P=True, C=cpt)
    fig.colorbar(C=cpt, D='jTC+w6i/0.2i+h+e+o0/1i', B='af')
    fig.savefig("my-figure.pdf")

Arguments can also be passed as in the GMT command-line by using a single
string::

    import gmt

    fig = gmt.Figure()
    gmt.makecpt('-Ccubhelix -T-4500/4500', output='my.cpt')
    fig.grdimage('grid.nc -JM6i -Baf -P -Cmy.cpt')
    fig.colorbar('-Cmy.cpt -DjTC+w6i/0.2i+h+e+o0/1i -Baf')
    fig.savefig("my-figure.pdf")

Notice that output that would be redirected to a file is specified using the
``output`` keyword argument.

You can also pass in data from Python.
Grids in netCDF format are passed as xarray ``Datasets`` that can come from a
netCDF file or generated in memory::

    import gmt
    import xarray as xr

    data = xr.open_dataset('grid.nc')

    cpt = gmt.makecpt(C='cubhelix', T='-4500/4500')
    fig = gmt.Figure()
    fig.grdimage(input=data, J='M6i', B='af', P=True, C=cpt)
    fig.savefig('my-figure.pdf')

Tabular data can be passed as numpy arrays::

    import numpy as np
    import gmt

    data = np.loadtxt('data_file.csv')

    cpt = gmt.makecpt(C="red,green,blue", T="0,70,300,10000")
    fig = gmt.Figure()
    fig.coast(R='g', J='N180/10i', G='bisque', S='azure1', B='af', X='c')
    fig.plot(input=data, S='ci', C=cpt, h='i1', i='2,1,3,4+s0.02')
    fig.savefig('my-figure.pdf')


In the Jupyter notebook, we can preview the plot by calling ``gmt.show()``,
which embeds the image in the notebook::

    import numpy as np
    import gmt

    data = np.loadtxt('data_file.csv')

    cpt = gmt.makecpt(C="red,green,blue", T="0,70,300,10000")
    fig = gmt.Figure()
    fig.coast(R='g', J='N180/10i', G='bisque', S='azure1', B='af', X='c')
    fig.plot(input=data, S='ci', C=cpt, h='i1', i='2,1,3,4+s0.02')
    gmt.show()

``gmt.show`` will call ``psconvert`` in the background to get a PNG image back
and use ``IPython.display.Image`` to insert it into the notebook.

**TODO**: We're still thinking of the best way to call ``gmt.psconvert`` first
to generate a high-quality PDF and right after call ``gmt.show()`` for an
inline preview.
The issue is that ``psconvert`` deletes the temporary Postscript file that was
being constructed on the background, this calling it a second time through
``gmt.show()`` would not work.
Any suggestions are welcome!


Package organization
--------------------

The general layout of the Python package will probably look something like
this::


    gmt/
        clib/     # Package with low-level wrappers for the C API
            ...
        modules/  # Defines the functions corresponding to GMT modules
            ...


The module functions
--------------------

The functions corresponding to GMT modules (``pscoast``, ``psconvert``, etc)
are how the user interacts with the Python API.
They will be organized in different files in the ``gmt.modules`` package but
will all be accessible from the ``gmt`` package namespace.
For example, ``pscoast`` can live in ``gmt/modules/ps_generating.py`` but can
be called as ``gmt.pscoast``.

Here is what a module function will look like::

    def module_function(**kwargs):
        """
        Docstring explaining what each option is and all the aliases.

        Likely derived from the GMT documentation.
        """
        # Convert any inputs into things the C API can digest
        ...
        # Parse the keyword arguments and make an "args" list
        ...
        # Call the module function from the C API with the inputs
        ...
        # Process any outputs from the C API into Python data types
        ...
        return output


We will automate this process as much as possible:

* Common options in the docstrings can be reused from an ``OPTIONS``
  dictionary.
* Parsing of common arguments (R, J, etc) can be done by a function.
* Creating the GMT session and calling the module can be automated.
* Conversion of inputs and outputs will most likely be: tables to numpy arrays,
  grids to xarray ``Datasets``, text to Python text.

Most of the work in this part will be wrapping all of the many GMT modules,
parsing non-standard options, and making sure the docstrings are accurate.
It might even be possible to automatically generate the docstrings or parts of
them from the command-line help messages by passing a Python callback as the
``print_func`` when creating a GMT session.


The low-level wrappers
----------------------

The low-level wrapper functions will be bare-bones :py:mod:`ctypes` foreign
functions from the ``libgmt.so`` shared library.
The functions can be accessed from Python like so::

    import ctypes as ct

    libgmt = ct.cdll.LoadLibrary("libgmt.so")

    # Functions are accessed as members of the 'libgmt' object
    GMT_Call_Module = libgmt.GMT_Call_Module

    # Call them like normal Python functions
    GMT_Call_Module(... inputs ...)


The tricky part is making sure the functions get the input types they need.
:py:mod:`ctypes` provides access to C data types and a way to specify the data
type conversions that the function requires::

    GMT_Call_Module.argstypes = [ct.c_void_p, ct.c_char_p, ct.c_int, ct.c_void_p]

This is fine for standard data types like ``int``, ``char``, etc, but will need
extra work for custom GMT ``struct``.
These data types will need to be wrapped by Python classes that inherit from
:py:class:`ctypes.Structure`.

The ``gmt.c_api`` module will expose these foreign functions (with output and
input types specified) and GMT data types for the modules to use.

The main entry point into GMT will be through the ``GMT_Call_Module`` function.
This is what the ``gmt`` command-line application uses to run a given
module, like ``GMT_pscoast`` for example.
We will use it to run the modules from the Python side as well.
It has the following signature::

    int GMT_Call_Module (void *V_API, const char *module, int mode, void *args)

The arguments ``module``, ``mode``, and ``args`` (the command-line argument
list) are plain C types and can be generated easily using :py:mod:`ctypes`.
The Python module code will need to generate the ``args`` array from the
given function arguments.
The ``V_API`` argument is a "GMT Session" and is created through the
``GMT_Create_Session`` function, which will have to be wrapped as well.

The input and output of Python data will be handled through the GMT virtual
file machinery.
This allows us to write data to a memory location instead of a file without GMT
knowing the difference.
For input, we can use ``GMT_Open_VirtualFile`` and point it to the location in
memory of the Python data, for example using :attr:`numpy.ndarray.ctypes`.
We can also translate the Python data into :py:mod:`ctypes` compatible types.
The virtual file pointer can also be passed as the output option for the
module, for example as ``-G`` or through redirection (``->``).
We can read the contents of the virtual file using ``GMT_Read_VirtualFile``.

