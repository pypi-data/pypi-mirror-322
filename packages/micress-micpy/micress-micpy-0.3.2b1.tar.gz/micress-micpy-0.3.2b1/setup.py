# pylint: disable=missing-module-docstring

from pathlib import Path
from setuptools import setup

from micpy import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="micress-micpy",
    version=__version__,
    description="MicPy is a Python package to facilitate MICRESS workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lukas Koschmieder",
    author_email="l.koschmieder@access-technology.de",
    license="BSD-3-Clause (Copyright (c) 2024 Access e.V.)",
    license_files=["LICENSE"],
    packages=["micpy"],
    include_package_data=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["MICRESS"],
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "matplotlib",
        "pandas",
    ],
)
