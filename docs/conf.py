"""Minimal Sphinx configuration to prevent autosummary import errors."""

import os
import sys

# Add paths for documentation build
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
src_dir = os.path.join(project_root, "src")

sys.path.insert(0, current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, src_dir)  # Add src directory to Python path

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
html_static_path: list[str] = ["_static"]  # Add static files directory

# Enable autosummary functionality
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
