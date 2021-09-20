"""
Utilities for using pygmt with sphinx-gallery.
"""

import sphinx_gallery.scrapers
from pygmt.figure import SHOWED_FIGURES


class PyGMTScraper:  # pylint: disable=too-few-public-methods
    """
    Save ``pygmt.Figure`` objects that had their ``show`` method called.

    Used by sphinx-gallery to generate the plots from the code in the examples.

    Pass an instance of this class to ``sphinx_gallery_conf`` in your
    ``conf.py`` as the ``"image_scrapers"`` argument.
    """

    def __call__(self, block, block_vars, gallery_conf):
        """
        Called by sphinx-gallery to save the figures generated after running
        code.
        """
        image_names = []
        image_path_iterator = block_vars["image_path_iterator"]
        figures = SHOWED_FIGURES
        while figures:
            fname = next(image_path_iterator)
            fig = figures.pop(0)
            fig.savefig(fname, transparent=True, dpi=200)
            image_names.append(fname)
        return sphinx_gallery.scrapers.figure_rst(image_names, gallery_conf["src_dir"])
