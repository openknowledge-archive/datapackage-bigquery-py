# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import pytest
import unittest
from mock import MagicMock, patch, mock_open, call, ANY
from importlib import import_module
module = import_module('dpbq.package')


class PackageTest(unittest.TestCase):

    # Helpers

    def setUp(self):

        # Fixtures
        basedir = os.path.join(os.path.dirname(__file__), '..', '..')
        self.descriptor = os.path.join(basedir,
                'examples', 'data', 'spending', 'datapackage.json')

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

        # Mocks
        Resource = patch.object(module.jtsbq, 'Resource').start()
        resource = Resource.return_value

        # Method call
        self.package.create(self.descriptor)

        # Assert calls
        Resource.assert_any_call(
               service=self.service,
               project_id=self.project_id,
               dataset_id=self.dataset_id,
               table_id='data__data1')
        Resource.assert_any_call(
               service=self.service,
               project_id=self.project_id,
               dataset_id=self.dataset_id,
               table_id='data__data2')
        # TODO: add actual arguments
        resource.create.assert_any_call(ANY)
        resource.import_data.assert_any_call(ANY)

    def test_delete(self):

        # Method call
        self.package.delete()

        # Assert calls
        self.dataset.delete.assert_called_with()

    def test_get_resources(self):

        # Mocks
        Resource = patch.object(module.jtsbq, 'Resource').start()
        self.dataset.get_tables.return_value = ['name']

        # Method call
        result = self.package.get_resources()
        result_plain = self.package.get_resources(plain=True)

        # Asssert values
        result = [Resource.return_value]
        result_plain == ['name']

        # Assert calls
        self.dataset.get_tables.assert_called_with(plain=True)
        Resource.assert_called_with(
            service=self.service,
            project_id=self.project_id,
            dataset_id=self.dataset_id,
            table_id='name')

    def test_export(self):
        pass
