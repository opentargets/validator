#!/usr/bin/env python

from setuptools import setup

# importing __<vars>__ into the namespace
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
      install_requires=['requests','jsonschema'],
      dependency_links=[],
      include_package_data=True,
      entry_points={
          'console_scripts': ['opentargets_validator=opentargets_validator.cli:main'],
      },
      data_files=[],
      scripts=[],
      classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
      ],
      extras_require={
          'tests': [
              'nose'
              ]})
