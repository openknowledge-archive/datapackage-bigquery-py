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
from dpbq import Dataset


def run(dataset_id='dataset_test'):

    # Service
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
    credentials = GoogleCredentials.get_application_default()
    service = build('bigquery', 'v2', credentials=credentials)

    # Dataset
    project_id = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
    dataset = Dataset(service, project_id, dataset_id)

    # Delete
    print('[Delete]')
    print(dataset.is_existent)
    if dataset.is_existent:
        dataset.delete()
    print(dataset.is_existent)

    # Create
    print('[Create]')
    dataset.create()
    print(dataset.is_existent)
    print(dataset.get_tables())

    return locals()


if __name__ == '__main__':
    run()
