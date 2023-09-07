import gzip
import io
import os
import sys
import urllib.request

import pkg_resources as res

import opentargets_validator


def file_or_resource(fname=None):
    """
    get filename and check if in getcwd then get from
    the package resources folder
    """
    if fname is not None:
        filename = os.path.expanduser(fname)

        resource_package = opentargets_validator.__name__
        resource_path = os.path.sep.join(("resources", filename))

        abs_filename = os.path.join(os.path.abspath(os.getcwd()), filename) if not os.path.isabs(filename) else filename

        return abs_filename if os.path.isfile(abs_filename) else res.resource_filename(resource_package, resource_path)


def open_source(source):
    """Opens a data source and returns a file handler-like object."""

    # Legacy way of specifying local files, needs to be stripped.
    if source.startswith("file://"):
        source = source[7:]

    # Create a line iterator depending on file type.
    if source == "-":
        return sys.stdin
    if "://" in source:
        url_source = urllib.request.urlopen(source)
        encoding = url_source.headers.get_content_charset()
        return io.StringIO(url_source.read().decode(encoding))
    if source.endswith(".gz"):
        return gzip.open(source, "rt")
    return open(source, "rt")


def box_text(s):
    lines = s.split("\n")
    max_width = max(map(len, lines))
    boxed_lines = ["┃" + l.ljust(max_width) + "┃" for l in lines]
    return "\n".join(
        [
            "┏" + "━" * max_width + "┓",
            *boxed_lines,
            "┗" + "━" * max_width + "┛",
        ]
    )
