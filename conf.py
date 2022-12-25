# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "AbyxDev's Blog"
copyright = '2022, AbyxDev'
author = 'AbyxDev'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinxext.opengraph',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README']

rst_prolog = """
.. role:: python(code)
    :language: python
    :class: highlight
"""

rst_epilog = """

----

*If you have something to say about this page,
feel free to* `let me know <https://abyx.dev/contact>`_!
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_title = "AbyxDev's Blog" # remove the word "documentation"
html_favicon = '_static/favicon.ico'

# -- Options for OpenGraph meta tags -----------------------------------------

ogp_site_url = 'https://blog.abyx.dev'
ogp_site_name = "AbyxDev's Blog"
ogp_image = '_static/Abyx.png'
ogp_image_alt = 'AbyxDev'
ogp_type = 'article'
