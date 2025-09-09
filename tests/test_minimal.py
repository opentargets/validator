import os
import unittest

from opentargets_validator.helpers import open_source
from opentargets_validator.validator import validate


class MinimalTests(unittest.TestCase):
    def setUp(self):
        self.resources_path = os.path.dirname(os.path.realpath(__file__))
        self.schema_uri = os.path.join(
            self.resources_path,
            'resources',
            'minimal.schema.json',
        )

    def test_minimal(self):
        """Correct data must pass validation."""
        correct_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.data.json',
        )
        with open_source(correct_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert valid

    def test_incorrect_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.incorrect.json',
        )
        with open_source(incorrect_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert not valid

    def test_enum_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.enum.incorrect.json',
        )
        with open_source(incorrect_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert not valid

    def test_unexpected_field_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.field.incorrect.json',
        )
        with open_source(incorrect_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert not valid

    def test_pattern_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.pattern.incorrect.json',
        )
        with open_source(incorrect_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert not valid

    def test_required_fails(self):
        """Incorrect data must raise a validation error."""
        incorrect_filename = os.path.join(
            self.resources_path,
            'resources',
            'minimal.pattern.incorrect.json',
        )
        with open_source(incorrect_filename) as data_fh, open_source(
            self.schema_uri,
        ) as schema_fh:
            valid = validate(data_fh, schema_fh)
            assert not valid
