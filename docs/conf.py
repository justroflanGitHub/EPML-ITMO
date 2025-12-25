"""Sphinx configuration for basic documentation without autosummary."""

import os
import sys

# Add project paths manually for reliability
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
src_dir = os.path.abspath(os.path.join(project_root, "src"))

print(f"DEBUG: current_dir = {current_dir}")
print(f"DEBUG: project_root = {project_root}")
print(f"DEBUG: src_dir = {src_dir}")

# Insert at the beginning of sys.path
sys.path.insert(0, src_dir)
sys.path.insert(0, project_root)

print(f"DEBUG: sys.path = {sys.path[:3]}")  # Show first 3 paths

# Basic Sphinx configuration without autosummary
project = "Iris Data Science Project"
version = "0.1"
release = "0.1"
master_doc = "index"
extensions = ["myst_parser"]  # Only myst_parser, no autosummary
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
exclude_patterns = ["_build"]
templates_path: list[str] = []
html_static_path: list[str] = ["_static"]

# Disable autosummary functionality completely
autosummary_generate = False
