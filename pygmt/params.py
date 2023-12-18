from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import NamedTuple


class Alias(NamedTuple):
    name: str
    modifier: str
    separator: str | None = None


class BaseParams:
    def __str__(self):
        values = []
        for alias in self.aliases:
            value = getattr(self, alias.name)
            if value in (None, False):
                continue
            if value is True:
                value = ""
            if isinstance(value, Iterable) and not isinstance(value, str):
                value = alias.separator.join(map(str, value))
            values.append(f"{alias.modifier}{value}")
        return "".join(values)

    def __repr__(self):
        string = []
        for alias in self.aliases:
            value = getattr(self, alias.name)
            if value is None or value is False:
                continue
            string.append(f"{alias.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(string)})"


@dataclass(repr=False)
class Box(BaseParams):
    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    innerborder: str | Sequence | None = None
    pen: str | None = None
    radius: float | bool | None = False
    shading: str | Sequence | None = None

    aliases = [
        Alias("clearance", "+c", "/"),
        Alias("fill", "+g"),
        Alias("innerborder", "+i", "/"),
        Alias("pen", "+p"),
        Alias("radius", "+r"),
        Alias("shading", "+s", "/"),
    ]
