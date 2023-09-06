#!/usr/bin/env python3

from setuptools import setup
from setuptools.command.install import install
import io
import os
import sys


pkg_dir = os.path.dirname(__file__)
# importing __<vars>__ into the namespace
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
with open(os.path.join(pkg_dir, "opentargets_validator", "version.py")) as fv:
    exec(fv.read())


long_description = ""
readme_path = os.path.join(pkg_dir, "README.md")
with io.open(readme_path, encoding="utf-8") as readme_file:
    long_description = readme_file.read()


class VerifyVersionCommand(install):
    description = "Verify that the git tag matches CircleCI version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")
        if tag != __version__:
            sys.exit(f"Git tag {tag} does not match the version of this app {__version__}")


setup(
    name=__pkgname__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    author=__author__,
    author_email=__author_email__,
    url=__homepage__,
    packages=["opentargets_validator"],
    license=__license__,
    download_url=__homepage__ + "/archive/" + __version__ + ".tar.gz",
    keywords=["opentargets", "bioinformatics", "python3"],
    platforms=["any"],
    install_requires=[
        "fastjsonschema>=2.18.0",
        "pathos>=0.3.1",
    ],
    dependency_links=[],
    include_package_data=True,
    entry_points={
        "console_scripts": ["opentargets_validator=opentargets_validator.cli:main"],
    },
    data_files=[],
    scripts=[],
    classifiers=["Programming Language :: Python :: 3"],
    extras_require={"dev": ["build", "codecov", "pytest", "pytest-cov", "twine"]},
    python_requires=">=3.8",
    cmdclass={
        "verify": VerifyVersionCommand,
    },
)
