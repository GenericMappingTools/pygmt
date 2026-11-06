"""
legendspec - Build a legend specification for Figure.legend.
"""

import io


def _fmt(value: float | str | None) -> str:
    """
    Format a value for a legend record.

    >>> _fmt(1.0)
    '1.0'
    >>> _fmt("1.0c")
    '1.0c'
    >>> _fmt(None)
    '-'
    """
    return "-" if value is None else str(value)


class LegendSpec:
    """
    A legend specification for :meth:`pygmt.Figure.legend`.
    """

    def __init__(self) -> None:
        self.records: list[str] = []

    def _append(self, record: str):
        """
        Append one record.
        """
        self.records.append(record)

    def add_header(self, text: str, font: str | None = None):
        """
        Add a centered header (``H``) [Default font is :gmt-term:`FONT_TITLE`].
        """
        return self._append(f"H {_fmt(font)} {text}")

    def add_symbol(
        self,
        symbol: str,
        size: float | str,
        fill: str | None = None,
        pen: str | None = None,
        label: str | None = None,
        dx1: float | str | None = None,
        dx2: float | str | None = None,
    ):
        """
        Add a symbol, with an optional explanatory ``label``.

        ``dx1`` is the offset of the symbol from the left margin of the column and
        ``dx2`` the offset of the label; both are computed by GMT if not given.
        """
        args = ["S", _fmt(dx1), symbol, f"{size}", _fmt(fill), _fmt(pen)]
        if label is not None:
            args += [_fmt(dx2), f"{label}"]
        self._append(" ".join(args))

    def add_line(
        self,
        pen: str | None = None,
        length: float | str | None = None,
        label: str | None = None,
        dx1: float | str | None = None,
        dx2: float | str | None = None,
    ):
        """
        Add a line segment (``S``), with an optional explanatory ``label``.

        A line segment is a symbol record using GMT's horizontal dash symbol, so
        ``length`` is the length of the segment and ``pen`` its attributes.

        ``dx1`` is the offset of the segment from the left margin of the column and
        ``dx2`` the offset of the label; both are computed by GMT if not given.
        """
        self.add_symbol(symbol="-", size=length, pen=pen, label=label, dx1=dx1, dx2=dx2)

    def to_stringio(self) -> io.StringIO:
        """
        Return the specification as a :class:`io.StringIO` object.
        """
        return io.StringIO(str(self))

    def __str__(self) -> str:
        """
        The legend specification, one record per line.
        """
        return "\n".join(self.records)

    def __repr__(self) -> str:
        """
        A representation listing the records.
        """
        return f"{self.__class__.__name__}({self.records!r})"

    def __len__(self) -> int:
        """
        The number of records.
        """
        return len(self.records)
