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
