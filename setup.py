#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension

setup (name = 'easyAI',
        version = '0.0.0.1',
        description = 'Easy-to-use game AI algorithms (Negamax etc. )')
