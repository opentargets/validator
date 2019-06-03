from __future__ import unicode_literals
from builtins import object
import logging
import requests
import jsonschema as jss
import pkg_resources as res
import simplejson as json
import os
import rfc3987
import opentargets_validator
from collections import OrderedDict
import hashlib


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


class DataStructureFlattener:
    '''Class to flatten nested Python data structures into ordered dictionaries
    and to compute hexadigests of them when serialised as JSON. Used to compute
    hexadigests for JSON represented as Python data structures so that
    sub-structure order and white space are irrelvant.

    '''
    def __init__(self, data_structure):
        self.data_structure= data_structure

    def flatten(self, structure, key="", path="", flattened=None):
        '''
        Given any Python data structure nested to an arbitrary level, flatten it into an
        ordered dictionary. This method can be improved and simplified.
        Returns a Python dictionary where the levels of nesting are represented by
        successive arrows ("->").
        '''
        if flattened is None:
            flattened = {}
        if type(structure) not in(dict, list):
            flattened[((path + "->") if path else "") + key] = structure
        elif isinstance(structure, list):
            structure.sort()
            for i, item in enumerate(structure):
                self.flatten(item, "%d" % i, path + "->" + key, flattened)
        else:
            for new_key, value in structure.items():
                self.flatten(value, new_key, path + "->" + key, flattened)
        return flattened
        
    def get_ordered_dict(self):
        '''
        Return an ordered dictionary by processing the standard Python dictionary
        produced by method "flatten()".
        '''
        unordered_dict = self.flatten(self.data_structure)
        ordered_dict = OrderedDict()
        sorted_keys = sorted(unordered_dict.keys())
        for key in sorted_keys:
            key_cleaned = key.strip().replace('->->', '')
            ordered_dict[key_cleaned] = unordered_dict[key]
        return ordered_dict

    def get_hexdigest(self):
        '''
        Return the hexadigest value for a JSON-serialised version of the
        ordered dictionary returned by method "get_ordered_dict()".
        '''
        ordered_dict = self.get_ordered_dict()
        return hashlib.md5(json.dumps(ordered_dict).encode("utf-8")).hexdigest()