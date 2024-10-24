import io

from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def _parse_font_angle_justify(font, angle, justify):
    string = [
        f"{flag}{arg}"
        for arg, flag in [(font, "+f"), (angle, "+a"), (justify, "+j")]
        if arg is not None
    ]
    return "".join(string) if len(string) != 0 else None


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
    kwargs["F"] = _parse_font_angle_justify(font, angle, justify)
    kwargs["M"] = True
    with Session() as lib:
        with lib.virtualfile_from_stringio(stringio) as vfile:
            lib.call_module("text", args=build_arg_list(kwargs, infile=vfile))
