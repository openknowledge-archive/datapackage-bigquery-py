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
from dpbq import Package


def run(import_path='examples/data/spending/datapackage.json',
        export_path='tmp/datapackage_test',
        dataset_id='package_test'):

    # Service
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
    credentials = GoogleCredentials.get_application_default()
    service = build('bigquery', 'v2', credentials=credentials)

    # Dataset
    project_id = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
    package = Package(service, project_id, dataset_id)

    # Delete
    print('[Delete]')
    print(package.is_existent)
    if package.is_existent:
        package.delete()
    print(package.is_existent)

    # Create
    print('[Create]')
    if not package.is_existent:
        package.create(import_path)
    print(package.is_existent)
    print(package.get_resources())

    # Export
    print('[Export]')
    package.export(export_path)
    print('done')

    return locals()


if __name__ == '__main__':
    run()
