# -*- coding: utf-8 -*-
import sys
import os
import datetime

# Sphinx needs to be able to import the package to use autodoc and get the
# version number
sys.path.append(os.path.pardir)

from gmt import __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'numpydoc',
]

# Produce pages for each class and function
autosummary_generate = True
autodoc_default_flags = ['members', 'inherited-members']

# Sphinx project configuration
templates_path = ['_templates']
exclude_patterns = ['_build']
source_suffix = '.rst'
# The encoding of source files.
source_encoding = 'utf-8-sig'
master_doc = 'index'

# General information about the project
year = datetime.date.today().year
project = u'GMT Python'
copyright = u'2017, Leonardo Uieda'
if len(__version__.split('-')) > 1 or __version__ == 'unknown':
    version = 'dev'
else:
    version = __version__

# These enable substitutions using |variable| in the rst files
rst_epilog = """
.. |year| replace:: {year}
""".format(year=year)

html_last_updated_fmt = '%b %d, %Y'
html_title = 'GMT Python'
html_short_title = 'GMT Python'
# html_logo = '_static/logo.png'
# html_favicon = u'favicon.ico'
html_static_path = ['_static']
html_extra_path = ['.nojekyll']
html_use_smartypants = True
pygments_style = 'default'
add_function_parentheses = False

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}
# If false, no module index is generated.
#html_domain_indices = True
# If false, no index is generated.
#html_use_index = True
# If true, the index is split into individual pages for each letter.
#html_split_index = False
# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True
# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True
# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True
# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''
# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None
# Output file base name for HTML help builder.
htmlhelp_basename = 'gmt-python'

# Theme config
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}
html_theme_options = {
    # 'logo': 'logo.png',
    'github_user': 'GenericMappingTools',
    'github_repo': 'gmt-python',
    'github_type': 'star',
    'github_banner': 'true',
    'description': 'A Python interface for the Generic Mapping Tools',
    'extra_nav_links': {
    }
}

