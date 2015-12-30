# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import re
import six
import json
import jtsbq
from datapackage import DataPackage


# Module API

def import_package(storage, descriptor, force=False, default_base_path=None):
    """Import Data Package to storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: dict/str
        Data Package descriptor.
    force: bool
        Force table rewriting If it already exists.
    default_base_path: str
        If descriptor is not a path use it as base path.

    """

    # Initiate model
    model = DataPackage(descriptor, default_base_path=default_base_path)

    # Create resources
    for resource in model.resources:

        # Prepare parameters
        table = _convert_path(resource.metadata['path'])
        schema = resource.metadata['schema']
        data = resource.local_data_path

        # Import resource
        jtsbq.import_resource(storage, table, schema, data, force=force)


def export_package(storage, descriptor):
    """Export Data Package from storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: str
        Path where to store descriptor.

    """

    # Iterate over tables
    resources = []
    for table in storage.tables:

        # Export resource data
        schema = {}
        data = _restore_path(table)
        data = os.path.join(os.path.dirname(descriptor), data)
        jtsbq.export_resource(storage, table, schema, data)

        # Add resource metadata
        metadata = {'schema': schema, 'path': data}
        resources.append(metadata)

    # Write descriptor
    with io.open(descriptor,
                 mode=_write_mode,
                 encoding=_write_encoding) as file:
        descriptor = {'resources': resources}
        json.dump(descriptor, file, indent=4)


# Internal

_write_mode = 'w'
if six.PY2:
    _write_mode = 'wb'

_write_encoding = 'utf-8'
if six.PY2:
    _write_encoding = None


def _convert_path(path):
    table = os.path.splitext(path)[0]
    table = path.replace(os.path.sep, '__')
    table = re.sub('[^0-9a-zA-Z_]+', '_', path)
    return table


def _restore_path(table):
    path = table.replace('__', os.path.sep)
    path += '.csv'
    return path
