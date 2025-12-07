#!/usr/bin/env python

"""
Main entry point for the iris data science project.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Run the project pipeline or start Jupyter."""
    if len(sys.argv) > 1 and sys.argv[1] == "pipeline":
        # Run DVC pipeline
        subprocess.run(["dvc", "repro"], check=True)
    else:
        # Start Jupyter notebook
        subprocess.run(["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"])


if __name__ == "__main__":
    main()
