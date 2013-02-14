#!/usr/bin/env python
# coding: utf8

# distutils is nice and recommended, but pip will not install requires=
# requirements :(, so going with setuptools - as everyone else!?
# from distutils.core import setup
from setuptools import setup

setup(name='externals',
      version='0.1dev',
      description=u'A light abstraction of hierarchically named resources,'
                  u' potentially external to the current process',
      author=u'Krisztián Fekete',
#       author_email='fkr972',
#       url='http://maybe.later',
      packages=['externals'],
      install_requires=['tempdir >=0.4, <1.0'],
      provides=['externals (0.1)']
     )
