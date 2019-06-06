import unittest
import os
from opentargets_validator.helpers import file_or_resource
from opentargets_validator.validator import validate
from opentargets_urlzsource import URLZSource

class MinimalTests(unittest.TestCase):

    def test_minimal(self):
        resources_path = os.path.dirname(os.path.realpath(__file__))
        data_source_file = resources_path + os.path.sep + "resources" + os.path.sep + "minimal.data.json"

        schema_source_file = resources_path + os.path.sep + "resources" + os.path.sep + "minimal.schema.json"
        schema_uri = "file://"+schema_source_file

        with URLZSource(data_source_file).open() as data_file_handle:
            valid = validate(data_file_handle, schema_uri, True)
            self.assertTrue(valid)