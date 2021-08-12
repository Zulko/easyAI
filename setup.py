#!/usr/bin/env python

from setuptools import setup, find_packages

exec(open("easyAI/version.py").read())  # loads __version__

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
