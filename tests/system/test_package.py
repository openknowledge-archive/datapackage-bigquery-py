# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import io
import six
import sys
import json
import runpy
import shutil
import tempfile
import unittest


from examples import base
from examples import spending


class TestPackage(unittest.TestCase):

    # Helpers

    def setUp(self):
        self.target = tempfile.mkstemp(dir=tempfile.mkdtemp())[1]

    def tearDown(self):
        try:
            shutil.rmtree(os.path.dirname(self.target))
        except Exception:
            pass

    # Tests

    def test(self):

        # Run function
        base.run(spending.dataset, spending.prefix, spending.source, self.target)

        # Assert values
        # TODO: implement assertions
        actual = json.load(io.open(self.target, encoding='utf-8'))
        expected = json.load(io.open(spending.source, encoding='utf-8'))
