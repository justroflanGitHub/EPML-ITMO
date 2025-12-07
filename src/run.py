#!/usr/bin/env python

"""Main entry point for the iris data science project."""

import subprocess
import sys


def main():
    """Run the project pipeline or start Jupyter."""
    if len(sys.argv) > 1 and sys.argv[1] == "pipeline":
        # Run DVC pipeline
        try:
            subprocess.run([sys.executable, "-m", "dvc", "repro"], check=True)
        except FileNotFoundError:
            print("DVC not found. Please install DVC or ensure it's in PATH.")
            sys.exit(1)
    else:
        # Start Jupyter notebook
        try:
            subprocess.run(
                [
                    "jupyter",
                    "notebook",
                    "--ip=0.0.0.0",
                    "--port=8888",
                    "--no-browser",
                    "--allow-root",
                ]
            )
        except FileNotFoundError:
            print("Jupyter not found. Please install Jupyter.")
            sys.exit(1)


if __name__ == "__main__":
    main()
