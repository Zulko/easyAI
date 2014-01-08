#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension

setup (name = 'easyAI',
       author = "Zulko 2013",
        version = '0.0.0.2',
        description = 'Easy-to-use game AI algorithms (Negamax etc. )',
        long_description=open('README.rst').read())
