import unittest
import os
from opentargets_validator.validator import validate
from opentargets_validator.helpers import open_source


class MinimalTests(unittest.TestCase):
    def setUp(self):
        self.resources_path = os.path.dirname(os.path.realpath(__file__))
        self.schema_uri = os.path.join(self.resources_path, "resources", "minimal.schema.json")

    def test_minimal(self):
        """Correct data must pass validation."""
        correct_filename = os.path.join(self.resources_path, "resources", "minimal.data.json")
        with open_source(correct_filename) as data_fh, open_source(self.schema_uri) as schema_fh:
            valid = validate(data_fh, schema_fh)
            self.assertTrue(valid)

    def test_incorrect_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(self.resources_path, "resources", "minimal.incorrect.json")
        with open_source(incorrect_filename) as data_fh, open_source(self.schema_uri) as schema_fh:
            valid = validate(data_fh, schema_fh)
            self.assertFalse(valid)
