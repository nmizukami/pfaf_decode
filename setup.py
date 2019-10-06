#!/usr/bin/env python

"""The setup script."""

import sys
from setuptools import setup, find_packages
# import versioneer

# with open("requirements.txt") as f:
#     INSTALL_REQUIRES = f.read().strip().split("\n")

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

PYTHON_REQUIRES = '>=3.6'

description = ("module to decode pfafstetter code")
setup(
    name="pfaf_decoder",
    description=description,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    maintainer="Naoki Mizukami",
    maintainer_email="mizukami@ucar.edu",
    url="https://github.com/mizukami/pfaf_decode",
    py_modules=['pfaf'],
    packages=find_packages(),
    python_requires=PYTHON_REQUIRES,
    license="Apache",
    keywords="pfafstetter",
    version='0.0.1',
)
