#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='easyAI',
    version='1.0.0.4',
    description='Easy-to-use game AI algorithms (Negamax etc. )',
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    keywords="board games AI artificial intelligence negamax",
    packages=find_packages(exclude='docs')
)
