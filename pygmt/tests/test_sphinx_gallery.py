"""
Test the sphinx-gallery scraper and code required to make it work.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pygmt.figure import SHOWED_FIGURES, Figure
from pygmt.sphinx_gallery import PyGMTScraper

pytest.importorskip("sphinx_gallery", reason="Requires sphinx-gallery to be installed")
pytest.importorskip("IPython", reason="Requires IPython to be installed")


def test_pygmtscraper():
    """
    Make sure the scraper finds the figures and removes them from the pool.
    """
    showed = SHOWED_FIGURES.copy()
    for _ in range(len(SHOWED_FIGURES)):
        SHOWED_FIGURES.pop()
    try:
        fig = Figure()
        fig.coast(region="BR", projection="M6i", land="gray", frame=True)
        fig.show()
        assert len(SHOWED_FIGURES) == 1
        assert SHOWED_FIGURES[0] is fig
        scraper = PyGMTScraper()
        with TemporaryDirectory(dir=Path.cwd()) as tmpdir:
            conf = {"src_dir": "meh"}
            fname = Path(tmpdir) / "meh.png"
            block_vars = {"image_path_iterator": (i for i in [fname])}
            assert not fname.exists()
            scraper(None, block_vars, conf)
            assert fname.exists()
            assert not SHOWED_FIGURES
    finally:
        SHOWED_FIGURES.extend(showed)
