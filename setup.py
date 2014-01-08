#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension

setup( name = 'easyAI',
       author = 'Zulko 2013 and contributors',
       version = '0.0.0.4',
       description = 'Easy-to-use game AI algorithms (Negamax etc. )',
       long_description=open('README.rst').read(),
       license='LICENSE.txt',
       keywords="board games AI artificial intelligence negamax",
       packages= find_packages(exclude='docs'))
