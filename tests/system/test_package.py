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

from examples.package import run


class TestPackage(unittest.TestCase):

    # Helpers

    def setUp(self):

        # Export files
        self.export_dir = tempfile.mkdtemp()
        _, self.export_path = tempfile.mkstemp(dir=self.export_dir)

        # Python version
        self.version = '%s_%s' % (sys.version_info.major, sys.version_info.minor)

    def tearDown(self):

        # Delete temp files
        try:
            shutil.rmtree(self.export_dir)
        except Exception:
            pass

    # Tests

    def test(self):

        # Run example
        scope = run(
            dataset_id='package_test_%s' % self.version,
            export_path=self.export_path)

        # Assert descriptor
        actual = json.load(io.open(self.export_path, encoding='utf-8'))
        expected = json.load(io.open(scope['import_path'], encoding='utf-8'))
        assert actual['resources'][0]['schema'] == expected['resources'][0]['schema']
        assert actual['resources'][1]['schema'] == expected['resources'][1]['schema']

        # TODO: implement assert data
