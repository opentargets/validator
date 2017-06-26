#!/usr/bin/env python

from distutils.core import setup

# importing __<vars>__ into the namespace
with open('evsvalidator/version.py') as fv:
    exec(fv.read())

setup(name=__pkgname__,
      version=__version__,
      description=__description__,
      author=__author__,
      author_email=__author_email__,
      url=__homepage__,
      packages=['evsvalidator'],
      license=__license__,
      download_url=__homepage__ + '/archive/' + __version__ + '.tar.gz',
      keywords=['opentargets', 'bioinformatics', 'python2'],
      platforms=['any'],
      install_requires=[],
      dependency_links=[],
      include_package_data=True,
      entry_points={
          'console_scripts': ['evsvalidator=evsvalidator.cli:main'],
      },
      data_files=[],
      scripts=[])
