# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import unittest
from mock import MagicMock, patch, ANY
from importlib import import_module
module = import_module('dpbq.dataset')


class TestDataset(unittest.TestCase):

    # Helpers

    def setUp(self):

        # Mocks
        self.addCleanup(patch.stopall)
        self.service = MagicMock()
        self.project_id = 'project_id'
        self.dataset_id = 'dataset_id'

        # Create dataset
        self.dataset = module.Dataset(
                service=self.service,
                project_id=self.project_id,
                dataset_id=self.dataset_id)

    # Tests

    def test___repr__(self):

        # Assert values
        assert repr(self.dataset)

    def test_service(self):

        # Assert values
        assert self.dataset.service == self.service

    def test_project_id(self):

        # Assert values
        assert self.dataset.project_id == self.project_id

    def test_dataset_id(self):

        # Assert values
        assert self.dataset.dataset_id == self.dataset_id

    def test_is_existent_true(self):

        # Assert values
        assert self.dataset.is_existent

    def test_is_existent_false(self):

        # Mocks
        error = Exception()
        error.resp = MagicMock(status=404)
        patch.object(module, 'HttpError', Exception).start()
        self.service.tables.side_effect = error

        # Assert values
        assert not self.dataset.is_existent

    def test_is_existent_raise(self):

        # Mocks
        error = Exception()
        error.resp = MagicMock(status=500)
        patch.object(module, 'HttpError', Exception).start()
        self.service.tables.side_effect = error

        # Assert exception
        with pytest.raises(module.HttpError):
           self.dataset.is_existent

    def test_get_tables(self):
        pass

    def test_get_tables_plain(self):
        pass
