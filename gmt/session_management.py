"""
Session management modules: begin, end, figure, clean
"""
from . import clib


def begin(prefix='gmtsession', fmt='pdf'):
    """
    Initiate a new GMT session using modern mode.

    Used in combination with :func:`gmt.end`.

    Parameters
    ----------
    prefix : str
        The prefix to use for unnamed figures.
    fmt : str
        Sets the default plot format for the output figures.
        Choose one of these valid extensions:

        * bmp:       MicroSoft BitMap.
        * eps:       Encapsulated PostScript.
        * jpg:       Joint Photographic Experts Group format.
        * pdf:       Portable Document Format [Default].
        * png:       Portable Network Graphics.
        * ppm:       Portable Pixel Map.
        * ps:        PostScript.
        * tif:       Tagged Image Format File.
    """
    session = clib.create_session()
    clib.call_module(session, 'begin', '{} {}'.format(prefix, fmt))


def end():
    """
    Terminate GMT modern mode session and optionally  produce the figure files.

    Called after :func:`gmt.begin` and all commands that you want included in a
    session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``gmt.begin``), and bring the figures to the working directory.

    """
    session = clib.create_session()
    clib.call_module(session, 'end', '')


# Not working yet (perhaps bug in GMT).
def figure(prefix, formats='pdf', convertoptions='A,P'):
    """
    Start a new figure under a GMT modern mode session.

    Must be in a modern mode session (between calls to :func:`gmt.begin` and
    :func:`gmt.end`.

    Parameters
    ----------
    prefix : str
        The prefix to use for the next figure name.
    formats : str
        One or more comma-separated formats for the output figures.
        Choose from these valid extensions:

        * bmp:       MicroSoft BitMap.
        * eps:       Encapsulated PostScript.
        * jpg:       Joint Photographic Experts Group format.
        * pdf:       Portable Document Format [Default].
        * png:       Portable Network Graphics.
        * ppm:       Portable Pixel Map.
        * ps:        PostScript.
        * tif:       Tagged Image Format File.

    convertoptions : str
        One or more comma-separated options that will be passed to
        :func:`gmt.psconvert` when preparing the figures.
        The subset of valid options are:
        ``'A[<args>],C<args>,D<dir>,E<dpi>,P,Q<args>,S'``.

    """
    session = clib.create_session()
    args = '{} {} {}'.format(prefix, formats, convertoptions)
    clib.call_module(session, 'figure', args)
