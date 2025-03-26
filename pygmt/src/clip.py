"""
Clip.
"""

from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def _clip_method(clip_type):
    """
    Return the clip method for the given clip type.
    """
    match clip_type:
        case "polygon":
            return "clip"
        case "land":
            return "coast"
        case "water":
            return "coast"


class clip:  # noqa: N801
    """
    Clip.
    """

    def __init__(self):
        self.type = None
        self.data = None
        self.args_enter = ""
        self.args_exit = ""

    def polygon(self, x, y):
        """
        Clip the data to a polygon.
        """
        self.type = "polygon"
        self.data = (x, y)
        self.args_enter = []
        self.args_exit = ["-C"]
        return self

    def land(self):
        """
        Clip the data to the land.
        """
        self.type = "land"
        self.data = None
        self.args_enter = build_arg_list({"G": True})
        self.args_exit = build_arg_list({"Q": True})
        return self

    def water(self):
        """
        Clip the data to the water.
        """
        self.type = "water"
        self.data = None
        self.args_enter = build_arg_list({"S": True})
        self.args_exit = build_arg_list({"Q": True})
        return self

    def __enter__(self):
        """
        Enter the context manager.
        """
        module = _clip_method(self.type)

        with Session() as lib:
            if module == "clip":
                with lib.virtualfile_in(x=self.data[0], y=self.data[1]) as vintbl:
                    lib.call_module(module, args=[vintbl])
            else:
                lib.call_module(module, args=self.args_enter)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        module = _clip_method(self.type)
        with Session() as lib:
            lib.call_module(module, args=self.args_exit)
