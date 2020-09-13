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
import sphinx_rtd_theme
import sys
import os
sys.path.append(os.path.abspath("../../"))

from recommonmark.transform import AutoStructify
autodoc_inherit_docstrings = False

source_suffix = ['.rst', '.md']
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon',
              'sphinx_revealjs',
              'sphinxcontrib.video'

]

project = 'MiniTorch'
copyright = '2020, Sasha Rush'
author = 'Sasha Rush'

master_doc = "index"

# The full version, including alpha/beta/rc tags
release = '0.1'
highlight_language = 'python'
language = 'english'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
# ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_js_files = [
]
html_css_files = [
"default.css"
]

revealjs_script_conf = """
{
    controls: false,
    transition: 'none',
  history: true,
slideNumber: true,
  width: 960,
  height: 700,

  // Factor of the display size that should remain empty around
  // the content
  margin: 0.04,
  //fragments: false,

  // Bounds for smallest/largest possible scale to apply to content
  minScale: 0.2,
  maxScale: 2.0,
    center: false,
    keyboard: {
	    67: function() { RevealChalkboard.toggleNotesCanvas() },	// toggle notes canvas when 'c' is pressed
	    66: function() { RevealChalkboard.toggleChalkboard() },	// toggle chalkboard when 'b' is pressed
	    46: function() { RevealChalkboard.clear() },	// clear chalkboard when 'DEL' is pressed
	     8: function() { RevealChalkboard.reset() },	// reset chalkboard data on current slide when 'BACKSPACE' is pressed
	    68: function() { RevealChalkboard.download() },	// downlad recorded chalkboard drawing when 'd' is pressed
	    88: function() { RevealChalkboard.colorNext() },	// cycle colors forward when 'x' is pressed
	    89: function() { RevealChalkboard.colorPrev() },	// cycle colors backward when 'y' is pressed
    }
}
"""


revealjs_script_plugins = [
    {
         "src": 'js/chalkboard.js'
    },
    {
        "src": "revealjs/plugin/notes/notes.js",
        "options": "{async: true}",
    },
    {
        "src": "revealjs/plugin/highlight/highlight.js",
        "options": "{async: true, callback: function() { hljs.initHighlightingOnLoad(); }}",
    },
]

revealjs_css_files = [
    "revealjs/lib/css/zenburn.css",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css",
    "default.css"
]


