import logging
import tempfile as tmp
import requests as r
import jsonschema as jss
import pkg_resources as res
import json
import os
import gzip
import zipfile
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
        f = r.get(url, *args, stream=True, **kwargs)
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


def generate_validator_from_schema(schema_uri):
    '''load a uri, build and return a jsonschema validator'''
    with url_to_tmpfile(schema_uri) as r_file:
        js_schema = json.load(r_file)

    validator = jss.validators.validator_for(js_schema)
    return validator(schema=js_schema)


class LogAccum(object):
    def __init__(self, logger_o, elem_limit=1024):
        self._logger = logger_o
        self._accum = {'counter': 0}
        self._limit = elem_limit

    def _flush(self, force=False):
        flushed = False
        if force or self._accum['counter'] >= self._limit:
            keys = set(self._accum.iterkeys()) - set(['counter'])

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
