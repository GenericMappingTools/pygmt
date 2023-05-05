# -*- coding: utf-8 -*-
"""
Sphinx documentation configuration file.
"""
# pylint: disable=invalid-name

import datetime
from importlib.metadata import metadata

# isort: off
from sphinx_gallery.sorting import (  # pylint: disable=no-name-in-module
    ExplicitOrder,
    ExampleTitleSortKey,
)
import pygmt
from pygmt import __commit__, __version__
from pygmt.sphinx_gallery import PyGMTScraper

# isort: on

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
]

# Autosummary pages will be generated by sphinx-autogen instead of sphinx-build
autosummary_generate = []

# Auto-generate header anchors with MyST parser
myst_heading_anchors = 4
# Allow code fences using colons
myst_enable_extensions = ["colon_fence"]

# Make the list of returns arguments and attributes render the same as the
# parameters list
napoleon_use_rtype = False
napoleon_use_ivar = True

# configure links to GMT docs
extlinks = {
    "gmt-docs": ("https://docs.generic-mapping-tools.org/latest/%s", None),
    "gmt-term": ("https://docs.generic-mapping-tools.org/latest/gmt.conf#term-%s", ""),
    "gmt-datasets": ("https://www.generic-mapping-tools.org/remote-datasets/%s", None),
}

# intersphinx configuration
intersphinx_mapping = {
    "contextily": ("https://contextily.readthedocs.io/en/stable/", None),
    "geopandas": ("https://geopandas.org/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "rasterio": ("https://rasterio.readthedocs.io/en/stable/", None),
    "rioxarray": ("https://corteva.github.io/rioxarray/stable/", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
    "xyzservices": ("https://xyzservices.readthedocs.io/en/stable", None),
}

# options for sphinx-copybutton
# https://sphinx-copybutton.readthedocs.io
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True
copybutton_remove_prompts = True

sphinx_gallery_conf = {
    # path to your examples scripts
    "examples_dirs": [
        "../examples/gallery",
        "../examples/tutorials",
        "../examples/get_started",
        "../examples/projections",
    ],
    # path where to save gallery generated examples
    "gallery_dirs": ["gallery", "tutorials", "get_started", "projections"],
    "subsection_order": ExplicitOrder(
        [
            "../examples/gallery/maps",
            "../examples/gallery/lines",
            "../examples/gallery/symbols",
            "../examples/gallery/images",
            "../examples/gallery/3d_plots",
            "../examples/gallery/seismology",
            "../examples/gallery/basemaps",
            "../examples/gallery/histograms",
            "../examples/gallery/embellishments",
            "../examples/projections/azim",
            "../examples/projections/conic",
            "../examples/projections/cyl",
            "../examples/projections/misc",
            "../examples/projections/nongeo",
            "../examples/projections/table",
            "../examples/tutorials/basics",
            "../examples/tutorials/advanced",
            "../examples/get_started",
        ]
    ),
    # Patter to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)
    "within_subsection_order": ExampleTitleSortKey,
    # directory where function granular galleries are stored
    "backreferences_dir": "api/generated/backreferences",
    # Modules for which function level galleries are created.  In
    # this case sphinx_gallery and numpy in a tuple of strings.
    "doc_module": "pygmt",
    # Insert links to documentation of objects in the examples
    "reference_url": {"pygmt": None},
    "image_scrapers": (PyGMTScraper(),),
    # Removes configuration comments from scripts
    "remove_config_comments": True,
    # Disable "nested_sections" (default is True), to
    # generate only a single index file for the whole gallery.
    # This is a new feature up on Sphinx-Gallery 0.11.0.
    "nested_sections": False,
}

# Sphinx project configuration
templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
source_suffix = ".rst"
needs_sphinx = "1.8"
# The encoding of source files.
source_encoding = "utf-8-sig"
root_doc = "index"

# General information about the project
year = datetime.date.today().year
project = "PyGMT"
copyright = f"2017-{year}, The PyGMT Developers"  # pylint: disable=redefined-builtin
if len(__version__.split("+")) > 1 or __version__ == "unknown":
    version = "dev"
    # Set base_url for stable version
    html_baseurl = "https://pygmt.org/dev/"
else:
    version = __version__
    # Set base_url for dev version
    html_baseurl = "https://pygmt.org/latest/"
release = __version__

requires_python = metadata("pygmt")["Requires-Python"]
with pygmt.clib.Session() as lib:
    requires_gmt = ">=" + lib.required_version

# These enable substitutions using |variable| in the rst files
rst_epilog = f"""
.. |year| replace:: {year}
.. |requires_python| replace:: {requires_python}
.. |requires_gmt| replace:: {requires_gmt}
"""

html_last_updated_fmt = "%b %d, %Y"
html_title = "PyGMT"
html_short_title = "PyGMT"
html_logo = ""
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_css_files = ["style.css"]
html_extra_path = []
pygments_style = "default"
add_function_parentheses = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# Theme config
html_theme = "sphinx_rtd_theme"
html_theme_options = {}
repository = "GenericMappingTools/pygmt"
repository_url = "https://github.com/GenericMappingTools/pygmt"
if __commit__:
    commit_link = (
        f'<a href="{repository_url}/commit/{ __commit__ }">{ __commit__[:8] }</a>'
    )
else:
    commit_link = (
        f'<a href="{repository_url}/releases/tag/{ __version__ }">{ __version__ }</a>'
    )
html_context = {
    "menu_links": [
        (
            '<i class="fa fa-gavel fa-fw"></i> Code of Conduct',
            "https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> License',
            f"{repository_url}/blob/main/LICENSE.txt",
        ),
        (
            '<i class="fa fa-comment fa-fw"></i> Contact',
            "https://forum.generic-mapping-tools.org",
        ),
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            repository_url,
        ),
    ],
    # Custom variables to enable "Improve this page"" and "Download notebook"
    # links
    "doc_path": "doc",
    "galleries": sphinx_gallery_conf["gallery_dirs"],
    "gallery_dir": dict(
        zip(sphinx_gallery_conf["gallery_dirs"], sphinx_gallery_conf["examples_dirs"])
    ),
    "github_repo": repository,
    "github_version": "main",
    "commit": commit_link,
}
