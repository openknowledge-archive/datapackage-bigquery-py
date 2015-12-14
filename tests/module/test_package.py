# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import unittest
from mock import MagicMock, patch, mock_open, call, ANY
from importlib import import_module
module = import_module('dpbq.package')


class PackageTest(unittest.TestCase):

    # Helpers

    def setUp(self):

        # Mocks
        self.addCleanup(patch.stopall)
        self.Dataset = patch.object(module, 'Dataset').start()
        self.dataset = self.Dataset.return_value
        self.service = MagicMock()
        self.project_id = 'project_id'
        self.dataset_id = 'dataset_id'

        # Create package
        self.package = module.Package(
                service=self.service,
                project_id=self.project_id,
                dataset_id=self.dataset_id)

    # Tests

    def test___repr__(self):

        # Assert values
        assert repr(self.package)

    def test_table(self):

        # Assert values
        assert self.package.dataset == self.dataset

    def test_is_existent_true(self):

        # Assert values
        assert self.package.is_existent

    def test_is_existent_false(self):

        # Mocks
        self.dataset.is_existent = False

        # Assert values
        assert not self.package.is_existent

    def test_create(self):
        pass

    def test_delete(self):
        pass

    def test_get_resources(self):
        pass

    def test_export(self):
        pass
