# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from importlib import import_module
module = import_module('dpbq.dataset')


# TODO: implement
class DatasetTest(unittest.TestCase):

    # Tests

    def test(self):
        self.assertTrue(module.Dataset)