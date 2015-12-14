# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from dpbq import Package
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


# Parameters
client_email = os.environ['GOOGLE_CLIENT_EMAIL']
private_key = os.environ['GOOGLE_PRIVATE_KEY']
project_id = os.environ['GOOGLE_PROJECT_ID']
scope = 'https://www.googleapis.com/auth/bigquery'

# Service
credentials = SignedJwtAssertionCredentials(client_email, private_key, scope)
service = build('bigquery', 'v2', credentials=credentials)

# Dataset
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
