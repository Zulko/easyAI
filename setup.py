#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="easyAI",
    version="2.0.1",
    description="Easy-to-use game AI algorithms (Negamax etc. )",
    long_description=open("README.rst").read(),
    license="LICENSE.txt",
    keywords="board games AI artificial intelligence negamax",
    packages=find_packages(exclude="docs"),
    install_requires=["numpy"],
)
