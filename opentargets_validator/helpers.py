from __future__ import unicode_literals
from builtins import object
import logging
import tempfile as tmp
import requests
import jsonschema as jss
import pkg_resources as res
import json
import os
import gzip
import zipfile
import rfc3987
import functools
from contextlib import contextmanager
import opentargets_validator

class URLZSource(object):
    def __init__(self, filename, *args, **kwargs):
        """A source extension for petl python package
        Just in case you need to use proxies for url use it as normal
        named arguments
        """
        self.filename = filename
        self.args = args
        self.kwargs = kwargs
        self.proxies = None

    @contextmanager
    def _open_local(self, filename):
        file_to_open = filename[len('file://'):] if '://' in filename else filename
        open_f = None

        if file_to_open.endswith('.gz'):
            open_f = functools.partial(gzip.open, mode='rb')

        elif file_to_open.endswith('.zip'):
            zipped_data = zipfile.ZipFile(file_to_open)
            info = zipped_data.getinfo(zipped_data.filelist[0].orig_filename)

            file_to_open = info
            open_f = functools.partial(zipped_data.open)
        else:
            open_f = functools.partial(open, mode='r')

        with open_f(file_to_open) as fd:
            yield fd

    @contextmanager
    def open(self):
        if self.filename.startswith('ftp://'):
            raise NotImplementedError('finish ftp')

        elif self.filename.startswith('file://') or ('://' not in self.filename):
            file_to_open = self.filename[len('file://'):] if '://' in self.filename else self.filename
            with self._open_local(file_to_open) as fd:
                yield fd

        else:
            local_filename = self.filename.split('://')[-1].split('/')[-1]
            f = requests.get(self.filename, *self.args, stream=True, **self.kwargs)
            f.raise_for_status()
            file_to_open = None
            with tmp.NamedTemporaryFile(mode='wb', suffix=local_filename, delete=False) as fd:
                # write data into file in streaming fashion
                file_to_open = fd.name
                for block in f.iter_content(1024):
                    fd.write(block)

            with self._open_local(file_to_open) as fd:
                yield fd


def file_handler(uri):
    #handle file:// uris because of https://github.com/Julian/jsonschema/issues/478

    schema = None
    uri_split = rfc3987.parse(uri)
    with open(os.path.abspath(os.path.join(uri_split['authority'], uri_split['path'])), 'r') as schema_file:
        schema = json.load(schema_file)
    return schema


def generate_validator_from_schema(schema_uri):

    #download the schema to a string
    schema = None
    #handle http and file
    uri_split = rfc3987.parse(schema_uri)
    if uri_split['scheme'] in ("http", "https"):
        #its a http or https use requests
        schema = requests.get(schema_uri).json()
    elif uri_split['scheme'] == "file":
        #its a file, open as normal
        #reconstiture the file path from the uri
        with open(os.path.abspath(os.path.join(uri_split['authority'], uri_split['path'])), 'r') as schema_file:
            schema = json.load(schema_file)
    else:
        raise ValueError("schema uri must have file or url scheme")
    

    #Create a refresolver to allow resolution
    #of relative schema links
    #This is required to use git branches / versions and
    #local development correctly
    #Don't use from_schema because it uses the $id baked
    #into the schema, and we want to avoid baking
    handlers = dict(file=file_handler)
    resolver = jss.RefResolver(schema_uri, schema, handlers=handlers, 
        store={})

    validator = jss.Draft7Validator(schema=schema, 
        resolver=resolver,
        )

    return validator

def file_or_resource(fname=None):
    '''get filename and check if in getcwd then get from
    the package resources folder
    '''
    if fname is not None:
        filename = os.path.expanduser(fname)
    
        resource_package = opentargets_validator.__name__
        resource_path = os.path.sep.join(('resources', filename))

        abs_filename = os.path.join(os.path.abspath(os.getcwd()), filename) \
                       if not os.path.isabs(filename) else filename

        return abs_filename if os.path.isfile(abs_filename) \
            else res.resource_filename(resource_package, resource_path)
