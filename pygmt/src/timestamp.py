"""
timestamp - Plot the GMT timestamp logo.
"""
from packaging.version import Version
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, is_nonstr_iter

__doctest_skip__ = ["timestamp"]


def timestamp(
    self, label=None, justification="BL", offset=("-54p", "-54p"), font="Helvetica"
):
    """
    Plot the GMT timestamp logo.

    Parameters
    ----------
    label : str
        The text string shown after the GMT timestamp logo.
    justification : str
        Justification of the timestamp. *justification* is a two-character code
        that is a combination of a horizontal (**L**(eft), **C**(enter), or
        **R**(ight)) and a vertical (**T**(op), **M**(iddle), or **B**(ottom))
        code.
    offset : str or list
        (*offset_x*, *offset_y*) or *offset*.
        Offset the anchor point of the timestamp by *offset_x* and *offset_y*.
        If a single value *offset* is given, *offset_y*=*offset_x*=*offset*.
    font : str
        Font name or font number of the timestamp and the optional label .

    Examples
    --------
    >>> # Plot the GMT timestamp logo.
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.timestamp()
    >>> fig.show()

    >>> # Plot the GMT timestamp logo with a custom label.
    >>> fig = pygmt.Figure()
    >>> fig.timestamp(label="Powered by PyGMT")
    >>> fig.show()
    """
    self._preprocess()  # pylint: disable=protected-access

    kwdict = {}
    kwdict["T"] = True  # pass the -T option to the plot module
    kwdict["U"] = True

    # build the argument for the -U option
    label = "" if label is None else f"{label}"
    kwdict["U"] = f"{label}+j{justification}"

    if is_nonstr_iter(offset):  # given a list
        kwdict["U"] += "+o" + "/".join(f"{item}" for item in offset)
    else:
        kwdict["U"] += f"+o{offset}"
        if "/" not in offset:
            # Giving a single offset doesn't work in GMT <= 6.4.0.
            # See https://github.com/GenericMappingTools/gmt/issues/7107.
            with Session() as lib:
                if Version(lib.info["version"]) < Version("6.5.0"):
                    kwdict["U"] += "/{offset}"

    with Session() as lib:
        lib.call_module(
            module="plot", args=build_arg_string(kwdict) + f" --FONT_LOGO={font}"
        )
