#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='dc2.core',
    version='0.0.1',
    author="Stephan Adig",
    author_email="sh@sourcecode.de",
    namespace_packages=['dc2', 'dc2.core'],
    url='http://gitlab.sourcecode.de/sadig/dc2.core',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=[
        'scripts/manage.py',
        'scripts/run_app.py'
    ]
)
