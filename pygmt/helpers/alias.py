import functools
import inspect
from typing import NamedTuple
from pygmt.helpers.utils import is_nonstr_iter


class Alias(NamedTuple):
    name: str
    flag: str
    modifier: str
    separator: str

def sequence_to_str(seq, separator):
    return separator.join(str(item) for item in seq)

def apply_alias(aliases):
    def alias_decorator(module_func):
        sig = inspect.signature(module_func)

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            """
            New module that parses and replaces the registered aliases.
            """
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            bound.arguments["options"] = {}
            for alias in aliases:
                if alias.name not in bound.arguments:
                    continue
                value = bound.arguments.get(alias.name)
                if value in (None, False):
                    continue
                if alias.separator and is_nonstr_iter(value):
                    value = sequence_to_str(value, alias.separator)
                if value is True:
                    value = ""
                value = f"{alias.modifier}{value}"
                bound.arguments["options"][alias.flag] = bound.arguments["options"].get(alias.flag, "") + value
                print(bound.arguments)

            print(bound.arguments)
            print(bound.args)
            print(bound.kwargs)
            return module_func(*bound.args, **bound.kwargs)

        new_module.aliases = {alias.flag: alias.name for alias in aliases}
        return new_module

    return alias_decorator
