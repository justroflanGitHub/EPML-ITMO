"""Setup configuration for Iris Data Science Project."""

from setuptools import find_packages, setup

setup(
    name="iris-data-science-project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.1.0",
    description=(
        "Comprehensive Data Science Workspace for Analyzing the Iris Dataset "
        "Using Modern Engineering Practices"
    ),
    author="Mikhail",
    license="MIT",
)
