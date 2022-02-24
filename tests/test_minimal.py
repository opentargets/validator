import unittest
import os
from opentargets_validator.validator import validate
from opentargets_urlzsource import URLZSource


class MinimalTests(unittest.TestCase):

    def setUp(self):
        self.resources_path = os.path.dirname(os.path.realpath(__file__))
        self.schema_uri = 'file://' + os.path.join(self.resources_path, 'resources', 'minimal.schema.json')

    def test_minimal(self):
        """Correct data must pass validation."""
        correct_filename = os.path.join(self.resources_path, 'resources', 'minimal.data.json')
        with URLZSource(correct_filename).open() as data_file_handle:
            valid = validate(data_file_handle, self.schema_uri)
            self.assertTrue(valid)

    def test_incorrect_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(self.resources_path, 'resources', 'minimal.incorrect.json')
        with URLZSource(incorrect_filename).open() as data_file_handle:
            valid = validate(data_file_handle, self.schema_uri)
            self.assertFalse(valid)
