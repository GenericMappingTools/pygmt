"""
timestamp - Plot the GMT timestamp logo.
"""
from packaging.version import Version
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_string, is_nonstr_iter

__doctest_skip__ = ["timestamp"]


def timestamp(
    self,
    text=None,
    label=None,
    justification="BL",
    offset=("-54p", "-54p"),
    font="Helvetica",
):
    """
    Plot the GMT timestamp logo.

    Parameters
    ----------
    text : None or str
        If ``None``, the current UNIX time stamp is shown in the GMT timestamp
        logo. Setting this parameter to replace the UNIX time stamp with a
        custom text string instead. The text must be less than 64 characters.
        *Requires GMT>=6.5.0*.
    label : None or str
        The text string shown after the GMT timestamp logo.
    justification : str
        Justification of the timestamp. *justification* is a two-character code
        that is a combination of a horizontal (**L**(eft), **C**(enter), or
        **R**(ight)) and a vertical (**T**(op), **M**(iddle), or **B**(ottom))
        code.
    offset : str or tuple
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point of the timestamp by *offset_x* and *offset_y*.
        If a single value *offset* is given, *offset_y*=*offset_x*=*offset*.
    font : str
        Font of the timestamp and the optional label.
        For GMT<=6.4.0, this parameter can only change the font style.
        For GMT>=6.5.0, this parameter can change the font style and font color.

    Examples
    --------
    >>> # Plot the GMT timestamp logo.
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.timestamp()
    >>> fig.show()
    <IPython.core.display.Image object>

    >>> # Plot the GMT timestamp logo with a custom label.
    >>> fig = pygmt.Figure()
    >>> fig.timestamp(label="Powered by PyGMT")
    >>> fig.show()
    <IPython.core.display.Image object>
    """
    self._preprocess()  # pylint: disable=protected-access

    # Build the options passed to the "plot" module
    kwdict = dict(T=True, U="")
    if label is not None:
        kwdict["U"] += f"{label}"
    kwdict["U"] += f"+j{justification}"

    # Deal with compatibility with different GMT versions
    with Session() as lib:
        gmt_version = lib.info["version"]

    if is_nonstr_iter(offset):  # given a tuple
        kwdict["U"] += "+o" + "/".join(f"{item}" for item in offset)
    else:  # given a single value
        if "/" not in offset and Version(gmt_version) <= Version("6.4.0"):
            # Giving a single offset doesn't work in GMT <= 6.4.0.
            # See https://github.com/GenericMappingTools/gmt/issues/7107.
            kwdict["U"] += f"+o{offset}/{offset}"
        else:
            kwdict["U"] += f"+o{offset}"

    # The +t modifier was added in GMT 6.5.0.
    # See https://github.com/GenericMappingTools/gmt/pull/7127.
    if text is not None:
        if Version(gmt_version) <= Version("6.4.0"):
            raise GMTInvalidInput("The parameter 'text' requires GMT>=6.5.0.")
        kwdict["U"] += f"+t{text}"

    with Session() as lib:
        lib.call_module(
            module="plot", args=build_arg_string(kwdict) + f" --FONT_LOGO={font}"
        )
