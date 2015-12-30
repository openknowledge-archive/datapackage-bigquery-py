# datapackage-bigquery-py

[![Travis](https://img.shields.io/travis/okfn/datapackage-bigquery-py.svg)](https://travis-ci.org/okfn/datapackage-bigquery-py)
[![Coveralls](http://img.shields.io/coveralls/okfn/datapackage-bigquery-py.svg?branch=master)](https://coveralls.io/r/okfn/datapackage-bigquery-py?branch=master)

Generate and load BigQuery tables based on Data Package.

## Usage

This section is intended to be used by end-users of the library.

### Import/Export

> See section below how to get tabular storage object.

High-level API is easy to use.

Having Data Package in current directory we can import it to bigquery database:

```python
import dpbq

dpbq.import_package(<storage>, 'descriptor.json')
```

Also we can export it from sql database:

```python
import dpbq

dpbq.export_package(<storage>, 'descriptor.json')
```

### Tabular Storage

To start using Google BigQuery service:
- Create a new project - [link](https://console.developers.google.com/home/dashboard)
- Create a service key - [link](https://console.developers.google.com/apis/credentials)
- Download json credentials and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

We can get storage this way:

```python
import io
import os
import json
import jtsbq
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
credentials = GoogleCredentials.get_application_default()
service = build('bigquery', 'v2', credentials=credentials)
project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
storage = jtsbq.Storage(service, project, 'dataset')
```

### Design Overview

#### Storage & Drivers

See jsontableschema layer [readme](https://github.com/okfn/jsontableschema-bigquery-py/tree/update#jsontableschema-bigquery-py).

#### Mappings

```
datapackage.json -> *not stored*
datapackage.json resources -> sql  tables
data/data.csv schema -> sql table schema
data/data.csv data -> sql table data
```

#### Drivers

Default Google BigQuery client is used as part of `jsontableschema-bigquery-py` package - [docs](https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/).

## Development

This section is intended to be used by tech users collaborating
on this project.

### Getting Started

To activate virtual environment, install
dependencies, add pre-commit hook to review and test code
and get `run` command as unified developer interface:

```
$ source activate.sh
```

### Reviewing

The project follow the next style guides:
- [Open Knowledge Coding Standards and Style Guide](https://github.com/okfn/coding-standards)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

To check the project against Python style guide:

```
$ run review
```

### Testing

To run tests with coverage check:

```
$ run test
```

Coverage data will be in the `.coverage` file.
