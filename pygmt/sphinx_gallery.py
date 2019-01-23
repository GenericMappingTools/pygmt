"""
Utilities for using pygmt with sphinx-gallery.
"""
try:
    from sphinx_gallery.scrapers import figure_rst
except ImportError:
    pass

from .figure import get_figures


class PyGMTScraper:  # pylint: disable=too-few-public-methods
    """
    Capture ``pygmt.Figure`` objects and save them for sphinx-gallery.

    Pass an instance of this class to ``sphinx_gallery_conf`` in your ``conf.py`` as the
    ``"image_scrapers"`` argument.
    """

    def __call__(self, block, block_vars, gallery_conf):
        """
        Called by sphinx-gallery to save the figures generated after running code.
        """
        image_names = list()
        image_path_iterator = block_vars["image_path_iterator"]
        figures = get_figures()
        while figures:
            fname = image_path_iterator.next()
            fig = figures.pop()
            fig.savefig(fname, transparent=True)
            image_names.append(fname)
        return figure_rst(image_names, gallery_conf["src_dir"])
