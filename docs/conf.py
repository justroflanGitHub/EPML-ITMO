"""Sphinx configuration with proper sys_path setup for autosummary imports."""

import os

# Sphinx configuration with autosummary support
project = "Iris Data Science Project"
version = "0.1"
release = "0.1"
master_doc = "index"
extensions = ["myst_parser", "sphinx.ext.autosummary", "sphinx.ext.autodoc"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
exclude_patterns = ["_build"]
templates_path: list[str] = []
html_static_path: list[str] = ["_static"]

# Use sys_path_append instead of manual sys.path modification
# This adds the project root and src directory to Python path
sys_path_append = [
    os.path.abspath(".."),  # Project root
    os.path.abspath("../src"),  # src directory
]

# Enable autosummary functionality
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
