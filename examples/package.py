# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import sys
import json
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

sys.path.insert(0, '.')
import jtsbq
import dpbq


def run(import_descriptor='examples/data/spending/datapackage.json',
        export_descriptor='tmp/datapackage.json',
        dataset='package_test',
        prefix='test_'):

    # Storage
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
    credentials = GoogleCredentials.get_application_default()
    service = build('bigquery', 'v2', credentials=credentials)
    project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
    storage = jtsbq.Storage(service, project, dataset, prefix=prefix)

    # Import
    print('[Import]')
    dpsql.import_package(
           storage=storage,
           descriptor=import_descriptor,
           force=True)
    print('imported')

    # Export
    print('[Export]')
    dpsql.export_package(
            storage=storage,
            descriptor=export_descriptor)
    print('exported')

    return locals()


if __name__ == '__main__':
    run()
