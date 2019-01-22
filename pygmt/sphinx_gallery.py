"""
Utilities for using pygmt with sphinx-gallery.
"""
try:
    from sphinx_gallery.scrapers import figure_rst
except ImportError:
    pass

from .figure import get_figures


class PyGMTScraper:
    """
    Capture ``pygmt.Figure`` objects and save them for sphinx-gallery.

    Pass an instance of this class to ``sphinx_gallery_conf`` in your ``conf.py`` as the
    ``"image_scrapers"`` argument.
    """

    def __init__(self):
        # Keep a set of figures that have already been saved
        self.saved = set()

    def __call__(self, block, block_vars, gallery_conf):
        """
        Called by sphinx-gallery to save the figures generated after running code.
        """
        image_names = list()
        image_path_iterator = block_vars["image_path_iterator"]
        figures = get_figures()
        for name in figures:
            if name not in self.saved:
                self.saved.add(name)
                fname = image_path_iterator.next()
                figures[name].savefig(fname, transparent=True)
                image_names.append(fname)
        return figure_rst(image_names, gallery_conf["src_dir"])
