#!/usr/bin/env python

from __future__ import unicode_literals
from setuptools import setup

# importing __<vars>__ into the namespace
#https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
with open('opentargets_validator/version.py') as fv:
    exec(fv.read())

setup(name=__pkgname__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__homepage__,
    packages=['opentargets_validator'],
    license=__license__,
    download_url=__homepage__ + '/archive/' + __version__ + '.tar.gz',
    keywords=['opentargets', 'bioinformatics', 'python2'],
    platforms=['any'],
    #make sure this matches requirements.txt
    install_requires=['requests','jsonschema==3.0.0a3', 'rfc3987', 'future'],
    dependency_links=[],
    include_package_data=True,
    entry_points={'console_scripts': ['opentargets_validator=opentargets_validator.cli:main'],},
    data_files=[],
    scripts=[],
    classifiers=[
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3'
    ],
    #make sure this matches requirements.txt
    extras_require={'dev': ['pytest-cov','codecov']}
)
