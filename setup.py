#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open(os.path.join("easyAI", "version.py"), "r") as f:
    __version__ = f.read().split(" ")[2].strip("\n").strip('"')

setup(
    name="easyAI",
    version=__version__,
    description="Easy-to-use game AI algorithms (Negamax etc. )",
    long_description=open("README.rst").read(),
    license="LICENSE.txt",
    keywords="board games AI artificial intelligence negamax",
    packages=find_packages(exclude="docs"),
    install_requires=["numpy"],
)
