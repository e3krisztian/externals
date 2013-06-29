#!/usr/bin/env python
# coding: utf8

# distutils is nice and recommended, but pip will not install requires=
# requirements :(, so going with setuptools - as everyone else?!
# from distutils.core import setup
from setuptools import setup

setup(
    name='externals',
    version='0.2dev',
    description=(
        'A light abstraction of hierarchically named resources,'
        ' potentially external to the current process'),
    author='Krisztián Fekete',
    author_email='fekete.krisztyan@gmail.com',
    url='http://maybe.later',
    packages=['externals'],
    install_requires=[],
    tests_require=['temp_dir >=0.1', 'nose >=1.3'],
    test_suite='nose.collector',
    )
