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


# Service
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
credentials = GoogleCredentials.get_application_default()
service = build('bigquery', 'v2', credentials=credentials)

# Dataset
project_id = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
package = Package(service, project_id, 'package_test')

# Delete
print('[Delete]')
print(package.is_existent)
if package.is_existent:
    package.delete()
print(package.is_existent)

# Create
print('[Create]')
if not package.is_existent:
    package.create('examples/data/spending/datapackage.json')
print(package.is_existent)
print(package.get_resources())

# Export
print('[Export]')
package.export('tmp/datapackage.json')
print('done')
