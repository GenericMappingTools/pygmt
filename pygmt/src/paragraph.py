import io

from pygmt.clib import Session


def paragraph(
    self,
    x,
    y,
    text,
    parwidth,
    font="12p,Helvetica,black",
    angle=0,
    justify="BL",
    linespacing=1.0,
    alignment="left",
    **kwargs,
):
    kwargs = self._preprocess(**kwargs)

    header = [x, y, linespacing, parwidth, alignment[0]]
    stringio = io.StringIO()
    stringio.write("> " + " ".join([str(i) for i in header]) + "\n")
    stringio.write(text)

    with Session() as lib:
        with lib.virtualfile_from_stringio(stringio) as vfile:
            lib.call_module("text", [vfile, "-M", "-F+a30"])
