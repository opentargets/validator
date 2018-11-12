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
from contextlib import contextmanager
import opentargets_validator

_l = logging.getLogger(__name__)


@contextmanager
def url_to_tmpfile(url, delete=True, *args, **kwargs):
    '''request a url using requests pkg and pass *args and **kwargs to
    requests.get function (useful for proxies) and returns the filled file
    descriptor from a tempfile.NamedTemporaryFile
    '''
    f = None

    if url.startswith('ftp://'):
        raise NotImplementedError('finish ftp')

    elif url.startswith('file://') or ('://' not in url):
        filename = url[len('file://'):] if '://' in url else url
        with open(filename, mode="r+b") as f:
            yield f

    else:
        f = requests.get(url, *args, stream=True, **kwargs)
        f.raise_for_status()

        with tmp.NamedTemporaryFile(mode='r+w+b', delete=delete) as fd:
            # write data into file in streaming fashion
            for block in f.iter_content(1024):
                fd.write(block)

            fd.seek(0)
            yield fd

        f.close()


class URLZSource(object):
    def __init__(self, *args, **kwargs):
        '''A source extension for petl python package
        Just in case you need to use proxies for url use it as normal
        named arguments
        '''
        self.args = args
        self.kwargs = kwargs
        self.proxies = None

    @contextmanager
    def open(self, mode='r'):
        if not mode.startswith('r'):
            raise IOError('source is read-only')

        zf = None

        with url_to_tmpfile(*self.args, **self.kwargs) as f:
            buf = f

            if self.args[0].endswith('.gz'):
                zf = gzip.GzipFile(fileobj=buf)
            elif self.args[0].endswith('.zip'):
                zipped_data = zipfile.ZipFile(buf)
                info = zipped_data.getinfo(
                    zipped_data.filelist[0].orig_filename)
                zf = zipped_data.open(info)
            else:
                zf = buf

            yield zf
        zf.close()

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


class LogAccum(object):
    def __init__(self, logger_o, elem_limit=1024):
        self._logger = logger_o
        self._accum = {'counter': 0}
        self._limit = elem_limit

    def _flush(self, force=False):
        flushed = False
        if force or self._accum['counter'] >= self._limit:
            keys = set(self._accum.keys()) - set(['counter'])

            for k in keys:
                for msg in self._accum[k]:
                    self._logger.log(k, msg[0], *msg[1])
            # reset the accum
            self._accum = {'counter': 0}
            flushed = True
        
        return flushed

    def flush(self, force=True):
        return self._flush(force)

    def log(self, level, message, *args):
        if level in self._accum:
            self._accum[level].append((message, args))
        else:
            self._accum[level] = [(message, args)]

        self._accum['counter'] += 1
        self._flush()

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush(True)


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
