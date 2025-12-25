"""Minimal Sphinx configuration - no extensions to avoid import issues."""

# Minimal configuration with no extensions
project = "Iris Data Science Project"
version = "0.1"
release = "0.1"
master_doc = "index"
extensions: list[str] = []  # No extensions at all
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
exclude_patterns = ["_build"]
templates_path: list[str] = []
html_static_path: list[str] = ["_static"]
